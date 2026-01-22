"""Frappe Hooks for CNTEMAD LMS."""

app_name = "cntemad_lms"
app_title = "CNTEMAD LMS"
app_publisher = "CNTEMAD"
app_description = "Plateforme LMS du Centre National de Télé-Enseignement de Madagascar"
app_email = "contact@cntemad.mg"
app_license = "GPL-3.0"

# Apps
required_apps = ["frappe", "lms"]

# Website
website_route_rules = [
    {"from_route": "/student/<path:app_path>", "to_route": "student"},
]

# Doctypes
fixtures = [
    {
        "doctype": "Custom Field",
        "filters": [["module", "=", "CNTEMAD LMS"]],
    },
    {
        "doctype": "Property Setter",
        "filters": [["module", "=", "CNTEMAD LMS"]],
    },
]

# Document Events
doc_events = {
    "CNTEMAD Payment": {
        "after_insert": "cntemad_lms.cntemad_lms.api.payment.on_payment_created",
        "on_update": "cntemad_lms.cntemad_lms.api.payment.on_payment_updated",
    },
    "CNTEMAD Enrollment": {
        "after_insert": "cntemad_lms.cntemad_lms.api.enrollment.on_enrollment_created",
    },
}

# Scheduled Tasks
scheduler_events = {
    "daily": [
        "cntemad_lms.cntemad_lms.tasks.daily.send_progress_reminders",
    ],
    "weekly": [
        "cntemad_lms.cntemad_lms.tasks.weekly.generate_center_reports",
    ],
}

# Jinja
jinja = {
    "methods": [
        "cntemad_lms.cntemad_lms.utils.get_student_progress",
    ],
}

# Include JS/CSS
app_include_css = "/assets/cntemad_lms/css/cntemad.css"
app_include_js = "/assets/cntemad_lms/js/cntemad.js"

# Web Include
web_include_css = "/assets/cntemad_lms/css/cntemad-web.css"
web_include_js = "/assets/cntemad_lms/js/cntemad-web.js"

# Home Pages
role_home_page = {
    "Student": "student",
    "Instructor": "instructor",
}

# Portal Menu
portal_menu_items = [
    {"title": "Mes Cours", "route": "/student/courses", "role": "Student"},
    {"title": "Ma Progression", "route": "/student/progress", "role": "Student"},
    {"title": "Paiements", "route": "/student/payments", "role": "Student"},
]

# Translation
# translated_languages_for_website = ["fr", "mg", "en"]
