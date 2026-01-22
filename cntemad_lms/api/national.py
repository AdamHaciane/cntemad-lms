"""API endpoints for National Admin operations (CNTEMAD central)."""

import frappe
from frappe import _
import json
from datetime import datetime, timedelta


@frappe.whitelist()
def get_national_dashboard() -> dict:
    """
    Get national dashboard with aggregated KPIs from all 34 centers.

    Returns:
        dict: {
            kpis: Global KPIs,
            centers_summary: Summary by center,
            trends: National trends,
            alerts: System-wide alerts,
            top_centers: Best performing centers,
            recent_activity: Recent national activity
        }
    """
    # Global KPIs
    kpis = get_national_kpis()

    # Centers summary
    centers_summary = get_centers_summary()

    # Trends (6 months)
    trends = get_national_trends()

    # Alerts
    alerts = get_national_alerts()

    # Top performing centers
    top_centers = get_top_centers(limit=5)

    # Recent activity
    recent_activity = get_recent_national_activity(limit=10)

    return {
        "kpis": kpis,
        "centers_summary": centers_summary,
        "trends": trends,
        "alerts": alerts,
        "top_centers": top_centers,
        "recent_activity": recent_activity
    }


def get_national_kpis() -> dict:
    """Calculate national KPIs across all centers."""
    # Total students
    total_students = frappe.db.count("CNTEMAD Student")

    # Active students (with at least one enrollment in last 30 days)
    thirty_days_ago = datetime.now() - timedelta(days=30)
    active_students = frappe.db.sql("""
        SELECT COUNT(DISTINCT student)
        FROM `tabCNTEMAD Enrollment`
        WHERE modified >= %s
    """, [thirty_days_ago])[0][0] or 0

    # Total centers
    total_centers = frappe.db.count("CNTEMAD Center")

    # Total ECs
    total_ecs = frappe.db.count("CNTEMAD EC")
    published_ecs = frappe.db.count("CNTEMAD EC", {"is_published": 1})

    # Total courses
    total_courses = frappe.db.count("CNTEMAD Course")

    # Enrollments
    total_enrollments = frappe.db.count("CNTEMAD Enrollment")
    validated_enrollments = frappe.db.count("CNTEMAD Enrollment", {"status": "Validated"})

    # Payments this month
    month_start = datetime.now().replace(day=1, hour=0, minute=0, second=0)
    payments_this_month = frappe.db.count(
        "CNTEMAD Payment",
        {"status": "Success", "creation": [">=", month_start]}
    )

    revenue_this_month = frappe.db.sql("""
        SELECT COALESCE(SUM(amount), 0)
        FROM `tabCNTEMAD Payment`
        WHERE status = 'Success' AND creation >= %s
    """, [month_start])[0][0] or 0

    # Total revenue
    total_revenue = frappe.db.sql("""
        SELECT COALESCE(SUM(amount), 0)
        FROM `tabCNTEMAD Payment`
        WHERE status = 'Success'
    """)[0][0] or 0

    # Validation rate
    validation_rate = round((validated_enrollments / total_enrollments) * 100, 1) if total_enrollments > 0 else 0

    return {
        "total_students": total_students,
        "active_students": active_students,
        "total_centers": total_centers,
        "total_ecs": total_ecs,
        "published_ecs": published_ecs,
        "total_courses": total_courses,
        "total_enrollments": total_enrollments,
        "validated_enrollments": validated_enrollments,
        "validation_rate": validation_rate,
        "payments_this_month": payments_this_month,
        "revenue_this_month": revenue_this_month,
        "total_revenue": total_revenue
    }


def get_centers_summary() -> list:
    """Get summary data for all centers."""
    centers = frappe.get_all(
        "CNTEMAD Center",
        fields=["name", "center_name", "region", "latitude", "longitude"],
        order_by="center_name asc"
    )

    for center in centers:
        # Student count
        center["student_count"] = frappe.db.count(
            "CNTEMAD Student",
            {"center": center.name}
        )

        # Payment stats
        payment_data = frappe.db.sql("""
            SELECT
                COUNT(*) as count,
                COALESCE(SUM(amount), 0) as total
            FROM `tabCNTEMAD Payment`
            WHERE center = %s AND status = 'Success'
        """, [center.name], as_dict=True)[0]

        center["payment_count"] = payment_data.get("count", 0)
        center["revenue"] = payment_data.get("total", 0)

        # Validation rate
        enrollments = frappe.db.sql("""
            SELECT
                COUNT(*) as total,
                SUM(CASE WHEN status = 'Validated' THEN 1 ELSE 0 END) as validated
            FROM `tabCNTEMAD Enrollment` e
            JOIN `tabCNTEMAD Student` s ON e.student = s.name
            WHERE s.center = %s
        """, [center.name], as_dict=True)[0]

        total = enrollments.get("total", 0) or 0
        validated = enrollments.get("validated", 0) or 0
        center["validation_rate"] = round((validated / total) * 100, 1) if total > 0 else 0

    return centers


def get_national_trends() -> list:
    """Get national enrollment trends over 6 months."""
    trends = []

    for i in range(5, -1, -1):
        date = datetime.now() - timedelta(days=i * 30)
        month_start = date.replace(day=1, hour=0, minute=0, second=0)

        if i > 0:
            next_month = (date + timedelta(days=32)).replace(day=1)
        else:
            next_month = datetime.now() + timedelta(days=1)

        # Enrollments
        enrollments = frappe.db.sql("""
            SELECT COUNT(*)
            FROM `tabCNTEMAD Enrollment`
            WHERE creation >= %s AND creation < %s
        """, [month_start, next_month])[0][0] or 0

        # Payments
        payments = frappe.db.sql("""
            SELECT COUNT(*), COALESCE(SUM(amount), 0)
            FROM `tabCNTEMAD Payment`
            WHERE status = 'Success' AND creation >= %s AND creation < %s
        """, [month_start, next_month])

        payment_count = payments[0][0] or 0
        revenue = payments[0][1] or 0

        # New students
        new_students = frappe.db.sql("""
            SELECT COUNT(*)
            FROM `tabCNTEMAD Student`
            WHERE creation >= %s AND creation < %s
        """, [month_start, next_month])[0][0] or 0

        trends.append({
            "month": month_start.strftime("%b %Y"),
            "month_short": month_start.strftime("%b"),
            "enrollments": enrollments,
            "payments": payment_count,
            "revenue": revenue,
            "new_students": new_students
        })

    return trends


def get_national_alerts() -> list:
    """Get system-wide alerts."""
    alerts = []

    # Centers with low activity
    thirty_days_ago = datetime.now() - timedelta(days=30)
    inactive_centers = frappe.db.sql("""
        SELECT c.name, c.center_name
        FROM `tabCNTEMAD Center` c
        WHERE NOT EXISTS (
            SELECT 1 FROM `tabCNTEMAD Payment` p
            WHERE p.center = c.name
            AND p.creation >= %s
        )
    """, [thirty_days_ago], as_dict=True)

    for center in inactive_centers[:3]:
        alerts.append({
            "id": f"inactive-{center.name}",
            "level": "warning",
            "message": f"Centre {center.center_name}: aucun paiement depuis 30 jours",
            "center": center.name
        })

    # Pending payments
    pending_payments = frappe.db.count("CNTEMAD Payment", {"status": "Pending"})
    if pending_payments > 10:
        alerts.append({
            "id": "pending-payments",
            "level": "warning",
            "message": f"{pending_payments} paiements en attente de confirmation"
        })

    # Failed payments today
    today = datetime.now().replace(hour=0, minute=0, second=0)
    failed_today = frappe.db.count(
        "CNTEMAD Payment",
        {"status": "Failed", "creation": [">=", today]}
    )
    if failed_today > 5:
        alerts.append({
            "id": "failed-payments",
            "level": "error",
            "message": f"{failed_today} paiements échoués aujourd'hui"
        })

    # Low validation rate centers
    low_validation = frappe.db.sql("""
        SELECT c.name, c.center_name,
            COUNT(e.name) as total,
            SUM(CASE WHEN e.status = 'Validated' THEN 1 ELSE 0 END) as validated
        FROM `tabCNTEMAD Center` c
        JOIN `tabCNTEMAD Student` s ON s.center = c.name
        JOIN `tabCNTEMAD Enrollment` e ON e.student = s.name
        GROUP BY c.name
        HAVING total > 10 AND (validated / total) < 0.3
    """, as_dict=True)

    for center in low_validation[:2]:
        rate = round((center.validated / center.total) * 100, 1)
        alerts.append({
            "id": f"low-validation-{center.name}",
            "level": "warning",
            "message": f"Centre {center.center_name}: taux de validation bas ({rate}%)",
            "center": center.name
        })

    return alerts[:5]


def get_top_centers(limit: int = 5) -> list:
    """Get top performing centers by various metrics."""
    centers = frappe.db.sql("""
        SELECT
            c.name,
            c.center_name,
            c.region,
            COUNT(DISTINCT s.name) as student_count,
            COALESCE(SUM(p.amount), 0) as revenue
        FROM `tabCNTEMAD Center` c
        LEFT JOIN `tabCNTEMAD Student` s ON s.center = c.name
        LEFT JOIN `tabCNTEMAD Payment` p ON p.center = c.name AND p.status = 'Success'
        GROUP BY c.name
        ORDER BY revenue DESC
        LIMIT %s
    """, [limit], as_dict=True)

    return centers


def get_recent_national_activity(limit: int = 10) -> list:
    """Get recent activity across all centers."""
    activities = []

    # Recent enrollments
    enrollments = frappe.get_all(
        "CNTEMAD Enrollment",
        fields=["name", "student", "ec", "creation"],
        order_by="creation desc",
        limit=5
    )

    for e in enrollments:
        student = frappe.db.get_value("CNTEMAD Student", e.student, ["full_name", "center"])
        ec_title = frappe.db.get_value("CNTEMAD EC", e.ec, "title")
        center_name = frappe.db.get_value("CNTEMAD Center", student[1], "center_name") if student else None

        activities.append({
            "id": f"enrollment-{e.name}",
            "type": "enrollment",
            "description": f"{student[0] if student else 'Étudiant'} inscrit à {ec_title or 'EC'}",
            "center": center_name,
            "time": e.creation.strftime("%d/%m %H:%M") if e.creation else ""
        })

    # Recent payments
    payments = frappe.get_all(
        "CNTEMAD Payment",
        filters={"status": "Success"},
        fields=["name", "student", "amount", "center", "creation"],
        order_by="creation desc",
        limit=5
    )

    for p in payments:
        student_name = frappe.db.get_value("CNTEMAD Student", p.student, "full_name")
        center_name = frappe.db.get_value("CNTEMAD Center", p.center, "center_name")

        activities.append({
            "id": f"payment-{p.name}",
            "type": "payment",
            "description": f"Paiement {p.amount:,.0f} Ar de {student_name or 'Étudiant'}",
            "center": center_name,
            "time": p.creation.strftime("%d/%m %H:%M") if p.creation else ""
        })

    # Sort by time and limit
    activities.sort(key=lambda x: x.get("time", ""), reverse=True)
    return activities[:limit]


@frappe.whitelist()
def get_all_centers() -> dict:
    """
    Get all centers with detailed stats.

    Returns:
        dict: { centers: [], total: int }
    """
    centers = get_centers_summary()

    return {
        "centers": centers,
        "total": len(centers)
    }


@frappe.whitelist()
def get_center_detail(center_id: str) -> dict:
    """
    Get detailed information for a specific center.

    Args:
        center_id: Center identifier

    Returns:
        dict: Center details with stats
    """
    if not frappe.db.exists("CNTEMAD Center", center_id):
        frappe.throw(_("Centre non trouvé"), frappe.DoesNotExistError)

    center = frappe.get_doc("CNTEMAD Center", center_id)

    # Get stats
    student_count = frappe.db.count("CNTEMAD Student", {"center": center_id})

    # Enrollments by status
    enrollment_stats = frappe.db.sql("""
        SELECT status, COUNT(*) as count
        FROM `tabCNTEMAD Enrollment` e
        JOIN `tabCNTEMAD Student` s ON e.student = s.name
        WHERE s.center = %s
        GROUP BY status
    """, [center_id], as_dict=True)

    # Payments
    payment_stats = frappe.db.sql("""
        SELECT
            COUNT(*) as total_payments,
            COALESCE(SUM(amount), 0) as total_revenue,
            COALESCE(SUM(CASE WHEN creation >= %s THEN amount ELSE 0 END), 0) as revenue_this_month
        FROM `tabCNTEMAD Payment`
        WHERE center = %s AND status = 'Success'
    """, [datetime.now().replace(day=1), center_id], as_dict=True)[0]

    # Monthly trends
    trends = []
    for i in range(5, -1, -1):
        date = datetime.now() - timedelta(days=i * 30)
        month_start = date.replace(day=1)
        if i > 0:
            next_month = (date + timedelta(days=32)).replace(day=1)
        else:
            next_month = datetime.now() + timedelta(days=1)

        count = frappe.db.sql("""
            SELECT COUNT(*)
            FROM `tabCNTEMAD Student`
            WHERE center = %s AND creation >= %s AND creation < %s
        """, [center_id, month_start, next_month])[0][0] or 0

        trends.append({
            "month": month_start.strftime("%b"),
            "count": count
        })

    return {
        "name": center.name,
        "center_name": center.center_name,
        "region": center.region,
        "address": center.get("address"),
        "phone": center.get("phone"),
        "email": center.get("email"),
        "latitude": center.get("latitude"),
        "longitude": center.get("longitude"),
        "stats": {
            "student_count": student_count,
            "enrollments": {s.status: s.count for s in enrollment_stats},
            "payments": payment_stats
        },
        "trends": trends
    }


@frappe.whitelist()
def compare_centers(center_ids: str = None) -> dict:
    """
    Compare multiple centers side by side.

    Args:
        center_ids: JSON array of center IDs

    Returns:
        dict: Comparison data
    """
    ids = json.loads(center_ids) if center_ids else []

    if not ids:
        frappe.throw(_("Sélectionnez au moins un centre"))

    comparisons = []

    for center_id in ids:
        if not frappe.db.exists("CNTEMAD Center", center_id):
            continue

        center = frappe.db.get_value(
            "CNTEMAD Center", center_id,
            ["name", "center_name", "region"],
            as_dict=True
        )

        # Stats
        student_count = frappe.db.count("CNTEMAD Student", {"center": center_id})

        enrollment_data = frappe.db.sql("""
            SELECT
                COUNT(*) as total,
                SUM(CASE WHEN status = 'Validated' THEN 1 ELSE 0 END) as validated
            FROM `tabCNTEMAD Enrollment` e
            JOIN `tabCNTEMAD Student` s ON e.student = s.name
            WHERE s.center = %s
        """, [center_id], as_dict=True)[0]

        payment_data = frappe.db.sql("""
            SELECT
                COUNT(*) as count,
                COALESCE(SUM(amount), 0) as total
            FROM `tabCNTEMAD Payment`
            WHERE center = %s AND status = 'Success'
        """, [center_id], as_dict=True)[0]

        total_enrollments = enrollment_data.get("total", 0) or 0
        validated = enrollment_data.get("validated", 0) or 0

        comparisons.append({
            "name": center.name,
            "center_name": center.center_name,
            "region": center.region,
            "student_count": student_count,
            "total_enrollments": total_enrollments,
            "validated_enrollments": validated,
            "validation_rate": round((validated / total_enrollments) * 100, 1) if total_enrollments > 0 else 0,
            "payment_count": payment_data.get("count", 0),
            "revenue": payment_data.get("total", 0)
        })

    # Sort by revenue
    comparisons.sort(key=lambda x: x["revenue"], reverse=True)

    return {
        "comparisons": comparisons,
        "metrics": ["student_count", "total_enrollments", "validation_rate", "revenue"]
    }


@frappe.whitelist()
def export_national_report(
    report_type: str = "summary",
    date_from: str = None,
    date_to: str = None,
    format: str = "csv"
) -> dict:
    """
    Export national reports.

    Args:
        report_type: Type of report (summary, students, payments, centers)
        date_from: Start date filter
        date_to: End date filter
        format: Export format (csv, xlsx)

    Returns:
        dict: { data: str, filename: str }
    """
    import csv
    from io import StringIO

    output = StringIO()
    writer = csv.writer(output)

    filename = f"cntemad_{report_type}_{datetime.now().strftime('%Y%m%d')}.csv"

    if report_type == "summary":
        # National summary report
        writer.writerow(["Rapport National CNTEMAD", datetime.now().strftime("%d/%m/%Y")])
        writer.writerow([])

        kpis = get_national_kpis()
        writer.writerow(["Indicateur", "Valeur"])
        writer.writerow(["Total étudiants", kpis["total_students"]])
        writer.writerow(["Étudiants actifs", kpis["active_students"]])
        writer.writerow(["Total centres", kpis["total_centers"]])
        writer.writerow(["Total EC", kpis["total_ecs"]])
        writer.writerow(["Inscriptions totales", kpis["total_enrollments"]])
        writer.writerow(["Inscriptions validées", kpis["validated_enrollments"]])
        writer.writerow(["Taux de validation", f"{kpis['validation_rate']}%"])
        writer.writerow(["Revenus ce mois", f"{kpis['revenue_this_month']:,.0f} Ar"])
        writer.writerow(["Revenus totaux", f"{kpis['total_revenue']:,.0f} Ar"])

    elif report_type == "centers":
        # Centers report
        writer.writerow([
            "Centre", "Région", "Étudiants", "Paiements",
            "Revenus (Ar)", "Taux validation (%)"
        ])

        centers = get_centers_summary()
        for c in centers:
            writer.writerow([
                c["center_name"],
                c["region"],
                c["student_count"],
                c["payment_count"],
                c["revenue"],
                c["validation_rate"]
            ])

    elif report_type == "students":
        # Students report
        filters = {}
        if date_from:
            filters["creation"] = [">=", date_from]

        students = frappe.get_all(
            "CNTEMAD Student",
            filters=filters,
            fields=["student_id", "full_name", "email", "phone", "center", "year", "creation"],
            order_by="creation desc",
            limit=10000
        )

        writer.writerow([
            "ID", "Nom complet", "Email", "Téléphone",
            "Centre", "Année", "Date inscription"
        ])

        for s in students:
            center_name = frappe.db.get_value("CNTEMAD Center", s.center, "center_name") if s.center else ""
            writer.writerow([
                s.student_id,
                s.full_name,
                s.email,
                s.phone,
                center_name,
                s.year,
                s.creation.strftime("%d/%m/%Y") if s.creation else ""
            ])

    elif report_type == "payments":
        # Payments report
        filters = {"status": "Success"}
        if date_from:
            filters["creation"] = [">=", date_from]
        if date_to:
            if "creation" in filters:
                filters["creation"] = ["between", [date_from, date_to]]
            else:
                filters["creation"] = ["<=", date_to]

        payments = frappe.get_all(
            "CNTEMAD Payment",
            filters=filters,
            fields=["reference", "student", "amount", "provider", "center", "creation"],
            order_by="creation desc",
            limit=10000
        )

        writer.writerow([
            "Référence", "Étudiant", "Montant (Ar)", "Provider",
            "Centre", "Date"
        ])

        for p in payments:
            student_name = frappe.db.get_value("CNTEMAD Student", p.student, "full_name") if p.student else ""
            center_name = frappe.db.get_value("CNTEMAD Center", p.center, "center_name") if p.center else ""
            writer.writerow([
                p.reference,
                student_name,
                p.amount,
                p.provider,
                center_name,
                p.creation.strftime("%d/%m/%Y %H:%M") if p.creation else ""
            ])

    return {
        "data": output.getvalue(),
        "filename": filename
    }


@frappe.whitelist()
def get_centers_map_data() -> dict:
    """
    Get center data formatted for map display.

    Returns:
        dict: { centers: [...], bounds: {...} }
    """
    centers = frappe.get_all(
        "CNTEMAD Center",
        fields=["name", "center_name", "region", "latitude", "longitude"],
        filters=[["latitude", "is", "set"], ["longitude", "is", "set"]]
    )

    # Add stats for each center
    for center in centers:
        center["student_count"] = frappe.db.count(
            "CNTEMAD Student",
            {"center": center.name}
        )

        revenue = frappe.db.sql("""
            SELECT COALESCE(SUM(amount), 0)
            FROM `tabCNTEMAD Payment`
            WHERE center = %s AND status = 'Success'
        """, [center.name])[0][0] or 0

        center["revenue"] = revenue

    # Calculate bounds
    if centers:
        lats = [c["latitude"] for c in centers if c.get("latitude")]
        lngs = [c["longitude"] for c in centers if c.get("longitude")]

        bounds = {
            "north": max(lats) if lats else -18.0,
            "south": min(lats) if lats else -26.0,
            "east": max(lngs) if lngs else 50.5,
            "west": min(lngs) if lngs else 43.0
        }
    else:
        # Default Madagascar bounds
        bounds = {
            "north": -11.95,
            "south": -25.60,
            "east": 50.48,
            "west": 43.18
        }

    return {
        "centers": centers,
        "bounds": bounds
    }
