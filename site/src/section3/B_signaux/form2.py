import sys
from PySide6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QFormLayout, QLineEdit,
    QDateEdit, QCheckBox, QComboBox, QSpinBox, QPushButton, QVBoxLayout, QTextEdit, QListWidget, QSplitter
)
from PySide6.QtCore import QDate, Signal

class Person:
    def __init__(self, first_name, last_name, email, dob, is_student, gender, age, country):
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.dob = dob
        self.is_student = is_student
        self.gender = gender
        self.age = age
        self.country = country

    def __str__(self):
        # Version courte pour l'affichage dans la liste
        return f"{self.first_name} {self.last_name} ({self.email})"

    def __repr__(self):
        # Version détaillée pour l'affichage des détails
        return (f"Personne : {self.first_name} {self.last_name}\n"
                f"Email : {self.email}\n"
                f"Date de naissance : {self.dob.toString("yyyy-MM-dd")}\n"
                f"Étudiant(e) : {"Oui" if self.is_student else "Non"}\n"
                f"Genre : {self.gender}\n"
                f"Âge : {self.age}\n"
                f"Pays : {self.country}")

class PersonForm(QWidget):
    person_added = Signal(object)  # Signal à émettre lorsqu'une personne est ajoutée

    def __init__(self):
        super().__init__()
        self.setWindowTitle("Formulaire d'ajout de nouvelle personne")
        self.setup_ui()

    def setup_ui(self):
        layout = QFormLayout()

        # Champs du formulaire
        self.first_name_edit = QLineEdit()
        self.last_name_edit = QLineEdit()
        self.email_edit = QLineEdit()
        self.dob_edit = QDateEdit()
        self.dob_edit.setCalendarPopup(True)
        self.dob_edit.setDate(QDate.currentDate())
        self.student_checkbox = QCheckBox("Est étudiant(e)")
        self.gender_combo = QComboBox()
        self.gender_combo.addItems(["Sélectionner...", "Femme", "Homme", "Autre"])
        self.age_spin = QSpinBox()
        self.age_spin.setRange(0, 120)
        self.country_combo = QComboBox()
        self.country_combo.addItems(["Sélectionner...", "Canada", "États-Unis", "Autre"])

        # Ajout des champs au layout
        layout.addRow("Prénom :", self.first_name_edit)
        layout.addRow("Nom :", self.last_name_edit)
        layout.addRow("Email :", self.email_edit)
        layout.addRow("Date de naissance :", self.dob_edit)
        layout.addRow("Étudiant(e) :", self.student_checkbox)
        layout.addRow("Genre :", self.gender_combo)
        layout.addRow("Âge :", self.age_spin)
        layout.addRow("Pays :", self.country_combo)

        # Boutons
        button_layout = QVBoxLayout()
        self.add_button = QPushButton("Ajouter")
        self.cancel_button = QPushButton("Annuler")

        self.add_button.clicked.connect(self.create_person)
        self.cancel_button.clicked.connect(self.close)

        button_layout.addWidget(self.add_button)
        button_layout.addWidget(self.cancel_button)
        layout.addRow(button_layout)

        self.setLayout(layout)

    def create_person(self):
        # Création d'un objet Person à partir des données du formulaire
        person = Person(
            first_name=self.first_name_edit.text(),
            last_name=self.last_name_edit.text(),
            email=self.email_edit.text(),
            dob=self.dob_edit.date(),
            is_student=self.student_checkbox.isChecked(),
            gender=self.gender_combo.currentText(),
            age=self.age_spin.value(),
            country=self.country_combo.currentText()
        )
        self.person_added.emit(person)
        self.close()

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.people = []  # Liste d'objets Person
        self.setup_ui()

    def setup_ui(self):
        splitter = QSplitter()

        # Widget liste pour les personnes
        self.person_list = QListWidget()
        self.person_list.currentRowChanged.connect(self.display_person_details)

        # Affichage des détails (en lecture seule)
        self.person_detail = QTextEdit()
        self.person_detail.setReadOnly(True)

        splitter.addWidget(self.person_list)
        splitter.addWidget(self.person_detail)

        # Bouton Ajouter une personne au-dessus du splitter
        central_widget = QWidget()
        layout = QVBoxLayout()
        self.open_form_button = QPushButton("Ajouter une nouvelle personne")
        self.open_form_button.clicked.connect(self.show_form)
        layout.addWidget(self.open_form_button)
        layout.addWidget(splitter)
        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)
        self.setWindowTitle("Gestion des personnes")
        self.setMinimumSize(600, 400)

    def handle_new_person(self, person):
        self.people.append(person)
        self.person_list.addItem(str(person))

    def show_form(self):
        self.form = PersonForm()
        self.form.person_added.connect(self.handle_new_person)
        self.form.show()

    def display_person_details(self, row):
        if 0 <= row < len(self.people):
            self.person_detail.setPlainText(repr(self.people[row]))
        else:
            self.person_detail.clear()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())