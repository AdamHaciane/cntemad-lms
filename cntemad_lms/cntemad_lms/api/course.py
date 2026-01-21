"""API endpoints for course operations."""

import frappe
from frappe import _


@frappe.whitelist(allow_guest=True)
def get_courses(center: str = None, year: str = None, limit: int = 20) -> list:
    """
    Récupère la liste des cours disponibles.

    Args:
        center: Filtrer par centre (optionnel)
        year: Filtrer par année (L1, L2, L3, M1, M2)
        limit: Nombre max de résultats

    Returns:
        list: Liste des cours
    """
    filters = {"is_published": 1}

    if center:
        filters["center"] = center
    if year:
        filters["year"] = year

    courses = frappe.get_all(
        "CNTEMAD Course",
        filters=filters,
        fields=[
            "name",
            "title",
            "description",
            "image",
            "year",
            "ec_count",
            "instructor",
        ],
        order_by="title asc",
        limit=limit,
    )

    return courses


@frappe.whitelist()
def get_course_content(course_id: str) -> dict:
    """
    Récupère le contenu complet d'un cours.

    Args:
        course_id: ID du cours

    Returns:
        dict: Détails du cours avec EC
    """
    if not frappe.db.exists("CNTEMAD Course", course_id):
        frappe.throw(_("Cours non trouvé"))

    course = frappe.get_doc("CNTEMAD Course", course_id)

    # Get ECs
    ecs = frappe.get_all(
        "CNTEMAD EC",
        filters={"course": course_id},
        fields=[
            "name",
            "title",
            "description",
            "order",
            "duration_hours",
            "is_mandatory",
        ],
        order_by="order asc",
    )

    # Check user enrollment if logged in
    user_progress = None
    if frappe.session.user != "Guest":
        student_id = frappe.db.get_value(
            "CNTEMAD Student", {"user": frappe.session.user}, "name"
        )
        if student_id:
            user_progress = get_user_course_progress(student_id, course_id)

    return {
        "course": {
            "name": course.name,
            "title": course.title,
            "description": course.description,
            "image": course.image,
            "year": course.year,
            "instructor": course.instructor,
        },
        "ecs": ecs,
        "user_progress": user_progress,
    }


def get_user_course_progress(student_id: str, course_id: str) -> dict:
    """Récupère la progression d'un étudiant sur un cours."""
    enrollments = frappe.get_all(
        "CNTEMAD Enrollment",
        filters={
            "student": student_id,
            "course": course_id,
        },
        fields=["ec", "status", "progress_percent", "validation_date"],
    )

    ec_status = {e["ec"]: e for e in enrollments}

    total_ecs = frappe.db.count("CNTEMAD EC", {"course": course_id})
    completed_ecs = len([e for e in enrollments if e["status"] == "Validated"])

    return {
        "total_ecs": total_ecs,
        "completed_ecs": completed_ecs,
        "progress_percent": (completed_ecs / total_ecs * 100) if total_ecs > 0 else 0,
        "ec_status": ec_status,
    }
