"""API endpoints for payment operations."""

import frappe
from frappe import _


VALID_PROVIDERS = ["mvola", "orange_money", "airtel_money"]


@frappe.whitelist()
def initiate_payment(student_id: str, amount: float, provider: str, ec_id: str = None) -> dict:
    """
    Initie un paiement mobile money.

    Args:
        student_id: ID de l'étudiant
        amount: Montant en Ariary
        provider: Provider (mvola, orange_money, airtel_money)
        ec_id: ID de l'EC à payer (optionnel)

    Returns:
        dict: {
            "payment_id": str,
            "status": str,
            "redirect_url": str (si applicable)
        }
    """
    # Validations
    if not frappe.db.exists("CNTEMAD Student", student_id):
        frappe.throw(_("Étudiant invalide"))

    if not isinstance(amount, (int, float)) or amount <= 0:
        frappe.throw(_("Montant invalide"))

    if provider not in VALID_PROVIDERS:
        frappe.throw(_("Provider invalide. Utilisez: {}").format(", ".join(VALID_PROVIDERS)))

    # Create payment record
    payment = frappe.get_doc({
        "doctype": "CNTEMAD Payment",
        "student": student_id,
        "amount": amount,
        "provider": provider,
        "ec": ec_id,
        "status": "Pending",
    })
    payment.insert()

    # TODO: Call provider API
    # result = call_provider_api(provider, amount, payment.name)

    return {
        "payment_id": payment.name,
        "status": "Pending",
        "message": _("Paiement initié. Veuillez confirmer sur votre téléphone."),
    }


@frappe.whitelist(allow_guest=True)
def payment_callback(provider: str, transaction_id: str, status: str, **kwargs) -> dict:
    """
    Webhook callback pour les paiements.

    Args:
        provider: Provider source
        transaction_id: ID transaction du provider
        status: Statut du paiement

    Returns:
        dict: Confirmation
    """
    # Validate webhook signature (TODO: implement per provider)
    # if not validate_webhook_signature(provider, kwargs):
    #     frappe.throw(_("Signature invalide"), frappe.AuthenticationError)

    # Find payment by transaction ID
    payment_name = frappe.db.get_value(
        "CNTEMAD Payment",
        {"provider_transaction_id": transaction_id},
        "name"
    )

    if not payment_name:
        frappe.log_error(f"Payment not found for transaction: {transaction_id}")
        return {"status": "error", "message": "Payment not found"}

    payment = frappe.get_doc("CNTEMAD Payment", payment_name)

    # Update status
    if status == "success":
        payment.status = "Completed"
        payment.completed_at = frappe.utils.now()

        # Activate enrollment if EC payment
        if payment.ec:
            activate_ec_enrollment(payment.student, payment.ec)

    elif status == "failed":
        payment.status = "Failed"
        payment.failure_reason = kwargs.get("reason", "Unknown")

    payment.save(ignore_permissions=True)
    frappe.db.commit()

    return {"status": "ok"}


def activate_ec_enrollment(student_id: str, ec_id: str):
    """Active l'inscription d'un étudiant à un EC après paiement."""
    enrollment = frappe.db.get_value(
        "CNTEMAD Enrollment",
        {"student": student_id, "ec": ec_id},
        "name"
    )

    if enrollment:
        frappe.db.set_value("CNTEMAD Enrollment", enrollment, "status", "Active")
    else:
        # Create enrollment
        frappe.get_doc({
            "doctype": "CNTEMAD Enrollment",
            "student": student_id,
            "ec": ec_id,
            "status": "Active",
        }).insert()


def on_payment_created(doc, method):
    """Hook après création d'un paiement."""
    # Log for audit
    frappe.log_error(
        message=f"Payment created: {doc.name} - {doc.amount} Ar via {doc.provider}",
        title="Payment Created"
    )


def on_payment_updated(doc, method):
    """Hook après mise à jour d'un paiement."""
    if doc.status == "Completed" and doc.has_value_changed("status"):
        # Send confirmation SMS/notification
        # send_payment_confirmation(doc)
        pass
