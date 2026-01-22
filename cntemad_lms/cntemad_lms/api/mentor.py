"""
API endpoints pour les mentors.
Gestion des mentorés, suivi progression, messagerie, alertes.
"""
import frappe
from frappe import _


@frappe.whitelist()
def get_mentor_dashboard():
    """
    Récupère le dashboard du mentor connecté.

    Returns:
        dict: {
            mentor: profil mentor,
            stats: statistiques globales,
            mentees: liste des mentorés,
            alerts: alertes actives,
            recent_activity: activité récente
        }
    """
    user = frappe.session.user

    # Simuler données mentor
    mentor = {
        "user": user,
        "full_name": frappe.db.get_value("User", user, "full_name") or user,
        "specialty": "Informatique",
        "since": "2024-01-01",
    }

    # Stats simulées
    stats = {
        "total_mentees": 12,
        "active_mentees": 10,
        "inactive_count": 2,
        "messages_unread": 5,
        "avg_progress": 68.5,
    }

    # Liste mentorés simulée
    mentees = [
        {
            "id": "STU-001",
            "name": "Jean Rakoto",
            "email": "jean.rakoto@email.mg",
            "year": "L2",
            "center": "Antananarivo",
            "progress": 75,
            "validated_ecs": 8,
            "total_ecs": 12,
            "last_activity": "2026-01-20",
            "days_inactive": 2,
            "status": "active",
            "average": 14.5,
        },
        {
            "id": "STU-002",
            "name": "Marie Rabe",
            "email": "marie.rabe@email.mg",
            "year": "L2",
            "center": "Antananarivo",
            "progress": 50,
            "validated_ecs": 6,
            "total_ecs": 12,
            "last_activity": "2026-01-10",
            "days_inactive": 12,
            "status": "inactive",
            "average": 11.2,
        },
        {
            "id": "STU-003",
            "name": "Paul Andria",
            "email": "paul.andria@email.mg",
            "year": "L3",
            "center": "Toamasina",
            "progress": 90,
            "validated_ecs": 11,
            "total_ecs": 12,
            "last_activity": "2026-01-22",
            "days_inactive": 0,
            "status": "active",
            "average": 16.8,
        },
    ]

    # Alertes
    alerts = [
        {
            "id": "alert-1",
            "type": "inactive",
            "student_id": "STU-002",
            "student_name": "Marie Rabe",
            "message": "Inactive depuis 12 jours",
            "severity": "warning",
            "created_at": "2026-01-20",
        },
        {
            "id": "alert-2",
            "type": "low_progress",
            "student_id": "STU-004",
            "student_name": "Luc Razafy",
            "message": "Progression faible (25%)",
            "severity": "danger",
            "created_at": "2026-01-19",
        },
    ]

    # Activité récente
    recent_activity = [
        {
            "type": "ec_validated",
            "student_name": "Paul Andria",
            "description": "A validé l'EC Algorithmique",
            "timestamp": "2026-01-22 14:30",
        },
        {
            "type": "message",
            "student_name": "Jean Rakoto",
            "description": "Nouveau message reçu",
            "timestamp": "2026-01-22 10:15",
        },
        {
            "type": "quiz_passed",
            "student_name": "Paul Andria",
            "description": "Quiz réussi (18/20)",
            "timestamp": "2026-01-21 16:45",
        },
    ]

    return {
        "mentor": mentor,
        "stats": stats,
        "mentees": mentees,
        "alerts": alerts,
        "recent_activity": recent_activity,
    }


@frappe.whitelist()
def get_my_mentees(status=None, year=None):
    """
    Récupère la liste des mentorés du mentor connecté.

    Args:
        status: Filtrer par statut (active, inactive, all)
        year: Filtrer par année (L1, L2, L3, M1, M2)

    Returns:
        list: Liste des mentorés avec progression
    """
    # Données simulées
    mentees = [
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
            "last_activity": "2026-01-20",
            "days_inactive": 2,
            "status": "active",
            "average": 14.5,
            "enrolled_since": "2025-09-01",
        },
        {
            "id": "STU-002",
            "name": "Marie Rabe",
            "email": "marie.rabe@email.mg",
            "phone": "032 98 765 43",
            "year": "L2",
            "center": "Antananarivo",
            "progress": 50,
            "validated_ecs": 6,
            "total_ecs": 12,
            "last_activity": "2026-01-10",
            "days_inactive": 12,
            "status": "inactive",
            "average": 11.2,
            "enrolled_since": "2025-09-01",
        },
        {
            "id": "STU-003",
            "name": "Paul Andria",
            "email": "paul.andria@email.mg",
            "phone": "033 11 222 33",
            "year": "L3",
            "center": "Toamasina",
            "progress": 90,
            "validated_ecs": 11,
            "total_ecs": 12,
            "last_activity": "2026-01-22",
            "days_inactive": 0,
            "status": "active",
            "average": 16.8,
            "enrolled_since": "2024-09-01",
        },
        {
            "id": "STU-004",
            "name": "Luc Razafy",
            "email": "luc.razafy@email.mg",
            "phone": "034 55 666 77",
            "year": "L1",
            "center": "Fianarantsoa",
            "progress": 25,
            "validated_ecs": 3,
            "total_ecs": 12,
            "last_activity": "2026-01-15",
            "days_inactive": 7,
            "status": "inactive",
            "average": 9.5,
            "enrolled_since": "2025-09-01",
        },
    ]

    # Filtrer par statut
    if status and status != "all":
        mentees = [m for m in mentees if m["status"] == status]

    # Filtrer par année
    if year:
        mentees = [m for m in mentees if m["year"] == year]

    return mentees


@frappe.whitelist()
def get_mentee_detail(student_id):
    """
    Récupère les détails complets d'un mentoré.

    Args:
        student_id: ID de l'étudiant

    Returns:
        dict: Profil complet avec progression détaillée
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
        "address": "Lot IVG 123 Analakely",
        "enrolled_since": "2025-09-01",
        "photo": None,
    }

    progress = {
        "overall": 75,
        "validated_ecs": 8,
        "total_ecs": 12,
        "average": 14.5,
        "rank": 15,
        "total_students": 120,
    }

    # Liste des EC avec statut
    ecs = [
        {"id": "EC-001", "title": "Algorithmique", "status": "validated", "grade": 16, "validated_at": "2026-01-15"},
        {"id": "EC-002", "title": "Programmation Python", "status": "validated", "grade": 18, "validated_at": "2026-01-10"},
        {"id": "EC-003", "title": "Base de données", "status": "validated", "grade": 14, "validated_at": "2026-01-05"},
        {"id": "EC-004", "title": "Réseaux", "status": "in_progress", "grade": None, "progress": 60},
        {"id": "EC-005", "title": "Systèmes d'exploitation", "status": "not_started", "grade": None, "progress": 0},
    ]

    # Historique activité
    activity = [
        {"type": "quiz", "description": "Quiz Algorithmique réussi (16/20)", "date": "2026-01-15"},
        {"type": "lesson", "description": "Leçon 5 de Réseaux complétée", "date": "2026-01-14"},
        {"type": "payment", "description": "Paiement EC Réseaux confirmé", "date": "2026-01-10"},
        {"type": "login", "description": "Dernière connexion", "date": "2026-01-20"},
    ]

    # Tendance progression (6 derniers mois)
    progress_trend = [
        {"month": "Août", "progress": 10},
        {"month": "Sept", "progress": 25},
        {"month": "Oct", "progress": 40},
        {"month": "Nov", "progress": 55},
        {"month": "Déc", "progress": 65},
        {"month": "Jan", "progress": 75},
    ]

    return {
        "student": student,
        "progress": progress,
        "ecs": ecs,
        "activity": activity,
        "progress_trend": progress_trend,
    }


@frappe.whitelist()
def get_messages(student_id=None, limit=50):
    """
    Récupère les messages avec un mentoré ou tous les messages.

    Args:
        student_id: ID étudiant (optionnel, si None retourne tous)
        limit: Nombre max de messages

    Returns:
        list: Liste des conversations/messages
    """
    # Messages simulés
    if student_id:
        messages = [
            {
                "id": "msg-1",
                "sender": "mentor",
                "content": "Bonjour Jean, comment avancez-vous sur l'EC Réseaux ?",
                "timestamp": "2026-01-20 10:00",
                "read": True,
            },
            {
                "id": "msg-2",
                "sender": "student",
                "content": "Bonjour ! J'ai terminé les 3 premières leçons. J'ai une question sur le chapitre TCP/IP.",
                "timestamp": "2026-01-20 10:15",
                "read": True,
            },
            {
                "id": "msg-3",
                "sender": "mentor",
                "content": "Très bien ! Quelle est votre question ?",
                "timestamp": "2026-01-20 10:20",
                "read": True,
            },
            {
                "id": "msg-4",
                "sender": "student",
                "content": "Je ne comprends pas bien la différence entre TCP et UDP. Pouvez-vous m'expliquer ?",
                "timestamp": "2026-01-20 10:25",
                "read": False,
            },
        ]
    else:
        # Liste des conversations
        messages = [
            {
                "student_id": "STU-001",
                "student_name": "Jean Rakoto",
                "last_message": "Je ne comprends pas bien la différence...",
                "timestamp": "2026-01-20 10:25",
                "unread_count": 1,
            },
            {
                "student_id": "STU-002",
                "student_name": "Marie Rabe",
                "last_message": "Merci pour votre aide !",
                "timestamp": "2026-01-18 15:30",
                "unread_count": 0,
            },
            {
                "student_id": "STU-003",
                "student_name": "Paul Andria",
                "last_message": "J'ai validé l'EC !",
                "timestamp": "2026-01-22 14:35",
                "unread_count": 2,
            },
        ]

    return messages


@frappe.whitelist()
def send_message(student_id, content):
    """
    Envoie un message à un mentoré.

    Args:
        student_id: ID de l'étudiant destinataire
        content: Contenu du message

    Returns:
        dict: Message créé
    """
    if not student_id or not content:
        frappe.throw(_("Étudiant et contenu requis"))

    # Simuler création message
    message = {
        "id": f"msg-{frappe.generate_hash(length=8)}",
        "sender": "mentor",
        "recipient": student_id,
        "content": content,
        "timestamp": frappe.utils.now(),
        "read": False,
    }

    # TODO: Créer le message en base
    # TODO: Envoyer notification à l'étudiant

    return message


@frappe.whitelist()
def get_alerts(status="active"):
    """
    Récupère les alertes du mentor.

    Args:
        status: Filtrer par statut (active, resolved, all)

    Returns:
        list: Liste des alertes
    """
    alerts = [
        {
            "id": "alert-1",
            "type": "inactive",
            "student_id": "STU-002",
            "student_name": "Marie Rabe",
            "message": "Inactive depuis 12 jours",
            "severity": "warning",
            "created_at": "2026-01-20",
            "status": "active",
        },
        {
            "id": "alert-2",
            "type": "low_progress",
            "student_id": "STU-004",
            "student_name": "Luc Razafy",
            "message": "Progression faible (25%) en L1",
            "severity": "danger",
            "created_at": "2026-01-19",
            "status": "active",
        },
        {
            "id": "alert-3",
            "type": "failed_quiz",
            "student_id": "STU-005",
            "student_name": "Sophie Ranaivo",
            "message": "Échec au quiz Algorithmes (3ème tentative)",
            "severity": "warning",
            "created_at": "2026-01-18",
            "status": "active",
        },
    ]

    if status and status != "all":
        alerts = [a for a in alerts if a["status"] == status]

    return alerts


@frappe.whitelist()
def dismiss_alert(alert_id):
    """
    Marque une alerte comme résolue.

    Args:
        alert_id: ID de l'alerte

    Returns:
        dict: Alerte mise à jour
    """
    if not alert_id:
        frappe.throw(_("ID alerte requis"))

    # TODO: Mettre à jour en base
    return {"id": alert_id, "status": "resolved"}


@frappe.whitelist()
def get_mentee_stats(student_id):
    """
    Récupère les statistiques détaillées d'un mentoré.

    Args:
        student_id: ID de l'étudiant

    Returns:
        dict: Statistiques complètes
    """
    if not student_id:
        frappe.throw(_("ID étudiant requis"))

    return {
        "login_frequency": {
            "last_7_days": 5,
            "last_30_days": 18,
            "average_session": "45 min",
        },
        "quiz_performance": {
            "total_attempts": 12,
            "passed": 10,
            "failed": 2,
            "average_score": 14.8,
        },
        "ec_completion": {
            "on_time": 6,
            "late": 2,
            "pending": 4,
        },
        "engagement_score": 78,
    }
