# **4. Soumission des données de formulaire**

Voici une version modifiée de l'exemple précédent de layout de formulaire, cette fois avec des signaux pour réagir aux clics sur les boutons :

```python
import sys
from PySide6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QFormLayout, QLineEdit,
    QDateEdit, QCheckBox, QComboBox, QSpinBox, QPushButton, QLabel, QVBoxLayout
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
        return (f"Personne : {self.first_name} {self.last_name}\n"
                f"Email : {self.email}\n"
                f"Date de naissance : {self.dob.toString('yyyy-MM-dd')}\n"
                f"Étudiant(e) : {'Oui' if self.is_student else 'Non'}\n"
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
        self.person = None
        self.setup_ui()

    def setup_ui(self):
        central_widget = QWidget()
        layout = QVBoxLayout()

        # Bouton Ajouter une personne
        self.open_form_button = QPushButton("Ajouter une nouvelle personne")
        self.open_form_button.clicked.connect(self.show_form)

        # Label d'affichage
        self.person_label = QLabel("Aucune personne ajoutée pour l'instant")

        layout.addWidget(self.open_form_button)
        layout.addWidget(self.person_label)
        central_widget.setLayout(layout)

        self.setCentralWidget(central_widget)
        self.setWindowTitle("Gestion des personnes")
        self.setMinimumSize(400, 300)

    def show_form(self):
        self.form = PersonForm()
        self.form.person_added.connect(self.handle_new_person)
        self.form.show()

    def handle_new_person(self, person):
        self.person = person
        self.person_label.setText(str(person))

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
```

### Modifications et fonctionnalités clés

1. **Structure de la fenêtre principale** :
   - Ajout d'une classe `MainWindow` comme interface principale
   - Contient un bouton "Ajouter une nouvelle personne" et un label d'affichage

2. **Logique d'affichage du formulaire** :
   - Le formulaire n'apparaît que lorsque l'on clique sur "Ajouter une nouvelle personne"
   - Utilise `show()` au lieu de `exec()` pour un dialogue non modal

3. **Classe Person** :
   - Définie avec tous les champs du formulaire comme attributs
   - Inclut une méthode `__str__` pour le formatage d'affichage

4. **Gestion des signaux** :
   - `PersonForm` émet un signal `person_added` avec l'objet Person
   - `MainWindow` se connecte à ce signal pour mettre à jour l'affichage

5. **Fonctionnalité des boutons** :
   - Le bouton Ajouter crée un objet Person et ferme le formulaire
   - Le bouton Annuler ferme immédiatement le formulaire
   - Les deux boutons effacent le formulaire lors de la prochaine ouverture (à cause d'une nouvelle instance)

6. **Flux de données** :
   - Les données du formulaire sont encapsulées dans un objet Person
   - La fenêtre principale stocke l'instance Person la plus récente
   - Le label se met à jour automatiquement lorsqu'une nouvelle personne est ajoutée

### Flux d'utilisation

1. Lancez l'application pour voir la fenêtre principale
2. Cliquez sur "Ajouter une nouvelle personne" pour ouvrir le formulaire
3. Remplissez le formulaire et cliquez :
   - **Ajouter** : Crée la personne, met à jour le label, ferme le formulaire
   - **Annuler** : Ferme le formulaire sans sauvegarder
4. Les détails de la nouvelle personne apparaissent dans le label de la fenêtre principale après l'ajout

Cette implémentation démontre une bonne séparation des préoccupations entre le formulaire et la fenêtre principale, tout en maintenant un flux de données propre grâce au mécanisme signal/slot de PySide6.

## Une autre version avec une liste d'objets Person

### Résumé des modifications

#### 1. Classe Person

- **Affichage court** : Implémentez `__str__` pour retourner un résumé bref (par exemple, `"Prénom Nom (email)"`) à utiliser dans la liste.
- **Affichage détaillé** : Déplacez la chaîne détaillée originale vers `__repr__` pour afficher les détails complets à droite.

#### 2. Classe MainWindow

- **Liste de personnes** : Remplacez l'attribut unique `person` par une liste `self.people` pour stocker plusieurs objets `Person`.
- **Disposition UI** : Utilisez un `QSplitter` comme layout principal, avec :
  - Un `QListWidget` à gauche pour afficher la liste des personnes (en utilisant `str(person)`).
  - Un `QTextEdit` (en lecture seule) à droite pour afficher les détails (`repr(person)`).
- **Ajout de personnes** : Lorsqu'une nouvelle personne est ajoutée, ajoutez-la à `self.people` et ajoutez sa chaîne au `QListWidget`.
- **Gestion de la sélection** : Connectez le signal `currentRowChanged` du `QListWidget` à une méthode qui affiche les détails de la personne correspondante dans le `QTextEdit`.

#### 3. Autres

- **Aucun changement** nécessaire dans la logique du formulaire ou la création de personnes, sauf éventuellement l'effacement du formulaire après ajout.

### Résultat

Vous avez maintenant une interface maître-détail :

- Le côté gauche liste toutes les personnes dans l'application.
- Le côté droit affiche les informations détaillées pour la personne sélectionnée.
- De nouvelles personnes peuvent être ajoutées et apparaîtront immédiatement dans la liste.

```python
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
                f"Date de naissance : {self.dob.toString('yyyy-MM-dd')}\n"
                f"Étudiant(e) : {'Oui' if self.is_student else 'Non'}\n"
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
```