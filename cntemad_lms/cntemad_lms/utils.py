"""Utility functions for CNTEMAD LMS."""

import frappe


def get_student_progress(student_id: str) -> dict:
    """
    Jinja method pour obtenir la progression d'un étudiant.

    Usage dans template:
        {{ get_student_progress(student.name) }}
    """
    from cntemad_lms.cntemad_lms.api.student import get_student_progress as _get_progress
    return _get_progress(student_id)


def get_current_student():
    """Retourne l'étudiant lié à l'utilisateur courant."""
    if frappe.session.user == "Guest":
        return None

    return frappe.db.get_value(
        "CNTEMAD Student",
        {"user": frappe.session.user},
        ["name", "full_name", "center", "current_year"],
        as_dict=True
    )
