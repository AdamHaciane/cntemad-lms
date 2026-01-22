"""API endpoints for student operations."""

import frappe
from frappe import _


@frappe.whitelist()
def get_student_progress(student_id: str) -> dict:
    """
    Récupère la progression d'un étudiant.

    Args:
        student_id: ID de l'étudiant (CNTEMAD Student)

    Returns:
        dict: {
            "total_ec": int,
            "validated_ec": int,
            "progress_percent": float,
            "current_year": str
        }

    Raises:
        frappe.DoesNotExistError: Si l'étudiant n'existe pas
    """
    if not frappe.db.exists("CNTEMAD Student", student_id):
        frappe.throw(_("Étudiant non trouvé"), frappe.DoesNotExistError)

    student = frappe.get_doc("CNTEMAD Student", student_id)

    # Get enrollments
    enrollments = frappe.get_all(
        "CNTEMAD Enrollment",
        filters={"student": student_id},
        fields=["ec", "status", "validation_date"],
    )

    total_ec = len(enrollments)
    validated_ec = len([e for e in enrollments if e.status == "Validated"])
    progress_percent = (validated_ec / total_ec * 100) if total_ec > 0 else 0

    return {
        "total_ec": total_ec,
        "validated_ec": validated_ec,
        "progress_percent": round(progress_percent, 1),
        "current_year": student.current_year or "L1",
        "enrollments": enrollments,
    }


@frappe.whitelist()
def get_student_dashboard(student_id: str = None) -> dict:
    """
    Récupère les données du dashboard étudiant.

    Args:
        student_id: ID de l'étudiant (optionnel, utilise l'utilisateur courant)

    Returns:
        dict: Données du dashboard
    """
    if not student_id:
        student_id = frappe.db.get_value(
            "CNTEMAD Student", {"user": frappe.session.user}, "name"
        )

    if not student_id:
        frappe.throw(_("Profil étudiant non trouvé"))

    progress = get_student_progress(student_id)
    student = frappe.get_doc("CNTEMAD Student", student_id)

    # Recent activities
    recent_enrollments = frappe.get_all(
        "CNTEMAD Enrollment",
        filters={"student": student_id},
        fields=["ec", "status", "modified"],
        order_by="modified desc",
        limit=5,
    )

    # Pending payments
    pending_payments = frappe.get_all(
        "CNTEMAD Payment",
        filters={"student": student_id, "status": "Pending"},
        fields=["amount", "provider", "creation"],
    )

    return {
        "student": {
            "name": student.name,
            "full_name": student.full_name,
            "center": student.center,
            "current_year": student.current_year,
        },
        "progress": progress,
        "recent_activities": recent_enrollments,
        "pending_payments": pending_payments,
    }
