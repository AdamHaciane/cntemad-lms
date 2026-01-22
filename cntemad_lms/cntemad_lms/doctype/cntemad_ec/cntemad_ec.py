"""CNTEMAD EC Doctype."""

import frappe
from frappe.model.document import Document


class CNTEMADEC(Document):
    """Représente un Élément Constitutif (unité d'enseignement)."""

    def after_insert(self):
        """Met à jour le compteur d'EC du cours parent."""
        self.update_course_ec_count()

    def after_delete(self):
        """Met à jour le compteur d'EC du cours parent."""
        self.update_course_ec_count()

    def update_course_ec_count(self):
        """Met à jour le nombre d'EC dans le cours."""
        if self.course:
            course = frappe.get_doc("CNTEMAD Course", self.course)
            course.update_ec_count()
            course.save()
