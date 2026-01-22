"""API endpoints for Teacher/Instructor operations."""

import frappe
from frappe import _
import json


@frappe.whitelist()
def get_my_courses() -> dict:
    """
    Get courses created by the current teacher.

    Returns:
        dict: { courses: [], total: int }
    """
    user = frappe.session.user

    # Get teacher profile
    teacher_id = frappe.db.get_value("LMS Instructor", {"user": user}, "name")

    if not teacher_id:
        # Fallback: check if user created any courses
        courses = frappe.get_all(
            "CNTEMAD Course",
            filters={"owner": user},
            fields=[
                "name", "title", "description", "year", "is_published",
                "image", "creation", "modified"
            ],
            order_by="modified desc"
        )
    else:
        # Get courses linked to instructor
        course_links = frappe.get_all(
            "Course Instructor",
            filters={"instructor": teacher_id},
            pluck="parent"
        )

        if course_links:
            courses = frappe.get_all(
                "CNTEMAD Course",
                filters={"name": ["in", course_links]},
                fields=[
                    "name", "title", "description", "year", "is_published",
                    "image", "creation", "modified"
                ],
                order_by="modified desc"
            )
        else:
            courses = []

    # Add EC count and stats for each course
    for course in courses:
        course["ec_count"] = frappe.db.count(
            "CNTEMAD EC",
            filters={"course": course.name}
        )
        course["student_count"] = get_course_student_count(course.name)

    return {
        "courses": courses,
        "total": len(courses)
    }


@frappe.whitelist()
def get_course_ecs(course_id: str) -> dict:
    """
    Get all ECs for a course.

    Args:
        course_id: Course identifier

    Returns:
        dict: { ecs: [], course: {} }
    """
    if not frappe.db.exists("CNTEMAD Course", course_id):
        frappe.throw(_("Cours non trouvé"), frappe.DoesNotExistError)

    course = frappe.get_doc("CNTEMAD Course", course_id)

    ecs = frappe.get_all(
        "CNTEMAD EC",
        filters={"course": course_id},
        fields=[
            "name", "title", "description", "price", "duration_hours",
            "is_published", "image", "creation", "modified"
        ],
        order_by="creation asc"
    )

    # Add stats for each EC
    for ec in ecs:
        stats = get_ec_stats_data(ec.name)
        ec.update(stats)

    return {
        "ecs": ecs,
        "course": {
            "name": course.name,
            "title": course.title,
            "year": course.year
        }
    }


@frappe.whitelist()
def get_ec_for_edit(ec_id: str) -> dict:
    """
    Get EC data for editing.

    Args:
        ec_id: EC identifier

    Returns:
        dict: EC data with content and quiz
    """
    if not frappe.db.exists("CNTEMAD EC", ec_id):
        frappe.throw(_("EC non trouvé"), frappe.DoesNotExistError)

    ec = frappe.get_doc("CNTEMAD EC", ec_id)

    # Get quiz if exists
    quiz_data = None
    if ec.get("quiz"):
        quiz = frappe.get_doc("LMS Quiz", ec.quiz)
        questions = []
        for q in quiz.get("questions", []):
            question_doc = frappe.get_doc("LMS Question", q.question)
            questions.append({
                "name": question_doc.name,
                "question": question_doc.question,
                "type": question_doc.type,
                "options": [
                    {
                        "option": opt.option,
                        "is_correct": opt.is_correct
                    }
                    for opt in question_doc.get("options", [])
                ]
            })
        quiz_data = {
            "name": quiz.name,
            "title": quiz.title,
            "passing_percentage": quiz.passing_percentage,
            "max_attempts": quiz.max_attempts,
            "time_limit": quiz.time_limit,
            "questions": questions
        }

    # Get lessons/content
    lessons = []
    if ec.get("lms_course") or ec.get("course"):
        course_id = ec.get("lms_course") or ec.get("course")
        lms_lessons = frappe.get_all(
            "Course Lesson",
            filters={"course": course_id},
            fields=["name", "title", "content", "youtube_link", "content_type", "idx"],
            order_by="idx asc"
        )
        lessons = lms_lessons

    return {
        "name": ec.name,
        "title": ec.title,
        "description": ec.description,
        "course": ec.course,
        "year": ec.year,
        "price": ec.price,
        "duration_hours": ec.duration_hours,
        "image": ec.image,
        "content": ec.get("content"),
        "is_published": ec.is_published,
        "quiz": quiz_data,
        "lessons": lessons
    }


@frappe.whitelist()
def save_ec(
    ec_id: str = None,
    title: str = None,
    description: str = None,
    course: str = None,
    year: str = None,
    price: float = 0,
    duration_hours: int = 0,
    content: str = None,
    is_published: bool = False,
    image: str = None
) -> dict:
    """
    Create or update an EC.

    Args:
        ec_id: EC identifier (None for new)
        title: EC title
        description: EC description
        course: Parent course
        year: Academic year (L1, L2, etc.)
        price: Price in Ariary
        duration_hours: Estimated duration
        content: HTML/Markdown content
        is_published: Publication status
        image: Image URL

    Returns:
        dict: { name: str, message: str }
    """
    if ec_id and frappe.db.exists("CNTEMAD EC", ec_id):
        # Update existing
        ec = frappe.get_doc("CNTEMAD EC", ec_id)
        ec.title = title or ec.title
        ec.description = description if description is not None else ec.description
        ec.course = course or ec.course
        ec.year = year or ec.year
        ec.price = price if price is not None else ec.price
        ec.duration_hours = duration_hours if duration_hours is not None else ec.duration_hours
        ec.content = content if content is not None else ec.get("content")
        ec.is_published = is_published
        if image:
            ec.image = image
        ec.save()
        message = "EC mis à jour avec succès"
    else:
        # Create new
        ec = frappe.get_doc({
            "doctype": "CNTEMAD EC",
            "title": title,
            "description": description,
            "course": course,
            "year": year,
            "price": price or 0,
            "duration_hours": duration_hours or 0,
            "content": content,
            "is_published": is_published,
            "image": image
        })
        ec.insert()
        message = "EC créé avec succès"

    frappe.db.commit()

    return {
        "name": ec.name,
        "message": message
    }


@frappe.whitelist()
def save_ec_content(ec_id: str, lessons: str = None) -> dict:
    """
    Save lessons/content for an EC.

    Args:
        ec_id: EC identifier
        lessons: JSON string of lessons array

    Returns:
        dict: { success: bool, message: str }
    """
    if not frappe.db.exists("CNTEMAD EC", ec_id):
        frappe.throw(_("EC non trouvé"), frappe.DoesNotExistError)

    ec = frappe.get_doc("CNTEMAD EC", ec_id)
    lessons_data = json.loads(lessons) if lessons else []

    # Get or create linked LMS course for lessons
    lms_course_id = ec.get("lms_course")

    if not lms_course_id:
        # Create LMS course to hold lessons
        lms_course = frappe.get_doc({
            "doctype": "LMS Course",
            "title": ec.title,
            "short_introduction": ec.description,
            "published": ec.is_published
        })
        lms_course.insert()
        lms_course_id = lms_course.name

        # Link to EC
        frappe.db.set_value("CNTEMAD EC", ec_id, "lms_course", lms_course_id)

    # Delete existing lessons
    existing_lessons = frappe.get_all(
        "Course Lesson",
        filters={"course": lms_course_id},
        pluck="name"
    )
    for lesson_name in existing_lessons:
        frappe.delete_doc("Course Lesson", lesson_name)

    # Create new lessons
    for idx, lesson in enumerate(lessons_data):
        frappe.get_doc({
            "doctype": "Course Lesson",
            "course": lms_course_id,
            "title": lesson.get("title", f"Leçon {idx + 1}"),
            "content": lesson.get("content", ""),
            "youtube_link": lesson.get("video_url", ""),
            "content_type": lesson.get("content_type", "Text"),
            "idx": idx + 1
        }).insert()

    frappe.db.commit()

    return {
        "success": True,
        "message": f"{len(lessons_data)} leçon(s) enregistrée(s)"
    }


@frappe.whitelist()
def save_quiz(ec_id: str, quiz_data: str = None) -> dict:
    """
    Save quiz for an EC.

    Args:
        ec_id: EC identifier
        quiz_data: JSON string with quiz configuration

    Returns:
        dict: { success: bool, quiz_id: str }
    """
    if not frappe.db.exists("CNTEMAD EC", ec_id):
        frappe.throw(_("EC non trouvé"), frappe.DoesNotExistError)

    ec = frappe.get_doc("CNTEMAD EC", ec_id)
    data = json.loads(quiz_data) if quiz_data else {}

    quiz_id = ec.get("quiz")

    if quiz_id and frappe.db.exists("LMS Quiz", quiz_id):
        # Update existing quiz
        quiz = frappe.get_doc("LMS Quiz", quiz_id)
        quiz.title = data.get("title", quiz.title)
        quiz.passing_percentage = data.get("passing_percentage", 70)
        quiz.max_attempts = data.get("max_attempts", 3)
        quiz.time_limit = data.get("time_limit", 0)

        # Clear existing questions
        quiz.questions = []
        quiz.save()
    else:
        # Create new quiz
        quiz = frappe.get_doc({
            "doctype": "LMS Quiz",
            "title": data.get("title", f"Quiz - {ec.title}"),
            "passing_percentage": data.get("passing_percentage", 70),
            "max_attempts": data.get("max_attempts", 3),
            "time_limit": data.get("time_limit", 0)
        })
        quiz.insert()
        quiz_id = quiz.name

        # Link to EC
        frappe.db.set_value("CNTEMAD EC", ec_id, "quiz", quiz_id)

    # Create questions
    questions = data.get("questions", [])
    for q in questions:
        # Create question
        question = frappe.get_doc({
            "doctype": "LMS Question",
            "question": q.get("question", ""),
            "type": q.get("type", "Choices")
        })

        # Add options
        for opt in q.get("options", []):
            question.append("options", {
                "option": opt.get("option", ""),
                "is_correct": opt.get("is_correct", False)
            })

        question.insert()

        # Link to quiz
        quiz.append("questions", {"question": question.name})

    quiz.save()
    frappe.db.commit()

    return {
        "success": True,
        "quiz_id": quiz_id,
        "message": f"Quiz enregistré avec {len(questions)} question(s)"
    }


@frappe.whitelist()
def get_ec_stats(ec_id: str) -> dict:
    """
    Get detailed statistics for an EC.

    Args:
        ec_id: EC identifier

    Returns:
        dict: Detailed stats
    """
    if not frappe.db.exists("CNTEMAD EC", ec_id):
        frappe.throw(_("EC non trouvé"), frappe.DoesNotExistError)

    ec = frappe.get_doc("CNTEMAD EC", ec_id)

    # Get enrollments
    enrollments = frappe.get_all(
        "CNTEMAD Enrollment",
        filters={"ec": ec_id},
        fields=["name", "student", "status", "creation", "quiz_score", "quiz_attempts"]
    )

    total = len(enrollments)
    validated = len([e for e in enrollments if e.status == "Validated"])
    in_progress = len([e for e in enrollments if e.status in ["In Progress", "Paid"]])

    # Quiz stats
    quiz_attempts = [e for e in enrollments if e.quiz_attempts and e.quiz_attempts > 0]
    avg_score = 0
    if quiz_attempts:
        scores = [e.quiz_score for e in quiz_attempts if e.quiz_score]
        avg_score = sum(scores) / len(scores) if scores else 0

    # Revenue
    payments = frappe.get_all(
        "CNTEMAD Payment",
        filters={"ec": ec_id, "status": "Success"},
        fields=["amount"]
    )
    total_revenue = sum(p.amount for p in payments)

    # Enrollments by month (last 6 months)
    from datetime import datetime, timedelta

    months_data = []
    for i in range(5, -1, -1):
        date = datetime.now() - timedelta(days=i * 30)
        month_start = date.replace(day=1)
        if i > 0:
            next_month = (date + timedelta(days=32)).replace(day=1)
        else:
            next_month = datetime.now() + timedelta(days=1)

        count = len([
            e for e in enrollments
            if e.creation and month_start <= e.creation.replace(tzinfo=None) < next_month
        ])

        months_data.append({
            "month": month_start.strftime("%b"),
            "count": count
        })

    # Recent enrollments
    recent = frappe.get_all(
        "CNTEMAD Enrollment",
        filters={"ec": ec_id},
        fields=["student", "status", "creation"],
        order_by="creation desc",
        limit=10
    )

    for r in recent:
        student = frappe.db.get_value(
            "CNTEMAD Student", r.student,
            ["full_name", "email"], as_dict=True
        )
        r["student_name"] = student.full_name if student else r.student
        r["student_email"] = student.email if student else None

    return {
        "ec": {
            "name": ec.name,
            "title": ec.title,
            "price": ec.price,
            "is_published": ec.is_published
        },
        "stats": {
            "total_students": total,
            "validated": validated,
            "in_progress": in_progress,
            "validation_rate": round((validated / total) * 100, 1) if total > 0 else 0,
            "avg_quiz_score": round(avg_score, 1),
            "total_revenue": total_revenue
        },
        "trends": months_data,
        "recent_enrollments": recent
    }


@frappe.whitelist()
def upload_media(file_url: str = None) -> dict:
    """
    Handle media upload confirmation.

    Args:
        file_url: URL of uploaded file

    Returns:
        dict: { url: str }
    """
    # Frappe handles file upload automatically
    # This endpoint just confirms and returns the URL
    return {"url": file_url}


@frappe.whitelist()
def delete_ec(ec_id: str) -> dict:
    """
    Delete an EC (only if no enrollments).

    Args:
        ec_id: EC identifier

    Returns:
        dict: { success: bool, message: str }
    """
    if not frappe.db.exists("CNTEMAD EC", ec_id):
        frappe.throw(_("EC non trouvé"), frappe.DoesNotExistError)

    # Check for enrollments
    enrollments = frappe.db.count("CNTEMAD Enrollment", {"ec": ec_id})
    if enrollments > 0:
        frappe.throw(_(f"Impossible de supprimer: {enrollments} inscription(s) existante(s)"))

    frappe.delete_doc("CNTEMAD EC", ec_id)
    frappe.db.commit()

    return {
        "success": True,
        "message": "EC supprimé"
    }


def get_course_student_count(course_id: str) -> int:
    """Get number of unique students enrolled in a course's ECs."""
    ecs = frappe.get_all("CNTEMAD EC", filters={"course": course_id}, pluck="name")
    if not ecs:
        return 0

    students = frappe.db.sql("""
        SELECT COUNT(DISTINCT student)
        FROM `tabCNTEMAD Enrollment`
        WHERE ec IN %s
    """, [ecs])

    return students[0][0] if students else 0


def get_ec_stats_data(ec_id: str) -> dict:
    """Get basic stats for an EC."""
    enrollments = frappe.db.count("CNTEMAD Enrollment", {"ec": ec_id})
    validated = frappe.db.count("CNTEMAD Enrollment", {"ec": ec_id, "status": "Validated"})

    return {
        "student_count": enrollments,
        "validated_count": validated,
        "validation_rate": round((validated / enrollments) * 100, 1) if enrollments > 0 else 0
    }
