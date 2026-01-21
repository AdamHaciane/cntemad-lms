"""CNTEMAD Course Doctype."""

import frappe
from frappe.model.document import Document


class CNTEMADCourse(Document):
    """Représente un cours CNTEMAD."""

    def validate(self):
        """Valide et met à jour le compteur d'EC."""
        self.update_ec_count()

    def update_ec_count(self):
        """Met à jour le nombre d'EC liés à ce cours."""
        self.ec_count = frappe.db.count("CNTEMAD EC", {"course": self.name})
