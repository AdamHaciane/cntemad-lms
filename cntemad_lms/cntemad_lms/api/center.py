"""API endpoints for center operations."""

import frappe
from frappe import _


@frappe.whitelist()
def get_center_stats(center_id: str) -> dict:
    """
    Récupère les statistiques d'un centre régional.

    Args:
        center_id: ID du centre

    Returns:
        dict: Statistiques du centre
    """
    if not frappe.db.exists("CNTEMAD Center", center_id):
        frappe.throw(_("Centre non trouvé"))

    # Check permission
    if not frappe.has_permission("CNTEMAD Center", "read", center_id):
        frappe.throw(_("Accès non autorisé"))

    center = frappe.get_doc("CNTEMAD Center", center_id)

    # Student stats
    total_students = frappe.db.count(
        "CNTEMAD Student", {"center": center_id}
    )
    active_students = frappe.db.count(
        "CNTEMAD Student", {"center": center_id, "status": "Active"}
    )

    # Payment stats
    payments = frappe.db.sql("""
        SELECT
            COUNT(*) as count,
            SUM(amount) as total,
            status
        FROM `tabCNTEMAD Payment`
        WHERE student IN (
            SELECT name FROM `tabCNTEMAD Student` WHERE center = %s
        )
        AND creation >= DATE_SUB(NOW(), INTERVAL 30 DAY)
        GROUP BY status
    """, center_id, as_dict=True)

    payment_stats = {p["status"]: {"count": p["count"], "total": p["total"]} for p in payments}

    # Enrollment stats
    enrollments = frappe.db.sql("""
        SELECT
            e.status,
            COUNT(*) as count
        FROM `tabCNTEMAD Enrollment` e
        INNER JOIN `tabCNTEMAD Student` s ON e.student = s.name
        WHERE s.center = %s
        GROUP BY e.status
    """, center_id, as_dict=True)

    enrollment_stats = {e["status"]: e["count"] for e in enrollments}

    return {
        "center": {
            "name": center.name,
            "title": center.title,
            "region": center.region,
        },
        "students": {
            "total": total_students,
            "active": active_students,
        },
        "payments": payment_stats,
        "enrollments": enrollment_stats,
    }


@frappe.whitelist()
def get_all_centers() -> list:
    """
    Récupère la liste de tous les centres.

    Returns:
        list: Liste des centres avec stats basiques
    """
    centers = frappe.get_all(
        "CNTEMAD Center",
        fields=["name", "title", "region", "is_active"],
        order_by="region asc, title asc",
    )

    # Add student count
    for center in centers:
        center["student_count"] = frappe.db.count(
            "CNTEMAD Student", {"center": center["name"]}
        )

    return centers
