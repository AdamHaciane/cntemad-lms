"""CNTEMAD Student Doctype."""

import frappe
from frappe.model.document import Document


class CNTEMADStudent(Document):
    """Représente un étudiant inscrit au CNTEMAD."""

    def before_save(self):
        """Calcule le nom complet avant sauvegarde."""
        self.full_name = f"{self.first_name} {self.last_name}"

    def after_insert(self):
        """Actions après création d'un étudiant."""
        # Create user if not exists
        if not self.user and self.email:
            self.create_user()

    def create_user(self):
        """Crée un utilisateur Frappe pour l'étudiant."""
        if frappe.db.exists("User", self.email):
            self.user = self.email
            return

        user = frappe.get_doc({
            "doctype": "User",
            "email": self.email,
            "first_name": self.first_name,
            "last_name": self.last_name,
            "enabled": 1,
            "user_type": "Website User",
            "roles": [{"role": "Student"}],
        })
        user.insert(ignore_permissions=True)
        self.user = user.name

    def get_progress(self) -> dict:
        """Retourne la progression de l'étudiant."""
        from cntemad_lms.cntemad_lms.api.student import get_student_progress
        return get_student_progress(self.name)
