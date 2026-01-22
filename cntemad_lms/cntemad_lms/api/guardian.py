"""
API endpoints pour les parents/tuteurs.
Suivi des enfants, progression, paiements.
"""
import frappe
from frappe import _


@frappe.whitelist()
def get_guardian_dashboard():
    """
    Récupère le dashboard du parent/tuteur connecté.

    Returns:
        dict: {
            guardian: profil parent,
            children: liste des enfants,
            stats: statistiques globales,
            recent_activity: activité récente,
            notifications: notifications non lues
        }
    """
    user = frappe.session.user

    # Profil parent simulé
    guardian = {
        "user": user,
        "full_name": frappe.db.get_value("User", user, "full_name") or user,
        "email": user,
        "phone": "034 12 345 67",
    }

    # Enfants simulés
    children = [
        {
            "id": "STU-001",
            "name": "Jean Rakoto",
            "year": "L2",
            "center": "Antananarivo",
            "progress": 75,
            "validated_ecs": 8,
            "total_ecs": 12,
            "average": 14.5,
            "last_activity": "2026-01-20",
            "status": "active",
            "photo": None,
        },
        {
            "id": "STU-006",
            "name": "Marie Rakoto",
            "year": "L1",
            "center": "Antananarivo",
            "progress": 40,
            "validated_ecs": 5,
            "total_ecs": 12,
            "average": 12.0,
            "last_activity": "2026-01-22",
            "status": "active",
            "photo": None,
        },
    ]

    # Stats globales
    stats = {
        "total_children": len(children),
        "total_validated_ecs": sum(c["validated_ecs"] for c in children),
        "total_payments": 450000,
        "avg_progress": sum(c["progress"] for c in children) / len(children) if children else 0,
    }

    # Activité récente
    recent_activity = [
        {
            "type": "ec_validated",
            "child_name": "Jean Rakoto",
            "description": "A validé l'EC Algorithmique (16/20)",
            "timestamp": "2026-01-20 14:30",
        },
        {
            "type": "payment",
            "child_name": "Marie Rakoto",
            "description": "Paiement EC Mathématiques confirmé",
            "timestamp": "2026-01-19 10:00",
        },
        {
            "type": "quiz",
            "child_name": "Jean Rakoto",
            "description": "Quiz réussi Base de données (14/20)",
            "timestamp": "2026-01-18 16:45",
        },
    ]

    # Notifications
    notifications = [
        {
            "id": "notif-1",
            "type": "success",
            "title": "EC validé",
            "message": "Jean a validé l'EC Algorithmique",
            "read": False,
            "created_at": "2026-01-20",
        },
        {
            "id": "notif-2",
            "type": "info",
            "title": "Paiement confirmé",
            "message": "Paiement de 75 000 Ar confirmé pour Marie",
            "read": True,
            "created_at": "2026-01-19",
        },
    ]

    return {
        "guardian": guardian,
        "children": children,
        "stats": stats,
        "recent_activity": recent_activity,
        "notifications": notifications,
    }


@frappe.whitelist()
def get_my_children():
    """
    Récupère la liste des enfants du parent connecté.

    Returns:
        list: Liste des enfants avec progression
    """
    # Données simulées
    children = [
        {
            "id": "STU-001",
            "name": "Jean Rakoto",
            "email": "jean.rakoto@email.mg",
            "phone": "034 12 345 67",
            "year": "L2",
            "center": "Antananarivo",
            "progress": 75,
            "validated_ecs": 8,
            "total_ecs": 12,
            "average": 14.5,
            "last_activity": "2026-01-20",
            "days_inactive": 2,
            "status": "active",
            "enrolled_since": "2025-09-01",
        },
        {
            "id": "STU-006",
            "name": "Marie Rakoto",
            "email": "marie.rakoto@email.mg",
            "phone": "032 98 765 43",
            "year": "L1",
            "center": "Antananarivo",
            "progress": 40,
            "validated_ecs": 5,
            "total_ecs": 12,
            "average": 12.0,
            "last_activity": "2026-01-22",
            "days_inactive": 0,
            "status": "active",
            "enrolled_since": "2025-09-01",
        },
    ]

    return children


@frappe.whitelist()
def get_child_progress(student_id):
    """
    Récupère la progression détaillée d'un enfant.

    Args:
        student_id: ID de l'étudiant

    Returns:
        dict: Progression complète avec EC et historique
    """
    if not student_id:
        frappe.throw(_("ID étudiant requis"))

    # Données simulées
    student = {
        "id": student_id,
        "name": "Jean Rakoto",
        "email": "jean.rakoto@email.mg",
        "phone": "034 12 345 67",
        "year": "L2",
        "center": "Antananarivo",
        "enrolled_since": "2025-09-01",
    }

    progress = {
        "overall": 75,
        "validated_ecs": 8,
        "total_ecs": 12,
        "average": 14.5,
        "rank": 15,
        "total_students": 120,
    }

    # EC avec statut
    ecs = [
        {"id": "EC-001", "title": "Algorithmique", "status": "validated", "grade": 16, "validated_at": "2026-01-15", "price": 75000},
        {"id": "EC-002", "title": "Programmation Python", "status": "validated", "grade": 18, "validated_at": "2026-01-10", "price": 75000},
        {"id": "EC-003", "title": "Base de données", "status": "validated", "grade": 14, "validated_at": "2026-01-05", "price": 75000},
        {"id": "EC-004", "title": "Réseaux", "status": "in_progress", "grade": None, "progress": 60, "price": 75000, "paid": True},
        {"id": "EC-005", "title": "Systèmes d'exploitation", "status": "not_started", "grade": None, "progress": 0, "price": 75000, "paid": False},
    ]

    # Tendance sur 6 mois
    trend = [
        {"month": "Août", "progress": 10},
        {"month": "Sept", "progress": 25},
        {"month": "Oct", "progress": 40},
        {"month": "Nov", "progress": 55},
        {"month": "Déc", "progress": 65},
        {"month": "Jan", "progress": 75},
    ]

    # Historique notes
    grades_history = [
        {"ec": "Algorithmique", "grade": 16, "date": "2026-01-15"},
        {"ec": "Programmation Python", "grade": 18, "date": "2026-01-10"},
        {"ec": "Base de données", "grade": 14, "date": "2026-01-05"},
    ]

    return {
        "student": student,
        "progress": progress,
        "ecs": ecs,
        "trend": trend,
        "grades_history": grades_history,
    }


@frappe.whitelist()
def get_child_payments(student_id):
    """
    Récupère l'historique des paiements pour un enfant.

    Args:
        student_id: ID de l'étudiant

    Returns:
        list: Historique des paiements
    """
    if not student_id:
        frappe.throw(_("ID étudiant requis"))

    payments = [
        {
            "id": "PAY-001",
            "ec_title": "Algorithmique",
            "amount": 75000,
            "provider": "mvola",
            "status": "completed",
            "paid_at": "2025-10-15 10:30",
            "transaction_ref": "MVL123456",
        },
        {
            "id": "PAY-002",
            "ec_title": "Programmation Python",
            "amount": 75000,
            "provider": "orange_money",
            "status": "completed",
            "paid_at": "2025-10-20 14:00",
            "transaction_ref": "ORG789012",
        },
        {
            "id": "PAY-003",
            "ec_title": "Base de données",
            "amount": 75000,
            "provider": "mvola",
            "status": "completed",
            "paid_at": "2025-11-05 09:15",
            "transaction_ref": "MVL345678",
        },
        {
            "id": "PAY-004",
            "ec_title": "Réseaux",
            "amount": 75000,
            "provider": "airtel_money",
            "status": "completed",
            "paid_at": "2026-01-10 11:00",
            "transaction_ref": "AIR901234",
        },
    ]

    return payments


@frappe.whitelist()
def get_unpaid_ecs(student_id):
    """
    Récupère la liste des EC non payés pour un enfant.

    Args:
        student_id: ID de l'étudiant

    Returns:
        list: EC disponibles non payés
    """
    if not student_id:
        frappe.throw(_("ID étudiant requis"))

    unpaid_ecs = [
        {
            "id": "EC-005",
            "title": "Systèmes d'exploitation",
            "description": "Introduction aux systèmes d'exploitation",
            "price": 75000,
            "duration": "30 heures",
            "lessons": 10,
        },
        {
            "id": "EC-006",
            "title": "Développement Web",
            "description": "HTML, CSS, JavaScript",
            "price": 75000,
            "duration": "40 heures",
            "lessons": 12,
        },
        {
            "id": "EC-007",
            "title": "Gestion de projet",
            "description": "Méthodes agiles et traditionnelles",
            "price": 75000,
            "duration": "25 heures",
            "lessons": 8,
        },
    ]

    return unpaid_ecs


@frappe.whitelist()
def initiate_payment_for_child(student_id, ec_id, provider, phone_number):
    """
    Initie un paiement pour un enfant.

    Args:
        student_id: ID de l'étudiant
        ec_id: ID de l'EC à payer
        provider: Provider de paiement (mvola, orange_money, airtel_money)
        phone_number: Numéro de téléphone pour le paiement

    Returns:
        dict: Détails du paiement initié
    """
    if not all([student_id, ec_id, provider, phone_number]):
        frappe.throw(_("Tous les champs sont requis"))

    # Valider le provider
    valid_providers = ["mvola", "orange_money", "airtel_money"]
    if provider not in valid_providers:
        frappe.throw(_("Provider invalide"))

    # Simuler la création du paiement
    payment = {
        "id": f"PAY-{frappe.generate_hash(length=6).upper()}",
        "student_id": student_id,
        "ec_id": ec_id,
        "amount": 75000,
        "provider": provider,
        "phone_number": phone_number,
        "status": "pending",
        "created_at": frappe.utils.now(),
    }

    # TODO: Intégrer avec les vraies API de paiement

    return payment


@frappe.whitelist()
def get_notifications(unread_only=False):
    """
    Récupère les notifications du parent.

    Args:
        unread_only: Si True, retourne uniquement les non lues

    Returns:
        list: Liste des notifications
    """
    notifications = [
        {
            "id": "notif-1",
            "type": "success",
            "title": "EC validé",
            "message": "Jean a validé l'EC Algorithmique avec 16/20",
            "child_name": "Jean Rakoto",
            "read": False,
            "created_at": "2026-01-20 14:30",
        },
        {
            "id": "notif-2",
            "type": "info",
            "title": "Paiement confirmé",
            "message": "Paiement de 75 000 Ar confirmé pour l'EC Réseaux",
            "child_name": "Jean Rakoto",
            "read": True,
            "created_at": "2026-01-19 10:00",
        },
        {
            "id": "notif-3",
            "type": "warning",
            "title": "Inactivité détectée",
            "message": "Marie n'a pas été active depuis 5 jours",
            "child_name": "Marie Rakoto",
            "read": False,
            "created_at": "2026-01-18 08:00",
        },
        {
            "id": "notif-4",
            "type": "success",
            "title": "Quiz réussi",
            "message": "Marie a réussi le quiz Mathématiques (13/20)",
            "child_name": "Marie Rakoto",
            "read": True,
            "created_at": "2026-01-17 16:45",
        },
    ]

    if unread_only:
        notifications = [n for n in notifications if not n["read"]]

    return notifications


@frappe.whitelist()
def mark_notification_read(notification_id):
    """
    Marque une notification comme lue.

    Args:
        notification_id: ID de la notification

    Returns:
        dict: Notification mise à jour
    """
    if not notification_id:
        frappe.throw(_("ID notification requis"))

    # TODO: Mettre à jour en base
    return {"id": notification_id, "read": True}


@frappe.whitelist()
def get_payment_summary():
    """
    Récupère le résumé des paiements du parent.

    Returns:
        dict: Statistiques des paiements
    """
    return {
        "total_paid": 450000,
        "this_month": 75000,
        "this_year": 300000,
        "pending_payments": 1,
        "pending_amount": 75000,
        "by_child": [
            {"child_name": "Jean Rakoto", "amount": 300000, "ecs_paid": 4},
            {"child_name": "Marie Rakoto", "amount": 150000, "ecs_paid": 2},
        ],
        "by_provider": [
            {"provider": "mvola", "amount": 225000, "count": 3},
            {"provider": "orange_money", "amount": 150000, "count": 2},
            {"provider": "airtel_money", "amount": 75000, "count": 1},
        ],
    }
