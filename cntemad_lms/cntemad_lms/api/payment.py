"""
API endpoints for mobile money and bank transfer payments.

Providers supported:
- MVola (Telma) - 034, 038
- Orange Money - 032, 037
- Airtel Money - 033
- Bank Transfer (BFV, BNI)

Usage:
    POST /api/method/cntemad_lms.api.payment.initiate_payment
    POST /api/method/cntemad_lms.api.payment.initiate_bank_payment
    POST /api/method/cntemad_lms.api.payment.submit_bank_proof
    POST /api/method/cntemad_lms.api.payment.validate_bank_payment
    GET  /api/method/cntemad_lms.api.payment.check_payment_status
    POST /api/method/cntemad_lms.api.payment.webhook_callback
"""

import frappe
from frappe import _
from frappe.utils import now_datetime, cint, get_datetime_str
import re
import hashlib
import hmac
import random
import string


VALID_PROVIDERS = ["mvola", "orange_money", "airtel_money"]
VALID_BANKS = ["bfv", "bni"]

# Bank details for CNTEMAD
BANKS = {
    "bfv": {
        "name": "BFV-SG",
        "rib": "00005 00001 01234567890 12",
        "account_name": "CNTEMAD",
        "swift": "BFVMMGMG",
    },
    "bni": {
        "name": "BNI Madagascar",
        "rib": "00001 00002 01234567890 34",
        "account_name": "CNTEMAD",
        "swift": "BNIMMGMG",
    },
}

# Phone number patterns for Madagascar
PHONE_PATTERNS = {
    "mvola": r"^(034|038)\d{7}$",  # Telma
    "orange_money": r"^(032|037)\d{7}$",  # Orange
    "airtel_money": r"^(033)\d{7}$",  # Airtel
}

PROVIDER_LABELS = {
    "mvola": "MVola",
    "orange_money": "Orange Money",
    "airtel_money": "Airtel Money",
    "bank_bfv": "Virement BFV-SG",
    "bank_bni": "Virement BNI",
}

# Bank payment statuses (different from mobile money)
# pending_transfer: User has initiated, waiting for them to make the transfer
# pending_validation: User has submitted proof, waiting for admin validation
# completed: Admin has validated
# rejected: Admin has rejected


def validate_phone_number(phone: str, provider: str) -> bool:
    """Validate phone number format for provider."""
    phone = re.sub(r"[\s\-\.]", "", phone)
    pattern = PHONE_PATTERNS.get(provider)
    if not pattern:
        return False
    return bool(re.match(pattern, phone))


def get_provider_config(provider: str) -> dict:
    """Get provider API configuration from site config."""
    config = frappe.conf.get("mobile_money", {}).get(provider, {})
    return {
        "api_url": config.get("api_url", ""),
        "api_key": config.get("api_key", ""),
        "api_secret": config.get("api_secret", ""),
        "merchant_id": config.get("merchant_id", ""),
        "sandbox": config.get("sandbox", True),
    }


@frappe.whitelist()
def initiate_payment(ec_id: str, provider: str, phone_number: str) -> dict:
    """
    Initie un paiement mobile money pour un EC.

    Args:
        ec_id: ID de l'EC à payer
        provider: mvola, orange_money, ou airtel_money
        phone_number: Numéro de téléphone au format malgache

    Returns:
        dict: {
            "payment_id": str,
            "status": str,
            "provider_ref": str,
            "message": str
        }

    Raises:
        frappe.ValidationError: Si les données sont invalides
    """
    # Get current student
    student_id = frappe.db.get_value(
        "CNTEMAD Student", {"user": frappe.session.user}, "name"
    )
    if not student_id:
        frappe.throw(_("Profil étudiant non trouvé"), frappe.ValidationError)

    # Validate provider
    if provider not in VALID_PROVIDERS:
        frappe.throw(
            _("Provider invalide. Utilisez: {}").format(", ".join(VALID_PROVIDERS)),
            frappe.ValidationError
        )

    # Validate phone number
    phone_clean = re.sub(r"[\s\-\.]", "", phone_number)
    if not validate_phone_number(phone_clean, provider):
        frappe.throw(
            _("Numéro de téléphone invalide pour {}").format(PROVIDER_LABELS.get(provider, provider)),
            frappe.ValidationError,
        )

    # Check EC exists
    if not frappe.db.exists("CNTEMAD EC", ec_id):
        frappe.throw(_("EC non trouvé"), frappe.DoesNotExistError)

    ec = frappe.get_doc("CNTEMAD EC", ec_id)

    # Check if already paid
    existing_payment = frappe.db.get_value(
        "CNTEMAD Payment",
        {
            "student": student_id,
            "ec": ec_id,
            "status": ["in", ["Pending", "Processing", "Completed"]],
        },
        ["name", "status"],
        as_dict=True
    )

    if existing_payment:
        if existing_payment.status == "Completed":
            frappe.throw(_("Cet EC est déjà payé"), frappe.ValidationError)
        elif existing_payment.status in ["Pending", "Processing"]:
            return {
                "payment_id": existing_payment.name,
                "status": existing_payment.status.lower(),
                "message": _("Un paiement est déjà en cours pour cet EC"),
            }

    # Get amount from EC
    amount = ec.price or 0
    if amount <= 0:
        frappe.throw(_("Prix de l'EC invalide"), frappe.ValidationError)

    # Create payment record
    payment = frappe.get_doc({
        "doctype": "CNTEMAD Payment",
        "student": student_id,
        "ec": ec_id,
        "amount": amount,
        "provider": provider,
        "status": "Pending",
        "phone_last_4": phone_clean[-4:],
    })
    payment.insert(ignore_permissions=True)
    frappe.db.commit()

    # Call provider API
    try:
        provider_response = call_provider_api(payment, phone_clean)

        if provider_response.get("success"):
            payment.status = "Processing"
            payment.provider_transaction_id = provider_response.get("transaction_id", "")
            payment.save(ignore_permissions=True)
            frappe.db.commit()

            return {
                "payment_id": payment.name,
                "status": "processing",
                "provider_ref": provider_response.get("transaction_id"),
                "amount": amount,
                "provider_label": PROVIDER_LABELS.get(provider, provider),
                "message": _("Paiement initié. Confirmez sur votre téléphone."),
            }
        else:
            payment.status = "Failed"
            payment.failure_reason = provider_response.get("error", "Unknown error")
            payment.save(ignore_permissions=True)
            frappe.db.commit()

            frappe.throw(
                _("Erreur provider: {}").format(provider_response.get("error")),
                frappe.ValidationError,
            )

    except Exception as e:
        payment.status = "Failed"
        payment.failure_reason = str(e)
        payment.save(ignore_permissions=True)
        frappe.db.commit()
        raise


def call_provider_api(payment, phone: str) -> dict:
    """
    Call the mobile money provider API to initiate payment.

    In sandbox mode, simulates a successful payment initiation.
    In production, calls the actual provider API.
    """
    provider = payment.provider
    config = get_provider_config(provider)

    # Sandbox mode - simulate success
    if config.get("sandbox", True):
        # Generate fake transaction ID
        tx_id = "".join(random.choices(string.ascii_uppercase + string.digits, k=12))
        return {
            "success": True,
            "transaction_id": f"{provider.upper()}-{tx_id}",
            "message": "Payment initiated (sandbox)",
        }

    # Production mode - call actual provider API
    if provider == "mvola":
        return call_mvola_api(payment, phone, config)
    elif provider == "orange_money":
        return call_orange_api(payment, phone, config)
    elif provider == "airtel_money":
        return call_airtel_api(payment, phone, config)

    return {"success": False, "error": "Provider not configured"}


def call_mvola_api(payment, phone: str, config: dict) -> dict:
    """Call MVola API to initiate payment."""
    import requests

    api_url = config.get("api_url", "https://devapi.mvola.mg")

    headers = {
        "Authorization": f"Bearer {config.get('api_key')}",
        "Content-Type": "application/json",
        "X-Callback-URL": frappe.utils.get_url(
            "/api/method/cntemad_lms.api.payment.mvola_callback"
        ),
    }

    payload = {
        "amount": str(int(payment.amount)),
        "currency": "Ar",
        "descriptionText": f"Paiement EC - {payment.ec}",
        "requestingOrganisationTransactionReference": payment.name,
        "requestDate": now_datetime().isoformat(),
        "debitParty": [{"key": "msisdn", "value": phone}],
        "creditParty": [{"key": "msisdn", "value": config.get("merchant_id")}],
    }

    try:
        response = requests.post(
            f"{api_url}/mvola/mm/transactions/type/merchantpay/1.0.0/",
            json=payload,
            headers=headers,
            timeout=30,
        )

        if response.status_code == 200:
            data = response.json()
            return {
                "success": True,
                "transaction_id": data.get("serverCorrelationId"),
            }
        else:
            return {
                "success": False,
                "error": f"MVola error: {response.status_code}",
            }
    except requests.exceptions.RequestException as e:
        return {"success": False, "error": str(e)}


def call_orange_api(payment, phone: str, config: dict) -> dict:
    """Call Orange Money API to initiate payment."""
    # Placeholder - implement based on Orange Money API docs
    return {
        "success": True,
        "transaction_id": f"ORANGE-{payment.name}",
    }


def call_airtel_api(payment, phone: str, config: dict) -> dict:
    """Call Airtel Money API to initiate payment."""
    # Placeholder - implement based on Airtel Money API docs
    return {
        "success": True,
        "transaction_id": f"AIRTEL-{payment.name}",
    }


@frappe.whitelist()
def check_payment_status(payment_id: str) -> dict:
    """
    Vérifie le statut d'un paiement.

    Args:
        payment_id: ID du paiement CNTEMAD

    Returns:
        dict: {
            "status": str,
            "completed_at": datetime,
            "failure_reason": str,
            # For bank payments:
            "bank_reference": str,
            "bank": dict,
            "proof_type": str,
            "proof_value": str
        }
    """
    if not frappe.db.exists("CNTEMAD Payment", payment_id):
        frappe.throw(_("Paiement non trouvé"), frappe.DoesNotExistError)

    payment = frappe.get_doc("CNTEMAD Payment", payment_id)

    # Verify ownership
    student_id = frappe.db.get_value(
        "CNTEMAD Student", {"user": frappe.session.user}, "name"
    )

    if payment.student != student_id and not frappe.has_permission("CNTEMAD Payment", "write"):
        frappe.throw(_("Accès non autorisé"), frappe.PermissionError)

    result = {
        "payment_id": payment.name,
        "status": payment.status.lower().replace(" ", "_"),
        "amount": payment.amount,
        "provider": payment.provider,
        "provider_label": PROVIDER_LABELS.get(payment.provider, payment.provider),
        "ec": payment.ec,
        "ec_title": frappe.db.get_value("CNTEMAD EC", payment.ec, "title") if payment.ec else None,
        "completed_at": str(payment.completed_at) if payment.completed_at else None,
        "failure_reason": payment.failure_reason,
    }

    # Add bank-specific fields if it's a bank payment
    if payment.provider and payment.provider.startswith("bank_"):
        bank_code = payment.bank_code or payment.provider.replace("bank_", "")
        bank_info = BANKS.get(bank_code)
        result.update({
            "is_bank_payment": True,
            "bank_reference": payment.bank_reference,
            "bank_code": bank_code,
            "bank": {
                "id": bank_code,
                "name": bank_info["name"] if bank_info else bank_code,
                "rib": bank_info["rib"] if bank_info else None,
                "account_name": bank_info["account_name"] if bank_info else None,
                "swift": bank_info["swift"] if bank_info else None,
            } if bank_info else None,
            "proof_type": payment.proof_type,
            "proof_value": payment.proof_value,
            "proof_submitted_at": str(payment.proof_submitted_at) if payment.proof_submitted_at else None,
        })
    else:
        result["is_bank_payment"] = False

    return result


@frappe.whitelist()
def get_payment_history(limit: int = 20, offset: int = 0) -> dict:
    """
    Get payment history for current student.

    Returns:
        dict: { payments: [], total: int }
    """
    student_id = frappe.db.get_value(
        "CNTEMAD Student", {"user": frappe.session.user}, "name"
    )

    if not student_id:
        return {"payments": [], "total": 0}

    filters = {"student": student_id}
    total = frappe.db.count("CNTEMAD Payment", filters)

    payments = frappe.get_all(
        "CNTEMAD Payment",
        filters=filters,
        fields=[
            "name", "ec", "amount", "provider", "status",
            "creation", "completed_at", "failure_reason"
        ],
        order_by="creation desc",
        limit_page_length=cint(limit),
        limit_start=cint(offset),
    )

    # Enrich with EC titles
    for p in payments:
        if p.ec:
            p["ec_title"] = frappe.db.get_value("CNTEMAD EC", p.ec, "title")
        p["provider_label"] = PROVIDER_LABELS.get(p.provider, p.provider)

    return {
        "payments": payments,
        "total": total,
    }


@frappe.whitelist(allow_guest=True)
def mvola_callback():
    """Webhook callback for MVola payment notifications."""
    return process_webhook_callback("mvola")


@frappe.whitelist(allow_guest=True)
def orange_callback():
    """Webhook callback for Orange Money payment notifications."""
    return process_webhook_callback("orange_money")


@frappe.whitelist(allow_guest=True)
def airtel_callback():
    """Webhook callback for Airtel Money payment notifications."""
    return process_webhook_callback("airtel_money")


def process_webhook_callback(provider: str) -> dict:
    """
    Process webhook callback from mobile money provider.

    Args:
        provider: Provider name (mvola, orange_money, airtel_money)

    Returns:
        dict: {"status": "ok"} or error
    """
    config = get_provider_config(provider)

    # Verify webhook signature (skip in sandbox)
    if not config.get("sandbox", True):
        if not verify_webhook_signature(provider, config):
            frappe.throw(_("Invalid webhook signature"), frappe.AuthenticationError)

    # Parse callback data
    data = frappe.request.get_json(force=True, silent=True) or {}

    # Extract transaction info based on provider format
    if provider == "mvola":
        tx_id = data.get("serverCorrelationId")
        reference = data.get("requestingOrganisationTransactionReference")
        status = data.get("status", "").lower()
    elif provider == "orange_money":
        tx_id = data.get("transactionId")
        reference = data.get("orderId")
        status = data.get("status", "").lower()
    elif provider == "airtel_money":
        tx_id = data.get("transaction_id")
        reference = data.get("reference")
        status = data.get("status", "").lower()
    else:
        return {"status": "error", "message": "Unknown provider"}

    # Find payment by reference (our payment name)
    if not reference or not frappe.db.exists("CNTEMAD Payment", reference):
        frappe.log_error(
            f"Webhook callback: Payment not found for reference {reference}",
            "Payment Webhook Error"
        )
        return {"status": "error", "message": "Payment not found"}

    payment = frappe.get_doc("CNTEMAD Payment", reference)

    # Update payment status
    if status in ["completed", "success", "successful"]:
        payment.status = "Completed"
        payment.completed_at = now_datetime()
        payment.provider_transaction_id = tx_id

        # Create/update enrollment
        if payment.ec:
            activate_ec_enrollment(payment.student, payment.ec, payment.name)

        # Send confirmation
        send_payment_confirmation(payment)

    elif status in ["failed", "cancelled", "rejected"]:
        payment.status = "Failed"
        payment.failure_reason = data.get("message", data.get("reason", "Payment failed"))

    elif status in ["pending", "processing"]:
        payment.status = "Processing"

    payment.save(ignore_permissions=True)
    frappe.db.commit()

    frappe.logger().info(f"Payment {reference} updated to {payment.status}")
    return {"status": "ok"}


def verify_webhook_signature(provider: str, config: dict) -> bool:
    """Verify webhook signature from provider."""
    if provider == "mvola":
        signature = frappe.request.headers.get("X-Callback-Signature", "")
        secret = config.get("api_secret", "")
        body = frappe.request.get_data(as_text=True)
        expected = hmac.new(
            secret.encode(), body.encode(), hashlib.sha256
        ).hexdigest()
        return hmac.compare_digest(signature, expected)

    # Other providers - implement as needed
    return True


def activate_ec_enrollment(student_id: str, ec_id: str, payment_name: str = None):
    """Active l'inscription d'un étudiant à un EC après paiement."""
    enrollment = frappe.db.get_value(
        "CNTEMAD Enrollment",
        {"student": student_id, "ec": ec_id},
        "name"
    )

    if enrollment:
        frappe.db.set_value("CNTEMAD Enrollment", enrollment, {
            "status": "Paid",
            "payment": payment_name,
        })
    else:
        # Create enrollment
        frappe.get_doc({
            "doctype": "CNTEMAD Enrollment",
            "student": student_id,
            "ec": ec_id,
            "status": "Paid",
            "payment": payment_name,
            "enrollment_date": now_datetime(),
        }).insert(ignore_permissions=True)

    frappe.db.commit()


def send_payment_confirmation(payment) -> None:
    """Send SMS/email confirmation for successful payment."""
    try:
        student = frappe.get_doc("CNTEMAD Student", payment.student)
        ec_title = frappe.db.get_value("CNTEMAD EC", payment.ec, "title") or payment.ec

        # Email notification
        if student.user:
            frappe.sendmail(
                recipients=[student.user],
                subject=f"Paiement confirmé - {ec_title}",
                message=f"""
                <p>Bonjour {student.full_name},</p>
                <p>Votre paiement a été confirmé:</p>
                <ul>
                    <li><strong>EC:</strong> {ec_title}</li>
                    <li><strong>Montant:</strong> {int(payment.amount):,} Ar</li>
                    <li><strong>Référence:</strong> {payment.name}</li>
                </ul>
                <p>Vous pouvez maintenant accéder au contenu de l'EC.</p>
                <p>CNTEMAD</p>
                """,
            )

        frappe.logger().info(f"Payment confirmation sent for {payment.name}")

    except Exception as e:
        frappe.log_error(f"Failed to send payment confirmation: {e}", "Payment Notification Error")


# Simulate payment completion for sandbox testing
@frappe.whitelist()
def simulate_payment_success(payment_id: str) -> dict:
    """
    Simulate successful payment (sandbox only).

    Args:
        payment_id: ID of pending payment

    Returns:
        dict: Updated payment status
    """
    config = get_provider_config("mvola")  # Check any provider
    if not config.get("sandbox", True):
        frappe.throw(_("Simulation not available in production"))

    if not frappe.db.exists("CNTEMAD Payment", payment_id):
        frappe.throw(_("Paiement non trouvé"))

    payment = frappe.get_doc("CNTEMAD Payment", payment_id)

    # Verify ownership
    student_id = frappe.db.get_value(
        "CNTEMAD Student", {"user": frappe.session.user}, "name"
    )
    if payment.student != student_id:
        frappe.throw(_("Accès non autorisé"))

    if payment.status not in ["Pending", "Processing"]:
        frappe.throw(_("Le paiement ne peut pas être simulé dans cet état"))

    # Simulate success
    payment.status = "Completed"
    payment.completed_at = now_datetime()
    payment.save(ignore_permissions=True)

    # Activate enrollment
    if payment.ec:
        activate_ec_enrollment(payment.student, payment.ec, payment.name)

    frappe.db.commit()

    return {
        "payment_id": payment.name,
        "status": "completed",
        "message": _("Paiement simulé avec succès (sandbox)"),
    }


# ==============================================================================
# BANK TRANSFER PAYMENT FUNCTIONS
# ==============================================================================


def generate_bank_reference(ec_id: str, student_id: str) -> str:
    """
    Generate unique reference for bank transfer.
    Format: CNT-{EC_CODE}-{STUDENT_ID[-4:]}-{YYMMDD}

    Example: CNT-INFO101-2345-240122
    """
    # Get EC code (first part of EC name or title)
    ec_code = ec_id.split("-")[0] if "-" in ec_id else ec_id[:8]
    ec_code = ec_code.upper()

    # Last 4 digits of student ID
    student_suffix = student_id[-4:] if len(student_id) >= 4 else student_id

    # Date stamp
    date_stamp = now_datetime().strftime("%y%m%d")

    return f"CNT-{ec_code}-{student_suffix}-{date_stamp}"


@frappe.whitelist()
def get_banks() -> list:
    """
    Get list of available banks for transfer.

    Returns:
        list: Bank details (without sensitive info)
    """
    return [
        {
            "id": bank_id,
            "name": bank_info["name"],
            "rib": bank_info["rib"],
            "account_name": bank_info["account_name"],
            "swift": bank_info["swift"],
        }
        for bank_id, bank_info in BANKS.items()
    ]


@frappe.whitelist()
def initiate_bank_payment(ec_id: str, bank: str) -> dict:
    """
    Initiate a bank transfer payment for an EC.

    Different from mobile money:
    - No instant confirmation
    - Returns bank details and unique reference
    - Status starts as 'Pending Transfer'

    Args:
        ec_id: ID of the EC to pay
        bank: Bank code (bfv or bni)

    Returns:
        dict: {
            "payment_id": str,
            "status": str,
            "reference": str,
            "bank": dict,
            "amount": float,
            "message": str
        }
    """
    # Get current student
    student_id = frappe.db.get_value(
        "CNTEMAD Student", {"user": frappe.session.user}, "name"
    )
    if not student_id:
        frappe.throw(_("Profil étudiant non trouvé"), frappe.ValidationError)

    # Validate bank
    if bank not in VALID_BANKS:
        frappe.throw(
            _("Banque invalide. Utilisez: {}").format(", ".join(VALID_BANKS)),
            frappe.ValidationError
        )

    # Check EC exists
    if not frappe.db.exists("CNTEMAD EC", ec_id):
        frappe.throw(_("EC non trouvé"), frappe.DoesNotExistError)

    ec = frappe.get_doc("CNTEMAD EC", ec_id)

    # Check if already paid or has pending bank payment
    existing_payment = frappe.db.get_value(
        "CNTEMAD Payment",
        {
            "student": student_id,
            "ec": ec_id,
            "status": ["in", ["Pending", "Processing", "Completed", "Pending Transfer", "Pending Validation"]],
        },
        ["name", "status", "bank_reference"],
        as_dict=True
    )

    if existing_payment:
        if existing_payment.status == "Completed":
            frappe.throw(_("Cet EC est déjà payé"), frappe.ValidationError)
        elif existing_payment.status in ["Pending Transfer", "Pending Validation"]:
            # Return existing bank payment info
            bank_info = BANKS.get(bank, BANKS["bfv"])
            return {
                "payment_id": existing_payment.name,
                "status": existing_payment.status.lower().replace(" ", "_"),
                "reference": existing_payment.bank_reference,
                "bank": {
                    "id": bank,
                    "name": bank_info["name"],
                    "rib": bank_info["rib"],
                    "account_name": bank_info["account_name"],
                    "swift": bank_info["swift"],
                },
                "amount": ec.price,
                "message": _("Un virement est déjà en cours pour cet EC"),
            }
        elif existing_payment.status in ["Pending", "Processing"]:
            return {
                "payment_id": existing_payment.name,
                "status": existing_payment.status.lower(),
                "message": _("Un paiement mobile money est déjà en cours pour cet EC"),
            }

    # Get amount from EC
    amount = ec.price or 0
    if amount <= 0:
        frappe.throw(_("Prix de l'EC invalide"), frappe.ValidationError)

    # Generate unique reference
    bank_reference = generate_bank_reference(ec_id, student_id)

    # Create payment record
    payment = frappe.get_doc({
        "doctype": "CNTEMAD Payment",
        "student": student_id,
        "ec": ec_id,
        "amount": amount,
        "provider": f"bank_{bank}",
        "status": "Pending Transfer",
        "bank_reference": bank_reference,
        "bank_code": bank,
    })
    payment.insert(ignore_permissions=True)
    frappe.db.commit()

    bank_info = BANKS[bank]

    return {
        "payment_id": payment.name,
        "status": "pending_transfer",
        "reference": bank_reference,
        "bank": {
            "id": bank,
            "name": bank_info["name"],
            "rib": bank_info["rib"],
            "account_name": bank_info["account_name"],
            "swift": bank_info["swift"],
        },
        "amount": amount,
        "ec_title": ec.title,
        "message": _("Effectuez le virement avec la référence indiquée, puis soumettez votre preuve de paiement."),
    }


@frappe.whitelist()
def submit_bank_proof(payment_id: str, proof_type: str, proof_value: str) -> dict:
    """
    Submit proof of bank transfer.

    Args:
        payment_id: ID of the payment
        proof_type: Type of proof ('reference' or 'receipt')
        proof_value: Bank reference number or file URL

    Returns:
        dict: Updated payment status
    """
    if not frappe.db.exists("CNTEMAD Payment", payment_id):
        frappe.throw(_("Paiement non trouvé"), frappe.DoesNotExistError)

    payment = frappe.get_doc("CNTEMAD Payment", payment_id)

    # Verify ownership
    student_id = frappe.db.get_value(
        "CNTEMAD Student", {"user": frappe.session.user}, "name"
    )

    if payment.student != student_id:
        frappe.throw(_("Accès non autorisé"), frappe.PermissionError)

    # Validate status
    if payment.status != "Pending Transfer":
        frappe.throw(
            _("Ce paiement ne peut pas recevoir de preuve dans son état actuel: {}").format(payment.status),
            frappe.ValidationError
        )

    # Validate proof type
    if proof_type not in ["reference", "receipt"]:
        frappe.throw(_("Type de preuve invalide"), frappe.ValidationError)

    # Validate proof value
    if not proof_value or len(proof_value.strip()) < 3:
        frappe.throw(_("La preuve de paiement est invalide"), frappe.ValidationError)

    # Update payment
    payment.status = "Pending Validation"
    payment.proof_type = proof_type
    payment.proof_value = proof_value.strip()
    payment.proof_submitted_at = now_datetime()
    payment.save(ignore_permissions=True)
    frappe.db.commit()

    # Notify center admin
    notify_center_admin_bank_payment(payment)

    return {
        "payment_id": payment.name,
        "status": "pending_validation",
        "message": _("Votre preuve a été soumise. Vous serez notifié une fois le paiement validé par votre centre."),
    }


def notify_center_admin_bank_payment(payment) -> None:
    """Notify center admin about pending bank payment validation."""
    try:
        student = frappe.get_doc("CNTEMAD Student", payment.student)
        ec_title = frappe.db.get_value("CNTEMAD EC", payment.ec, "title") or payment.ec

        # Get center admin email (if center has admin)
        if student.center:
            center_admin_email = frappe.db.get_value(
                "CNTEMAD Center", student.center, "admin_email"
            )
            if center_admin_email:
                frappe.sendmail(
                    recipients=[center_admin_email],
                    subject=f"Virement à valider - {student.full_name}",
                    message=f"""
                    <p>Un nouveau virement bancaire nécessite votre validation:</p>
                    <ul>
                        <li><strong>Étudiant:</strong> {student.full_name}</li>
                        <li><strong>EC:</strong> {ec_title}</li>
                        <li><strong>Montant:</strong> {int(payment.amount):,} Ar</li>
                        <li><strong>Référence:</strong> {payment.bank_reference}</li>
                        <li><strong>Type de preuve:</strong> {payment.proof_type}</li>
                        <li><strong>Preuve:</strong> {payment.proof_value}</li>
                    </ul>
                    <p>Connectez-vous au dashboard admin pour valider ou rejeter ce paiement.</p>
                    """,
                )

        frappe.logger().info(f"Bank payment notification sent for {payment.name}")

    except Exception as e:
        frappe.log_error(f"Failed to send bank payment notification: {e}", "Bank Payment Notification Error")


@frappe.whitelist()
def validate_bank_payment(payment_id: str, approved: bool, note: str = "") -> dict:
    """
    Validate or reject a bank transfer payment (admin only).

    Args:
        payment_id: ID of the payment
        approved: True to approve, False to reject
        note: Admin note (required for rejection)

    Returns:
        dict: Updated payment status
    """
    # Check permissions - must be Center Admin or above
    if not frappe.has_permission("CNTEMAD Payment", "write"):
        frappe.throw(_("Vous n'avez pas la permission de valider les paiements"), frappe.PermissionError)

    if not frappe.db.exists("CNTEMAD Payment", payment_id):
        frappe.throw(_("Paiement non trouvé"), frappe.DoesNotExistError)

    payment = frappe.get_doc("CNTEMAD Payment", payment_id)

    # Validate status
    if payment.status != "Pending Validation":
        frappe.throw(
            _("Ce paiement ne peut pas être validé dans son état actuel: {}").format(payment.status),
            frappe.ValidationError
        )

    # Rejection requires a note
    if not approved and not note:
        frappe.throw(_("Une note est requise pour le rejet"), frappe.ValidationError)

    if approved:
        payment.status = "Completed"
        payment.completed_at = now_datetime()
        payment.validated_by = frappe.session.user
        payment.validation_note = note

        # Activate enrollment
        if payment.ec:
            activate_ec_enrollment(payment.student, payment.ec, payment.name)

        # Send confirmation to student
        send_bank_payment_confirmation(payment, approved=True)

        message = _("Paiement validé avec succès")
    else:
        payment.status = "Rejected"
        payment.failure_reason = note
        payment.validated_by = frappe.session.user
        payment.validation_note = note

        # Send rejection notification to student
        send_bank_payment_confirmation(payment, approved=False, reason=note)

        message = _("Paiement rejeté")

    payment.save(ignore_permissions=True)
    frappe.db.commit()

    return {
        "payment_id": payment.name,
        "status": payment.status.lower().replace(" ", "_"),
        "message": message,
    }


def send_bank_payment_confirmation(payment, approved: bool, reason: str = "") -> None:
    """Send confirmation/rejection email for bank payment."""
    try:
        student = frappe.get_doc("CNTEMAD Student", payment.student)
        ec_title = frappe.db.get_value("CNTEMAD EC", payment.ec, "title") or payment.ec

        if student.user:
            if approved:
                subject = f"Paiement validé - {ec_title}"
                message = f"""
                <p>Bonjour {student.full_name},</p>
                <p>Votre virement bancaire a été validé:</p>
                <ul>
                    <li><strong>EC:</strong> {ec_title}</li>
                    <li><strong>Montant:</strong> {int(payment.amount):,} Ar</li>
                    <li><strong>Référence:</strong> {payment.bank_reference}</li>
                </ul>
                <p>Vous pouvez maintenant accéder au contenu de l'EC.</p>
                <p>CNTEMAD</p>
                """
            else:
                subject = f"Paiement rejeté - {ec_title}"
                message = f"""
                <p>Bonjour {student.full_name},</p>
                <p>Votre virement bancaire a été rejeté:</p>
                <ul>
                    <li><strong>EC:</strong> {ec_title}</li>
                    <li><strong>Montant:</strong> {int(payment.amount):,} Ar</li>
                    <li><strong>Référence:</strong> {payment.bank_reference}</li>
                    <li><strong>Raison:</strong> {reason}</li>
                </ul>
                <p>Veuillez contacter votre centre CNTEMAD pour plus d'informations.</p>
                <p>CNTEMAD</p>
                """

            frappe.sendmail(
                recipients=[student.user],
                subject=subject,
                message=message,
            )

        frappe.logger().info(f"Bank payment {'confirmation' if approved else 'rejection'} sent for {payment.name}")

    except Exception as e:
        frappe.log_error(f"Failed to send bank payment confirmation: {e}", "Bank Payment Notification Error")


@frappe.whitelist()
def get_pending_bank_payments(center_id: str = None, limit: int = 50, offset: int = 0) -> dict:
    """
    Get pending bank payments for validation (admin endpoint).

    Args:
        center_id: Filter by center (optional)
        limit: Number of results
        offset: Pagination offset

    Returns:
        dict: { payments: [], total: int }
    """
    # Check permissions
    if not frappe.has_permission("CNTEMAD Payment", "read"):
        frappe.throw(_("Accès non autorisé"), frappe.PermissionError)

    filters = {
        "status": "Pending Validation",
        "provider": ["like", "bank_%"],
    }

    # If center_id provided, filter by student's center
    if center_id:
        students_in_center = frappe.get_all(
            "CNTEMAD Student",
            filters={"center": center_id},
            pluck="name"
        )
        if students_in_center:
            filters["student"] = ["in", students_in_center]
        else:
            return {"payments": [], "total": 0}

    total = frappe.db.count("CNTEMAD Payment", filters)

    payments = frappe.get_all(
        "CNTEMAD Payment",
        filters=filters,
        fields=[
            "name", "student", "ec", "amount", "provider", "status",
            "bank_reference", "bank_code", "proof_type", "proof_value",
            "proof_submitted_at", "creation"
        ],
        order_by="proof_submitted_at desc",
        limit_page_length=cint(limit),
        limit_start=cint(offset),
    )

    # Enrich with student and EC info
    for p in payments:
        p["student_name"] = frappe.db.get_value("CNTEMAD Student", p.student, "full_name")
        p["ec_title"] = frappe.db.get_value("CNTEMAD EC", p.ec, "title") if p.ec else None
        p["provider_label"] = PROVIDER_LABELS.get(p.provider, p.provider)
        p["bank_name"] = BANKS.get(p.bank_code, {}).get("name", p.bank_code)

    return {
        "payments": payments,
        "total": total,
    }
