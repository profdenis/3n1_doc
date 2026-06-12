import sys
from PySide6.QtWidgets import (
    QApplication, QWidget, QFormLayout, QLineEdit,
    QDateEdit, QCheckBox, QComboBox, QSpinBox, QPushButton
)
from PySide6.QtCore import QDate


class PersonForm(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Formulaire d'inscription - Nouvelle personne")

        # Création du layout de formulaire
        layout = QFormLayout()

        # Prénom
        self.first_name_edit = QLineEdit()
        layout.addRow("Prénom :", self.first_name_edit)

        # Nom
        self.last_name_edit = QLineEdit()
        layout.addRow("Nom :", self.last_name_edit)

        # Email
        self.email_edit = QLineEdit()
        layout.addRow("Email :", self.email_edit)

        # Date de naissance
        self.dob_edit = QDateEdit()
        self.dob_edit.setCalendarPopup(True)  # Active le calendrier pop-up
        self.dob_edit.setDate(QDate.currentDate())  # Date actuelle par défaut
        layout.addRow("Date de naissance :", self.dob_edit)

        # Étudiant (case à cocher)
        self.student_checkbox = QCheckBox("Est étudiant(e)")
        layout.addRow("Étudiant :", self.student_checkbox)

        # Genre (liste déroulante)
        self.gender_combo = QComboBox()
        self.gender_combo.addItems(["Sélectionner...", "Femme", "Homme", "Autre"])
        layout.addRow("Genre :", self.gender_combo)

        # Âge (champ numérique)
        self.age_spin = QSpinBox()
        self.age_spin.setRange(0, 120)  # Plage de 0 à 120 ans
        layout.addRow("Âge :", self.age_spin)

        # Pays (liste déroulante)
        self.country_combo = QComboBox()
        self.country_combo.addItems(["Sélectionner...", "Canada", "États-Unis", "Autre"])
        layout.addRow("Pays :", self.country_combo)

        # Bouton de soumission
        self.submit_button = QPushButton("Soumettre")
        layout.addRow(self.submit_button)

        self.setLayout(layout)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = PersonForm()
    window.show()
    sys.exit(app.exec())