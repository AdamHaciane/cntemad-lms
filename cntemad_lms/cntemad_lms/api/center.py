"""
API endpoints for center operations.

Admin centre régional - Dashboard, étudiants, paiements.

Usage:
    GET /api/method/cntemad_lms.api.center.get_my_center
    GET /api/method/cntemad_lms.api.center.get_center_dashboard
    GET /api/method/cntemad_lms.api.center.get_center_students
    GET /api/method/cntemad_lms.api.center.get_center_payments
"""

import frappe
from frappe import _
from frappe.utils import now_datetime, add_days, getdate, cint
from datetime import datetime, timedelta


@frappe.whitelist()
def get_my_center() -> dict:
    """
    Get the center for the current admin user.

    Returns:
        dict: Center info or None
    """
    user = frappe.session.user

    # Check if user is a center admin
    center_id = frappe.db.get_value(
        "CNTEMAD Center",
        {"admin_user": user},
        "name"
    )

    if not center_id:
        # Check if linked via custom field or role
        center_id = frappe.db.get_value(
            "CNTEMAD Center Admin",
            {"user": user, "is_active": 1},
            "center"
        ) if frappe.db.exists("DocType", "CNTEMAD Center Admin") else None

    if not center_id:
        return None

    center = frappe.get_doc("CNTEMAD Center", center_id)

    return {
        "name": center.name,
        "title": center.title,
        "region": center.region,
        "code": center.code if hasattr(center, "code") else None,
    }


@frappe.whitelist()
def get_center_dashboard(center_id: str = None) -> dict:
    """
    Get complete dashboard data for a center.

    Args:
        center_id: Center ID (optional, uses current user's center)

    Returns:
        dict: {
            center: Center info,
            kpis: Key metrics,
            trends: Enrollment trends,
            alerts: Pending actions,
            recent_activity: Recent events
        }
    """
    # Get center
    if not center_id:
        my_center = get_my_center()
        if not my_center:
            frappe.throw(_("Aucun centre associé à votre compte"))
        center_id = my_center["name"]

    if not frappe.db.exists("CNTEMAD Center", center_id):
        frappe.throw(_("Centre non trouvé"))

    center = frappe.get_doc("CNTEMAD Center", center_id)

    # KPIs
    kpis = get_center_kpis(center_id)

    # Trends (last 30 days)
    trends = get_enrollment_trends(center_id, days=30)

    # Alerts
    alerts = get_center_alerts(center_id)

    # Recent activity
    recent = get_recent_activity(center_id, limit=10)

    return {
        "center": {
            "name": center.name,
            "title": center.title,
            "region": center.region,
        },
        "kpis": kpis,
        "trends": trends,
        "alerts": alerts,
        "recent_activity": recent,
    }


def get_center_kpis(center_id: str) -> dict:
    """Get key performance indicators for a center."""
    # Student counts
    total_students = frappe.db.count("CNTEMAD Student", {"center": center_id})
    active_students = frappe.db.count(
        "CNTEMAD Student", {"center": center_id, "status": "Active"}
    )

    # This month's stats
    first_of_month = getdate().replace(day=1)

    # Payments this month
    monthly_payments = frappe.db.sql("""
        SELECT
            COUNT(*) as count,
            COALESCE(SUM(amount), 0) as total
        FROM `tabCNTEMAD Payment` p
        INNER JOIN `tabCNTEMAD Student` s ON p.student = s.name
        WHERE s.center = %s
        AND p.status = 'Completed'
        AND p.creation >= %s
    """, (center_id, first_of_month), as_dict=True)[0]

    # Pending payments
    pending_payments = frappe.db.sql("""
        SELECT COUNT(*) as count
        FROM `tabCNTEMAD Payment` p
        INNER JOIN `tabCNTEMAD Student` s ON p.student = s.name
        WHERE s.center = %s
        AND p.status IN ('Pending', 'Processing')
    """, center_id, as_dict=True)[0]

    # EC validations this month
    validations = frappe.db.sql("""
        SELECT COUNT(*) as count
        FROM `tabCNTEMAD Enrollment` e
        INNER JOIN `tabCNTEMAD Student` s ON e.student = s.name
        WHERE s.center = %s
        AND e.status = 'Validated'
        AND e.validation_date >= %s
    """, (center_id, first_of_month), as_dict=True)[0]

    # Validation rate
    total_enrollments = frappe.db.sql("""
        SELECT COUNT(*) as count
        FROM `tabCNTEMAD Enrollment` e
        INNER JOIN `tabCNTEMAD Student` s ON e.student = s.name
        WHERE s.center = %s
        AND e.status IN ('Paid', 'In Progress', 'Validated')
    """, center_id, as_dict=True)[0]

    validation_rate = 0
    if total_enrollments["count"] > 0:
        validated = frappe.db.sql("""
            SELECT COUNT(*) as count
            FROM `tabCNTEMAD Enrollment` e
            INNER JOIN `tabCNTEMAD Student` s ON e.student = s.name
            WHERE s.center = %s
            AND e.status = 'Validated'
        """, center_id, as_dict=True)[0]
        validation_rate = round((validated["count"] / total_enrollments["count"]) * 100)

    return {
        "total_students": total_students,
        "active_students": active_students,
        "monthly_payments": monthly_payments["count"],
        "monthly_revenue": monthly_payments["total"] or 0,
        "pending_payments": pending_payments["count"],
        "monthly_validations": validations["count"],
        "validation_rate": validation_rate,
    }


def get_enrollment_trends(center_id: str, days: int = 30) -> list:
    """Get daily enrollment/payment trends."""
    start_date = add_days(getdate(), -days)

    # Daily enrollments
    data = frappe.db.sql("""
        SELECT
            DATE(e.creation) as date,
            COUNT(*) as enrollments,
            SUM(CASE WHEN e.status = 'Validated' THEN 1 ELSE 0 END) as validations
        FROM `tabCNTEMAD Enrollment` e
        INNER JOIN `tabCNTEMAD Student` s ON e.student = s.name
        WHERE s.center = %s
        AND e.creation >= %s
        GROUP BY DATE(e.creation)
        ORDER BY date
    """, (center_id, start_date), as_dict=True)

    # Daily payments
    payments = frappe.db.sql("""
        SELECT
            DATE(p.creation) as date,
            COUNT(*) as payments,
            COALESCE(SUM(p.amount), 0) as revenue
        FROM `tabCNTEMAD Payment` p
        INNER JOIN `tabCNTEMAD Student` s ON p.student = s.name
        WHERE s.center = %s
        AND p.status = 'Completed'
        AND p.creation >= %s
        GROUP BY DATE(p.creation)
        ORDER BY date
    """, (center_id, start_date), as_dict=True)

    # Merge data
    payment_by_date = {str(p["date"]): p for p in payments}

    result = []
    for d in data:
        date_str = str(d["date"])
        p = payment_by_date.get(date_str, {})
        result.append({
            "date": date_str,
            "enrollments": d["enrollments"],
            "validations": d["validations"],
            "payments": p.get("payments", 0),
            "revenue": p.get("revenue", 0),
        })

    return result


def get_center_alerts(center_id: str) -> list:
    """Get alerts/pending actions for a center."""
    alerts = []

    # Pending payments (> 24h)
    old_pending = frappe.db.sql("""
        SELECT COUNT(*) as count
        FROM `tabCNTEMAD Payment` p
        INNER JOIN `tabCNTEMAD Student` s ON p.student = s.name
        WHERE s.center = %s
        AND p.status = 'Pending'
        AND p.creation < DATE_SUB(NOW(), INTERVAL 24 HOUR)
    """, center_id, as_dict=True)[0]

    if old_pending["count"] > 0:
        alerts.append({
            "type": "warning",
            "title": "Paiements en attente",
            "message": f"{old_pending['count']} paiement(s) en attente depuis plus de 24h",
            "action": "/admin/payments?status=pending",
        })

    # Inactive students (no activity in 7 days)
    inactive = frappe.db.sql("""
        SELECT COUNT(DISTINCT s.name) as count
        FROM `tabCNTEMAD Student` s
        LEFT JOIN `tabCNTEMAD Enrollment` e ON e.student = s.name
        WHERE s.center = %s
        AND s.status = 'Active'
        AND (e.modified < DATE_SUB(NOW(), INTERVAL 7 DAY) OR e.modified IS NULL)
    """, center_id, as_dict=True)[0]

    if inactive["count"] > 0:
        alerts.append({
            "type": "info",
            "title": "Étudiants inactifs",
            "message": f"{inactive['count']} étudiant(s) sans activité depuis 7 jours",
            "action": "/admin/students?status=inactive",
        })

    return alerts


def get_recent_activity(center_id: str, limit: int = 10) -> list:
    """Get recent activity for a center."""
    # Recent payments
    payments = frappe.db.sql("""
        SELECT
            'payment' as type,
            p.name as id,
            s.full_name as student_name,
            p.amount,
            p.status,
            p.creation as date
        FROM `tabCNTEMAD Payment` p
        INNER JOIN `tabCNTEMAD Student` s ON p.student = s.name
        WHERE s.center = %s
        ORDER BY p.creation DESC
        LIMIT %s
    """, (center_id, limit), as_dict=True)

    # Recent validations
    validations = frappe.db.sql("""
        SELECT
            'validation' as type,
            e.name as id,
            s.full_name as student_name,
            ec.title as ec_title,
            e.validation_date as date
        FROM `tabCNTEMAD Enrollment` e
        INNER JOIN `tabCNTEMAD Student` s ON e.student = s.name
        INNER JOIN `tabCNTEMAD EC` ec ON e.ec = ec.name
        WHERE s.center = %s
        AND e.status = 'Validated'
        AND e.validation_date IS NOT NULL
        ORDER BY e.validation_date DESC
        LIMIT %s
    """, (center_id, limit), as_dict=True)

    # Merge and sort
    activity = list(payments) + list(validations)
    activity.sort(key=lambda x: x["date"] or "", reverse=True)

    return activity[:limit]


@frappe.whitelist()
def get_center_students(
    center_id: str = None,
    status: str = None,
    year: str = None,
    search: str = None,
    limit: int = 20,
    offset: int = 0
) -> dict:
    """
    Get students for a center with filters.

    Returns:
        dict: { students: [], total: int }
    """
    if not center_id:
        my_center = get_my_center()
        if not my_center:
            frappe.throw(_("Aucun centre associé"))
        center_id = my_center["name"]

    filters = {"center": center_id}

    if status:
        filters["status"] = status

    if year:
        filters["current_year"] = year

    # Base query
    students = frappe.get_all(
        "CNTEMAD Student",
        filters=filters,
        fields=[
            "name", "full_name", "email", "phone",
            "current_year", "status", "creation", "modified"
        ],
        order_by="full_name asc",
        limit_page_length=cint(limit),
        limit_start=cint(offset),
    )

    # Search filter
    if search:
        search_lower = search.lower()
        students = [
            s for s in students
            if search_lower in (s.full_name or "").lower()
            or search_lower in (s.email or "").lower()
            or search_lower in (s.name or "").lower()
        ]

    # Add enrollment stats for each student
    for student in students:
        enrollment_stats = frappe.db.sql("""
            SELECT
                COUNT(*) as total,
                SUM(CASE WHEN status = 'Validated' THEN 1 ELSE 0 END) as validated
            FROM `tabCNTEMAD Enrollment`
            WHERE student = %s
        """, student.name, as_dict=True)[0]

        student["total_ecs"] = enrollment_stats["total"]
        student["validated_ecs"] = enrollment_stats["validated"]
        student["progress"] = round(
            (enrollment_stats["validated"] / enrollment_stats["total"] * 100)
            if enrollment_stats["total"] > 0 else 0
        )

    total = frappe.db.count("CNTEMAD Student", filters)

    return {
        "students": students,
        "total": total,
    }


@frappe.whitelist()
def get_center_payments(
    center_id: str = None,
    status: str = None,
    provider: str = None,
    date_from: str = None,
    date_to: str = None,
    search: str = None,
    limit: int = 20,
    offset: int = 0
) -> dict:
    """
    Get payments for a center with filters.

    Returns:
        dict: { payments: [], total: int, stats: {} }
    """
    if not center_id:
        my_center = get_my_center()
        if not my_center:
            frappe.throw(_("Aucun centre associé"))
        center_id = my_center["name"]

    # Build query
    conditions = ["s.center = %s"]
    values = [center_id]

    if status:
        conditions.append("p.status = %s")
        values.append(status)

    if provider:
        conditions.append("p.provider = %s")
        values.append(provider)

    if date_from:
        conditions.append("p.creation >= %s")
        values.append(date_from)

    if date_to:
        conditions.append("p.creation <= %s")
        values.append(date_to)

    where_clause = " AND ".join(conditions)

    # Get payments
    payments = frappe.db.sql(f"""
        SELECT
            p.name,
            p.student,
            s.full_name as student_name,
            p.ec,
            ec.title as ec_title,
            p.amount,
            p.provider,
            p.status,
            p.creation,
            p.completed_at,
            p.failure_reason
        FROM `tabCNTEMAD Payment` p
        INNER JOIN `tabCNTEMAD Student` s ON p.student = s.name
        LEFT JOIN `tabCNTEMAD EC` ec ON p.ec = ec.name
        WHERE {where_clause}
        ORDER BY p.creation DESC
        LIMIT %s OFFSET %s
    """, values + [cint(limit), cint(offset)], as_dict=True)

    # Search filter
    if search:
        search_lower = search.lower()
        payments = [
            p for p in payments
            if search_lower in (p.student_name or "").lower()
            or search_lower in (p.name or "").lower()
            or search_lower in (p.ec_title or "").lower()
        ]

    # Get total
    total = frappe.db.sql(f"""
        SELECT COUNT(*) as count
        FROM `tabCNTEMAD Payment` p
        INNER JOIN `tabCNTEMAD Student` s ON p.student = s.name
        WHERE {where_clause}
    """, values, as_dict=True)[0]["count"]

    # Get stats
    stats = frappe.db.sql(f"""
        SELECT
            p.status,
            COUNT(*) as count,
            COALESCE(SUM(p.amount), 0) as total
        FROM `tabCNTEMAD Payment` p
        INNER JOIN `tabCNTEMAD Student` s ON p.student = s.name
        WHERE s.center = %s
        GROUP BY p.status
    """, center_id, as_dict=True)

    return {
        "payments": payments,
        "total": total,
        "stats": {s["status"]: {"count": s["count"], "total": s["total"]} for s in stats},
    }


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


@frappe.whitelist()
def export_students(center_id: str = None, format: str = "csv") -> dict:
    """
    Export students list for a center.

    Returns:
        dict: { url: download_url } or { data: csv_content }
    """
    if not center_id:
        my_center = get_my_center()
        if not my_center:
            frappe.throw(_("Aucun centre associé"))
        center_id = my_center["name"]

    students = frappe.db.sql("""
        SELECT
            s.name as id,
            s.full_name,
            s.email,
            s.phone,
            s.current_year,
            s.status,
            s.creation as inscription_date,
            COUNT(e.name) as total_ecs,
            SUM(CASE WHEN e.status = 'Validated' THEN 1 ELSE 0 END) as validated_ecs
        FROM `tabCNTEMAD Student` s
        LEFT JOIN `tabCNTEMAD Enrollment` e ON e.student = s.name
        WHERE s.center = %s
        GROUP BY s.name
        ORDER BY s.full_name
    """, center_id, as_dict=True)

    if format == "csv":
        import csv
        import io

        output = io.StringIO()
        writer = csv.writer(output)

        # Header
        writer.writerow([
            "ID", "Nom complet", "Email", "Téléphone",
            "Année", "Statut", "Date inscription",
            "Total EC", "EC validés"
        ])

        # Data
        for s in students:
            writer.writerow([
                s.id, s.full_name, s.email, s.phone,
                s.current_year, s.status, s.inscription_date,
                s.total_ecs, s.validated_ecs
            ])

        return {"data": output.getvalue(), "filename": f"etudiants_{center_id}.csv"}

    return {"students": students}
