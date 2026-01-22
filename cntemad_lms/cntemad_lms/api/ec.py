"""API endpoints for EC (Élément Constitutif) operations."""

import frappe
from frappe import _


@frappe.whitelist(allow_guest=True)
def get_available_ecs(
    year: str = None,
    course: str = None,
    search: str = None,
    sort_by: str = "title",
    limit: int = 20,
    offset: int = 0,
) -> dict:
    """
    Récupère la liste des EC disponibles (catalogue).

    Args:
        year: Filtrer par année (L1, L2, L3, M1, M2)
        course: Filtrer par cours parent
        search: Recherche textuelle
        sort_by: Tri (title, price, created)
        limit: Nombre de résultats
        offset: Décalage pour pagination

    Returns:
        dict: { ecs: [], total: int, has_more: bool }
    """
    filters = {"is_published": 1}

    if year:
        filters["year"] = year

    if course:
        filters["course"] = course

    # Build query
    ecs = frappe.get_all(
        "CNTEMAD EC",
        filters=filters,
        fields=[
            "name",
            "title",
            "description",
            "course",
            "year",
            "price",
            "duration_hours",
            "image",
            "is_published",
            "creation",
        ],
        order_by=f"{sort_by} asc" if sort_by in ["title", "price"] else "creation desc",
        limit_page_length=limit,
        start=offset,
    )

    # Search filter (post-query for simplicity)
    if search:
        search_lower = search.lower()
        ecs = [
            ec for ec in ecs
            if search_lower in (ec.title or "").lower()
            or search_lower in (ec.description or "").lower()
        ]

    # Get total count
    total = frappe.db.count("CNTEMAD EC", filters=filters)

    # Check if user has paid for each EC
    user = frappe.session.user
    if user != "Guest":
        student_id = frappe.db.get_value("CNTEMAD Student", {"user": user}, "name")
        if student_id:
            for ec in ecs:
                enrollment = frappe.db.get_value(
                    "CNTEMAD Enrollment",
                    {"student": student_id, "ec": ec.name},
                    ["status", "name"],
                    as_dict=True,
                )
                if enrollment:
                    ec["user_status"] = enrollment.status.lower().replace(" ", "_")
                else:
                    ec["user_status"] = "not_paid"
        else:
            for ec in ecs:
                ec["user_status"] = "not_paid"
    else:
        for ec in ecs:
            ec["user_status"] = "not_paid"

    return {
        "ecs": ecs,
        "total": total,
        "has_more": offset + len(ecs) < total,
    }


@frappe.whitelist(allow_guest=True)
def get_ec_detail(ec_id: str) -> dict:
    """
    Récupère le détail d'un EC.

    Args:
        ec_id: ID de l'EC

    Returns:
        dict: Détails de l'EC avec contenu si payé
    """
    if not frappe.db.exists("CNTEMAD EC", ec_id):
        frappe.throw(_("EC non trouvé"), frappe.DoesNotExistError)

    ec = frappe.get_doc("CNTEMAD EC", ec_id)

    result = {
        "name": ec.name,
        "title": ec.title,
        "description": ec.description,
        "course": ec.course,
        "course_title": frappe.db.get_value("CNTEMAD Course", ec.course, "title") if ec.course else None,
        "year": ec.year,
        "price": ec.price,
        "duration_hours": ec.duration_hours,
        "image": ec.image,
        "user_status": "not_paid",
        "content": None,
        "quiz_id": None,
    }

    # Check user access
    user = frappe.session.user
    if user != "Guest":
        student_id = frappe.db.get_value("CNTEMAD Student", {"user": user}, "name")
        if student_id:
            enrollment = frappe.db.get_value(
                "CNTEMAD Enrollment",
                {"student": student_id, "ec": ec_id},
                ["status", "name"],
                as_dict=True,
            )
            if enrollment:
                result["user_status"] = enrollment.status.lower().replace(" ", "_")

                # If paid, include content
                if enrollment.status in ["Paid", "In Progress", "Validated"]:
                    result["content"] = ec.content if hasattr(ec, "content") else None
                    result["quiz_id"] = ec.quiz if hasattr(ec, "quiz") else None

    return result


@frappe.whitelist()
def get_ec_content(ec_id: str) -> dict:
    """
    Récupère le contenu complet d'un EC avec les leçons (requiert paiement).

    Args:
        ec_id: ID de l'EC

    Returns:
        dict: {
            ec: EC details,
            lessons: List of lessons,
            progress: User progress
        }
    """
    user = frappe.session.user
    student_id = frappe.db.get_value("CNTEMAD Student", {"user": user}, "name")

    if not student_id:
        frappe.throw(_("Profil étudiant non trouvé"))

    # Vérifier l'accès
    enrollment = frappe.db.get_value(
        "CNTEMAD Enrollment",
        {"student": student_id, "ec": ec_id},
        ["status", "name", "completed_lessons"],
        as_dict=True,
    )

    ec = frappe.get_doc("CNTEMAD EC", ec_id)

    is_paid = enrollment and enrollment.status in ["Paid", "In Progress", "Validated"]

    ec_data = {
        "name": ec.name,
        "title": ec.title,
        "description": ec.description,
        "is_paid": is_paid,
        "quiz_id": ec.quiz if hasattr(ec, "quiz") else None,
    }

    if not is_paid:
        return {"ec": ec_data, "lessons": [], "progress": None}

    # Get lessons from Course Lesson (LMS) or custom content
    lessons = get_ec_lessons(ec)

    # Get user progress
    completed_lessons = []
    if enrollment and enrollment.completed_lessons:
        try:
            import json
            completed_lessons = json.loads(enrollment.completed_lessons)
        except:
            completed_lessons = []

    return {
        "ec": ec_data,
        "lessons": lessons,
        "progress": {
            "completed_lessons": completed_lessons,
            "total_lessons": len(lessons),
        },
    }


def get_ec_lessons(ec) -> list:
    """
    Get lessons for an EC from various sources.

    Returns list of lesson objects.
    """
    lessons = []

    # Try to get from linked LMS Course
    course_id = ec.get("lms_course") or ec.get("course")

    if course_id:
        # Get LMS Course lessons
        lms_lessons = frappe.get_all(
            "Course Lesson",
            filters={"course": course_id},
            fields=[
                "name", "title", "content", "youtube_link",
                "content_type", "idx"
            ],
            order_by="idx asc",
        )

        for lesson in lms_lessons:
            lessons.append({
                "name": lesson.name,
                "title": lesson.title,
                "content": lesson.content,
                "video_url": lesson.youtube_link,
                "content_type": determine_content_type(lesson),
            })

    # Fallback: Use EC's own content field
    if not lessons and hasattr(ec, "content") and ec.content:
        lessons.append({
            "name": f"{ec.name}-main",
            "title": ec.title,
            "content": ec.content,
            "content_type": "text",
        })

    # If still no lessons, create sample content
    if not lessons:
        lessons = [
            {
                "name": f"{ec.name}-intro",
                "title": "Introduction",
                "content": f"<h2>Bienvenue dans {ec.title}</h2><p>Ce module vous permettra d'apprendre les concepts fondamentaux.</p>",
                "content_type": "text",
            },
            {
                "name": f"{ec.name}-content",
                "title": "Contenu principal",
                "content": "<p>Le contenu de cette leçon sera bientôt disponible.</p>",
                "content_type": "text",
            },
        ]

    return lessons


def determine_content_type(lesson) -> str:
    """Determine the content type for a lesson."""
    if lesson.youtube_link:
        return "video"
    if lesson.content_type:
        return lesson.content_type.lower()
    if lesson.content and (".pdf" in lesson.content.lower() or "application/pdf" in lesson.content.lower()):
        return "pdf"
    return "text"


@frappe.whitelist()
def update_lesson_progress(ec_id: str, lesson_id: str, completed: bool = True) -> dict:
    """
    Update lesson completion progress for a student.

    Args:
        ec_id: EC identifier
        lesson_id: Lesson identifier
        completed: Whether lesson is completed

    Returns:
        dict: Updated progress
    """
    import json

    user = frappe.session.user
    student_id = frappe.db.get_value("CNTEMAD Student", {"user": user}, "name")

    if not student_id:
        frappe.throw(_("Profil étudiant non trouvé"))

    enrollment = frappe.db.get_value(
        "CNTEMAD Enrollment",
        {"student": student_id, "ec": ec_id},
        ["name", "completed_lessons", "status"],
        as_dict=True,
    )

    if not enrollment:
        frappe.throw(_("Inscription non trouvée"))

    # Parse existing completed lessons
    completed_lessons = []
    if enrollment.completed_lessons:
        try:
            completed_lessons = json.loads(enrollment.completed_lessons)
        except:
            completed_lessons = []

    # Update completion
    if completed and lesson_id not in completed_lessons:
        completed_lessons.append(lesson_id)
    elif not completed and lesson_id in completed_lessons:
        completed_lessons.remove(lesson_id)

    # Update status to In Progress if not already validated
    new_status = enrollment.status
    if enrollment.status == "Paid":
        new_status = "In Progress"

    frappe.db.set_value("CNTEMAD Enrollment", enrollment.name, {
        "completed_lessons": json.dumps(completed_lessons),
        "status": new_status,
    })

    frappe.db.commit()

    return {
        "completed_lessons": completed_lessons,
        "status": new_status,
    }


@frappe.whitelist()
def get_years() -> list:
    """Retourne la liste des années universitaires disponibles."""
    return [
        {"value": "L1", "label": "Licence 1"},
        {"value": "L2", "label": "Licence 2"},
        {"value": "L3", "label": "Licence 3"},
        {"value": "M1", "label": "Master 1"},
        {"value": "M2", "label": "Master 2"},
    ]


@frappe.whitelist()
def get_courses_for_filter() -> list:
    """Retourne la liste des cours pour les filtres."""
    courses = frappe.get_all(
        "CNTEMAD Course",
        filters={"is_published": 1},
        fields=["name", "title", "year"],
        order_by="title asc",
    )
    return [{"value": c.name, "label": c.title} for c in courses]
