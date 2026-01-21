"""API and hooks for enrollment operations."""

import frappe
from frappe import _


def on_enrollment_created(doc, method):
    """Hook après création d'une inscription."""
    # Log enrollment
    frappe.log_error(
        message=f"Enrollment created: {doc.student} -> {doc.ec or doc.course}",
        title="Enrollment Created"
    )

    # Send welcome notification if needed
    # send_enrollment_welcome(doc)
