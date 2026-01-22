"""API endpoints for Evaluator operations (corrections and certificates)."""

import frappe
from frappe import _
import json
from datetime import datetime, timedelta


@frappe.whitelist()
def get_evaluator_dashboard() -> dict:
    """
    Get evaluator dashboard with pending corrections and stats.

    Returns:
        dict: {
            stats: Evaluator stats,
            pending_corrections: List of pending,
            recent_corrections: Recently graded,
            pending_certificates: Certificates to validate
        }
    """
    user = frappe.session.user

    # Get evaluator profile
    evaluator = get_evaluator_profile(user)

    # Stats
    stats = get_evaluator_stats(user)

    # Pending corrections
    pending = get_pending_corrections(user, limit=10)

    # Recent corrections
    recent = get_recent_corrections(user, limit=5)

    # Pending certificates
    certificates = get_pending_certificates(user, limit=5)

    return {
        "evaluator": evaluator,
        "stats": stats,
        "pending_corrections": pending,
        "recent_corrections": recent,
        "pending_certificates": certificates
    }


def get_evaluator_profile(user: str) -> dict:
    """Get evaluator profile info."""
    # Check if user is Course Evaluator
    evaluator = frappe.db.get_value(
        "Course Evaluator",
        {"evaluator": user},
        ["name", "evaluator", "evaluator_name"],
        as_dict=True
    )

    if evaluator:
        return {
            "name": evaluator.name,
            "user": evaluator.evaluator,
            "full_name": evaluator.evaluator_name or frappe.db.get_value("User", user, "full_name")
        }

    # Fallback to user info
    return {
        "name": user,
        "user": user,
        "full_name": frappe.db.get_value("User", user, "full_name")
    }


def get_evaluator_stats(user: str) -> dict:
    """Get evaluator statistics."""
    # Total corrections done
    total_corrections = frappe.db.count(
        "CNTEMAD Submission",
        {"graded_by": user}
    ) if frappe.db.exists("DocType", "CNTEMAD Submission") else 0

    # This month
    month_start = datetime.now().replace(day=1, hour=0, minute=0, second=0)
    corrections_this_month = frappe.db.count(
        "CNTEMAD Submission",
        {"graded_by": user, "graded_at": [">=", month_start]}
    ) if frappe.db.exists("DocType", "CNTEMAD Submission") else 0

    # Pending count
    pending_count = len(get_pending_corrections(user, limit=1000))

    # Certificates validated
    certificates_validated = frappe.db.count(
        "LMS Certificate",
        {"evaluator": user}
    ) if frappe.db.exists("DocType", "LMS Certificate") else 0

    # Average grade given
    avg_grade = 0
    if frappe.db.exists("DocType", "CNTEMAD Submission"):
        result = frappe.db.sql("""
            SELECT AVG(grade)
            FROM `tabCNTEMAD Submission`
            WHERE graded_by = %s AND grade IS NOT NULL
        """, [user])
        avg_grade = round(result[0][0] or 0, 1)

    return {
        "total_corrections": total_corrections,
        "corrections_this_month": corrections_this_month,
        "pending_count": pending_count,
        "certificates_validated": certificates_validated,
        "avg_grade": avg_grade
    }


@frappe.whitelist()
def get_pending_corrections(user: str = None, limit: int = 20, offset: int = 0) -> list:
    """
    Get list of submissions pending correction.

    Args:
        user: Evaluator user (defaults to current)
        limit: Number of results
        offset: Pagination offset

    Returns:
        list: Pending submissions
    """
    if not user:
        user = frappe.session.user

    # Check if CNTEMAD Submission exists, if not use quiz attempts
    if frappe.db.exists("DocType", "CNTEMAD Submission"):
        submissions = frappe.get_all(
            "CNTEMAD Submission",
            filters={
                "status": "Pending",
                "assigned_evaluator": ["in", [user, None, ""]]
            },
            fields=[
                "name", "student", "ec", "submission_date",
                "submission_type", "file_url"
            ],
            order_by="submission_date asc",
            limit_page_length=limit,
            start=offset
        )

        for sub in submissions:
            sub["student_name"] = frappe.db.get_value(
                "CNTEMAD Student", sub.student, "full_name"
            )
            sub["ec_title"] = frappe.db.get_value(
                "CNTEMAD EC", sub.ec, "title"
            )

        return submissions

    # Fallback: use enrollments with quiz attempts that need review
    enrollments = frappe.get_all(
        "CNTEMAD Enrollment",
        filters={
            "status": "In Progress",
            "quiz_attempts": [">", 0],
            "needs_review": 1
        } if frappe.db.has_column("CNTEMAD Enrollment", "needs_review") else {
            "status": "In Progress",
            "quiz_attempts": [">", 0]
        },
        fields=[
            "name", "student", "ec", "quiz_score",
            "quiz_attempts", "modified"
        ],
        order_by="modified desc",
        limit_page_length=limit,
        start=offset
    )

    for e in enrollments:
        e["student_name"] = frappe.db.get_value(
            "CNTEMAD Student", e.student, "full_name"
        )
        e["ec_title"] = frappe.db.get_value(
            "CNTEMAD EC", e.ec, "title"
        )
        e["submission_date"] = e.modified
        e["submission_type"] = "quiz"

    return enrollments


@frappe.whitelist()
def get_recent_corrections(user: str = None, limit: int = 10) -> list:
    """Get recently corrected submissions."""
    if not user:
        user = frappe.session.user

    if frappe.db.exists("DocType", "CNTEMAD Submission"):
        corrections = frappe.get_all(
            "CNTEMAD Submission",
            filters={
                "graded_by": user,
                "status": "Graded"
            },
            fields=[
                "name", "student", "ec", "grade",
                "graded_at", "submission_type"
            ],
            order_by="graded_at desc",
            limit=limit
        )

        for c in corrections:
            c["student_name"] = frappe.db.get_value(
                "CNTEMAD Student", c.student, "full_name"
            )
            c["ec_title"] = frappe.db.get_value(
                "CNTEMAD EC", c.ec, "title"
            )

        return corrections

    return []


@frappe.whitelist()
def get_submission_detail(submission_id: str) -> dict:
    """
    Get full details of a submission for grading.

    Args:
        submission_id: Submission or enrollment ID

    Returns:
        dict: Full submission details
    """
    # Try CNTEMAD Submission first
    if frappe.db.exists("CNTEMAD Submission", submission_id):
        sub = frappe.get_doc("CNTEMAD Submission", submission_id)

        student = frappe.get_doc("CNTEMAD Student", sub.student)
        ec = frappe.get_doc("CNTEMAD EC", sub.ec)

        return {
            "type": "submission",
            "name": sub.name,
            "student": {
                "name": student.name,
                "full_name": student.full_name,
                "email": student.email,
                "student_id": student.student_id
            },
            "ec": {
                "name": ec.name,
                "title": ec.title,
                "description": ec.description
            },
            "submission": {
                "date": sub.submission_date,
                "type": sub.submission_type,
                "file_url": sub.file_url,
                "content": sub.get("content"),
                "answers": sub.get("answers")
            },
            "grading": {
                "status": sub.status,
                "grade": sub.grade,
                "feedback": sub.feedback,
                "graded_by": sub.graded_by,
                "graded_at": sub.graded_at
            }
        }

    # Try enrollment (quiz review)
    if frappe.db.exists("CNTEMAD Enrollment", submission_id):
        enrollment = frappe.get_doc("CNTEMAD Enrollment", submission_id)

        student = frappe.get_doc("CNTEMAD Student", enrollment.student)
        ec = frappe.get_doc("CNTEMAD EC", enrollment.ec)

        # Get quiz history if available
        quiz_history = []
        if ec.get("quiz"):
            quiz_history = frappe.get_all(
                "LMS Quiz Submission",
                filters={
                    "quiz": ec.quiz,
                    "member": student.user if hasattr(student, "user") else None
                },
                fields=["name", "score", "creation"],
                order_by="creation desc",
                limit=5
            ) if frappe.db.exists("DocType", "LMS Quiz Submission") else []

        return {
            "type": "enrollment",
            "name": enrollment.name,
            "student": {
                "name": student.name,
                "full_name": student.full_name,
                "email": student.email,
                "student_id": student.student_id
            },
            "ec": {
                "name": ec.name,
                "title": ec.title,
                "description": ec.description
            },
            "submission": {
                "date": enrollment.modified,
                "type": "quiz",
                "quiz_score": enrollment.quiz_score,
                "quiz_attempts": enrollment.quiz_attempts,
                "quiz_history": quiz_history
            },
            "grading": {
                "status": enrollment.status,
                "grade": enrollment.quiz_score,
                "feedback": enrollment.get("evaluator_feedback"),
                "graded_by": enrollment.get("graded_by"),
                "graded_at": enrollment.get("graded_at")
            }
        }

    frappe.throw(_("Soumission non trouvée"), frappe.DoesNotExistError)


@frappe.whitelist()
def submit_grade(
    submission_id: str,
    grade: float,
    feedback: str = None,
    validate_ec: bool = False
) -> dict:
    """
    Submit a grade for a submission.

    Args:
        submission_id: Submission or enrollment ID
        grade: Grade value (0-100 or 0-20)
        feedback: Written feedback
        validate_ec: Whether to mark EC as validated

    Returns:
        dict: { success: bool, message: str }
    """
    user = frappe.session.user

    # Handle CNTEMAD Submission
    if frappe.db.exists("CNTEMAD Submission", submission_id):
        frappe.db.set_value("CNTEMAD Submission", submission_id, {
            "status": "Graded",
            "grade": grade,
            "feedback": feedback,
            "graded_by": user,
            "graded_at": datetime.now()
        })

        # Get enrollment to potentially validate
        sub = frappe.db.get_value(
            "CNTEMAD Submission", submission_id,
            ["student", "ec"], as_dict=True
        )

        if validate_ec and sub:
            enrollment = frappe.db.get_value(
                "CNTEMAD Enrollment",
                {"student": sub.student, "ec": sub.ec},
                "name"
            )
            if enrollment:
                frappe.db.set_value("CNTEMAD Enrollment", enrollment, {
                    "status": "Validated",
                    "final_grade": grade
                })

        frappe.db.commit()
        return {"success": True, "message": "Note enregistrée"}

    # Handle enrollment (quiz)
    if frappe.db.exists("CNTEMAD Enrollment", submission_id):
        update_data = {
            "evaluator_feedback": feedback,
            "graded_by": user,
            "graded_at": datetime.now()
        }

        if validate_ec:
            update_data["status"] = "Validated"
            update_data["final_grade"] = grade

        if frappe.db.has_column("CNTEMAD Enrollment", "needs_review"):
            update_data["needs_review"] = 0

        frappe.db.set_value("CNTEMAD Enrollment", submission_id, update_data)
        frappe.db.commit()

        return {"success": True, "message": "Évaluation enregistrée"}

    frappe.throw(_("Soumission non trouvée"))


@frappe.whitelist()
def get_pending_certificates(user: str = None, limit: int = 20) -> list:
    """
    Get certificates pending validation.

    Args:
        user: Evaluator user
        limit: Number of results

    Returns:
        list: Pending certificates
    """
    if not user:
        user = frappe.session.user

    # Get students who have completed all ECs for a year
    # A certificate is pending when all ECs of a year are validated

    certificates = []

    # Get all years
    years = ["L1", "L2", "L3", "M1", "M2"]

    for year in years:
        # Get total ECs for this year
        total_ecs = frappe.db.count("CNTEMAD EC", {"year": year, "is_published": 1})
        if total_ecs == 0:
            continue

        # Find students who validated all ECs for this year
        students_complete = frappe.db.sql("""
            SELECT
                s.name as student_id,
                s.full_name,
                s.email,
                s.center,
                COUNT(e.name) as validated_count
            FROM `tabCNTEMAD Student` s
            JOIN `tabCNTEMAD Enrollment` e ON e.student = s.name
            JOIN `tabCNTEMAD EC` ec ON e.ec = ec.name
            WHERE ec.year = %s
            AND e.status = 'Validated'
            GROUP BY s.name
            HAVING validated_count >= %s
            LIMIT %s
        """, [year, total_ecs, limit], as_dict=True)

        for student in students_complete:
            # Check if certificate already exists
            existing = frappe.db.exists(
                "LMS Certificate",
                {"member": student.student_id, "course": year}
            ) if frappe.db.exists("DocType", "LMS Certificate") else False

            if not existing:
                center_name = frappe.db.get_value(
                    "CNTEMAD Center", student.center, "center_name"
                ) if student.center else None

                certificates.append({
                    "student_id": student.student_id,
                    "student_name": student.full_name,
                    "email": student.email,
                    "center": center_name,
                    "year": year,
                    "validated_ecs": student.validated_count,
                    "total_ecs": total_ecs
                })

    return certificates[:limit]


@frappe.whitelist()
def validate_certificate(
    student_id: str,
    year: str,
    certificate_number: str = None
) -> dict:
    """
    Validate and create a certificate for a student.

    Args:
        student_id: Student ID
        year: Academic year (L1, L2, etc.)
        certificate_number: Optional certificate number

    Returns:
        dict: { success: bool, certificate_id: str }
    """
    user = frappe.session.user

    # Verify student exists
    if not frappe.db.exists("CNTEMAD Student", student_id):
        frappe.throw(_("Étudiant non trouvé"))

    student = frappe.get_doc("CNTEMAD Student", student_id)

    # Verify all ECs are validated
    total_ecs = frappe.db.count("CNTEMAD EC", {"year": year, "is_published": 1})
    validated_ecs = frappe.db.count(
        "CNTEMAD Enrollment",
        {
            "student": student_id,
            "status": "Validated",
            "ec": ["in", frappe.get_all("CNTEMAD EC", {"year": year}, pluck="name")]
        }
    )

    if validated_ecs < total_ecs:
        frappe.throw(_(f"L'étudiant n'a pas validé tous les EC ({validated_ecs}/{total_ecs})"))

    # Generate certificate number if not provided
    if not certificate_number:
        certificate_number = f"CNTEMAD-{year}-{datetime.now().strftime('%Y%m%d')}-{student_id[-4:]}"

    # Create certificate record
    if frappe.db.exists("DocType", "LMS Certificate"):
        cert = frappe.get_doc({
            "doctype": "LMS Certificate",
            "member": student.user if hasattr(student, "user") else student_id,
            "course": year,
            "issue_date": datetime.now(),
            "expiry_date": None,
            "evaluator": user
        })
        cert.insert()
        cert_id = cert.name
    else:
        # Create simple certificate record
        cert_id = frappe.generate_hash()[:10]
        frappe.db.sql("""
            INSERT INTO `tabCNTEMAD Certificate`
            (name, student, year, certificate_number, issued_by, issued_at)
            VALUES (%s, %s, %s, %s, %s, %s)
        """, [cert_id, student_id, year, certificate_number, user, datetime.now()])

    frappe.db.commit()

    # Send notification to student
    try:
        frappe.sendmail(
            recipients=[student.email],
            subject=f"Félicitations ! Certificat {year} validé",
            message=f"""
            <p>Cher(e) {student.full_name},</p>
            <p>Félicitations ! Votre certificat pour l'année {year} a été validé.</p>
            <p>Numéro de certificat: <strong>{certificate_number}</strong></p>
            <p>Cordialement,<br>CNTEMAD</p>
            """
        )
    except Exception:
        pass  # Email failure should not block certificate creation

    return {
        "success": True,
        "certificate_id": cert_id,
        "certificate_number": certificate_number,
        "message": f"Certificat {year} créé pour {student.full_name}"
    }


@frappe.whitelist()
def get_grading_rubric(ec_id: str = None) -> dict:
    """
    Get grading rubric/criteria for an EC.

    Args:
        ec_id: EC identifier

    Returns:
        dict: Grading criteria
    """
    # Default rubric
    rubric = {
        "scale": "0-20",
        "passing_grade": 10,
        "criteria": [
            {"name": "Compréhension", "weight": 30, "description": "Compréhension du sujet"},
            {"name": "Analyse", "weight": 25, "description": "Qualité de l'analyse"},
            {"name": "Argumentation", "weight": 25, "description": "Clarté de l'argumentation"},
            {"name": "Présentation", "weight": 20, "description": "Qualité de la présentation"}
        ],
        "grade_labels": {
            "0-5": "Insuffisant",
            "6-9": "Passable",
            "10-12": "Assez bien",
            "13-15": "Bien",
            "16-18": "Très bien",
            "19-20": "Excellent"
        }
    }

    # Try to get EC-specific rubric if exists
    if ec_id and frappe.db.exists("CNTEMAD EC", ec_id):
        ec = frappe.get_doc("CNTEMAD EC", ec_id)
        if hasattr(ec, "grading_rubric") and ec.grading_rubric:
            try:
                custom_rubric = json.loads(ec.grading_rubric)
                rubric.update(custom_rubric)
            except Exception:
                pass

    return rubric
