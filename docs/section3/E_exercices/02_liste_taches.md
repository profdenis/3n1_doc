# **Exercice 2 : Gestionnaire de tâches (To-Do List)**

Cet exercice vous guide dans la construction étape par étape d'un gestionnaire de tâches complet avec **PySide6**.
Vous découvrirez comment manipuler une liste dynamique (`QListWidget`), valider les entrées utilisateur, associer des
cases à cocher et des priorités aux éléments, ajouter une barre de menus avec raccourcis clavier, persister vos données
en JSON avec des boîtes de dialogue de fichiers (`QFileDialog`), et gérer des événements avancés (touches clavier et
confirmation
de fermeture avec `closeEvent`).

---

## **Partie 1 : Créer le layout de base**

**Objectif :** Mettre en place la structure visuelle statique de l'application.

- Créez une nouvelle application PySide6 avec une fenêtre principale `QMainWindow` d'une taille initiale d'environ
  `450x400` pixels.
- Définissez un widget central muni d'un `QVBoxLayout`.
- Ajoutez une zone de saisie horizontale (`QHBoxLayout`) comprenant :
    - Un champ de texte `QLineEdit` pour saisir l'intitulé d'une nouvelle tâche, avec un texte indicatif
      (*placeholder*) : `"Nouvelle tâche à ajouter..."`.
    - Un bouton `QPushButton` avec le libellé « Ajouter ». Pour le moment, laissez ce bouton désactivé par défaut
      (`setEnabled(False)`).
- Ajoutez en dessous un composant de liste `QListWidget` qui servira à afficher les tâches.
- Ajoutez en bas de la fenêtre un bouton « Supprimer la sélection », également désactivé par défaut.
- Ne branchez aucune logique métier pour l'instant : assurez-vous simplement que les widgets s'affichent correctement et
  s'adaptent au redimensionnement de la fenêtre.

---

## **Partie 2 : Ajouter et supprimer des tâches avec validation**

**Objectif :** Rendre l'interface réactive et valider la saisie de l'utilisateur.

- Connectez le signal `textChanged` du champ de texte pour que le bouton « Ajouter » ne soit activé que lorsque le champ
  contient au moins un caractère non vide (en éliminant les espaces superflus avec `.strip()`).
- Connectez le clic sur « Ajouter » ainsi que l'appui sur la touche Entrée dans le champ de texte (`returnPressed`) à
  une méthode d'ajout de tâche.
- Dans cette méthode :
    - Créez un élément `QListWidgetItem` contenant le texte saisi.
    - Ajoutez-le au `QListWidget`.
    - Effacez le champ de texte et redonnez-lui le focus (`setFocus()`).
- Gérez la sélection dans la liste :
    - Écoutez le signal `itemSelectionChanged` de la liste pour activer le bouton « Supprimer la sélection » uniquement
      lorsqu'un élément est sélectionné.
- Connectez le bouton « Supprimer la sélection » pour retirer la ligne sélectionnée (`currentRow()`) à l'aide de
  `takeItem()`.

---

## **Partie 3 : Priorités et tâches à cocher**

**Objectif :** Enrichir les éléments de la liste avec des cases à cocher interactives et des niveaux de priorité.

- Ajoutez une boîte déroulante `QComboBox` entre le champ de saisie et le bouton « Ajouter » pour choisir la priorité de
  la tâche parmi : `"Basse"`, `"Moyenne"` et `"Haute"` (avec `"Moyenne"` sélectionnée par défaut).
- Lors de l'ajout d'une tâche :
    - Rendez l'élément cochable par l'utilisateur en combinant les drapeaux :
      `item.setFlags(item.flags() | Qt.ItemFlag.ItemIsUserCheckable)`.
    - Définissez son état initial à non coché : `item.setCheckState(Qt.CheckState.Unchecked)`.
    - Préfixez l'intitulé de la tâche par sa priorité (par exemple `[Haute] Faire les courses`) et conservez ces
      informations dans les données utilisateur de l'item via `item.setData(Qt.ItemDataRole.UserRole, ...)`.
- Connectez le signal `itemChanged` du `QListWidget` :
    - Lorsque la case d'une tâche est cochée (`Qt.CheckState.Checked`), barrez visuellement son texte
      (`font.setStrikeOut(True)`) et affichez-la en gris.
    - Lorsque la tâche est décochée, rétablissez la police normale et sa couleur d'origine.
    - *Astuce :* pensez à bloquer temporairement les signaux de la liste (`blockSignals(True)` / `blockSignals(False)`)
      lors de la modification de l'item dans le slot pour éviter tout déclenchement récursif.

---

## **Partie 4 : Barre de menus, raccourcis et boîte de dialogue de confirmation**

**Objectif :** Structurer l'application avec des menus standards, des raccourcis clavier et des dialogues de
confirmation `QMessageBox`.

- Ajoutez une barre de menus à la fenêtre :
    - Menu **« Fichier »** :
        - Action **« Nouvelle liste »** (raccourci `Ctrl+N`) : efface toutes les tâches de la liste après confirmation.
        - Séparateur horizontal.
        - Action **« Quitter »** (raccourci `Ctrl+Q`) : ferme l'application.
    - Menu **« Édition »** :
        - Action **« Supprimer la sélection »** (raccourci clavier `Delete` / `Suppr`) : connectée à la suppression de
          l'élément actif, activée uniquement lorsqu'une tâche est sélectionnée.
- Lorsque l'utilisateur déclenche « Nouvelle liste » et que la liste contient des tâches, affichez une boîte de dialogue
  de confirmation `QMessageBox.question` demandant confirmation (*« Voulez-vous vraiment effacer toutes les
  tâches ? »*). N'effacez la liste que si l'utilisateur valide (`QMessageBox.StandardButton.Yes`).
- Surchargez la méthode `keyPressEvent(self, event)` sur la fenêtre principale pour intercepter l'appui sur la touche
  `Delete` ou `Backspace` et supprimer directement l'élément sélectionné au clavier.

---

## **Partie 5 : Persistance des données en JSON et dialogue de fichiers**

**Objectif :** Sauvegarder et recharger les tâches depuis le disque avec `QFileDialog` et le module standard `json`.

- Dans le menu **« Fichier »**, ajoutez deux nouvelles actions :
    - Action **« Ouvrir... »** (raccourci `Ctrl+O`).
    - Action **« Enregistrer sous... »** (raccourci `Ctrl+S`).
- **Enregistrement :**
    - Ouvrez un sélecteur de fichier avec `QFileDialog.getSaveFileName` filtrant sur les fichiers JSON (`*.json`).
    - Parcourez tous les éléments du `QListWidget` et extrayez pour chacun son texte, sa priorité et son état coché
      (`completed: True/False`).
    - Écrivez ces données dans le fichier JSON avec `json.dump()`.
    - Affichez un message de succès avec `QMessageBox.information` ou d'erreur avec `QMessageBox.critical` en cas
      d'échec d'écriture.
- **Chargement :**
    - Ouvrez un sélecteur avec `QFileDialog.getOpenFileName`.
    - Lisez et désérialisez le fichier JSON.
    - Videz la liste existante et reconstruisez chaque élément avec sa case à cocher, sa priorité et son style barré
      s'il était déjà terminé.

---

## **Partie 6 : Filtrage dynamique, barre d'état et confirmation de fermeture**

**Objectif :** Offrir une expérience utilisateur soignée avec un filtrage sans perte, des statistiques en direct dans la
`QStatusBar` et la protection contre la fermeture accidentelle.

- **Filtrage en direct :**
    - Ajoutez une boîte déroulante `QComboBox` au-dessus de la liste avec trois options : `"Toutes les tâches"`,
      `"À faire (en cours)"`, et `"Terminées"`.
    - Lorsque le filtre change (ou lorsqu'une tâche est ajoutée/cochée), masquez ou affichez les éléments correspondants
      en appelant `item.setHidden(True/False)`. Notez que les éléments ne sont pas supprimés, seulement masqués
      visuellement.
- **Barre d'état (`QStatusBar`) :**
    - Initialisez la barre d'état de la fenêtre (`self.statusBar()`).
    - Créez une méthode de mise à jour affichant en temps réel le décompte :
      `"Total : X | À faire : Y | Terminées : Z"`.
    - Appelez cette méthode après chaque ajout, suppression, chargement ou changement d'état d'une tâche.
- **Confirmation de fermeture (`closeEvent`) :**
    - Surchargez la méthode `closeEvent(self, event)` de `QMainWindow`.
    - Si la liste contient au moins une tâche, affichez une boîte de dialogue `QMessageBox.question` demandant
      confirmation avant de quitter.
    - Appelez `event.accept()` si l'utilisateur confirme, ou `event.ignore()` pour annuler la fermeture et garder
      l'application ouverte.

---

**Défi bonus :**

- Ajoutez la possibilité de réordonner les tâches par glisser-déposer (*drag and drop*) interne avec
  `self.task_list.setDragDropMode(QAbstractItemView.DragDropMode.InternalMove)`.
- Ajoutez un champ de recherche textuel qui masque dynamiquement les tâches dont l'intitulé ne correspond pas à la
  recherche en cours.

---

**Instructions :**

- Pour chaque partie, partez de votre code de l'étape précédente et complétez-le avec les nouvelles fonctionnalités
  demandées.
- Testez chaque étape individuellement pour vous assurer du bon fonctionnement des signaux, des filtres et des
  dialogues.
- Conservez vos versions dans des fichiers séparés : `taches1.py`, `taches2.py`, `taches3.py`, `taches4.py`,
  `taches5.py`, `taches6.py`.

---

??? info "Exemple de solution pour la Partie 1"

    ```python title="taches1.py"
    import sys
    from PySide6.QtWidgets import (QApplication, QMainWindow, QWidget,
                                   QVBoxLayout, QHBoxLayout, QLineEdit,
                                   QPushButton, QListWidget)


    class MainWindow(QMainWindow):
        def __init__(self):
            super().__init__()
            self.setWindowTitle("Gestionnaire de tâches")
            self.resize(450, 400)

            # Widget central et layout principal
            central_widget = QWidget()
            layout = QVBoxLayout()

            # Zone de saisie d'une tâche
            input_layout = QHBoxLayout()
            self.task_input = QLineEdit()
            self.task_input.setPlaceholderText("Nouvelle tâche à ajouter...")
            self.add_button = QPushButton("Ajouter")
            self.add_button.setEnabled(False)  # Désactivé pour l'instant

            input_layout.addWidget(self.task_input)
            input_layout.addWidget(self.add_button)

            # Liste des tâches
            self.task_list = QListWidget()

            # Bouton d'action sur la sélection
            self.delete_button = QPushButton("Supprimer la sélection")
            self.delete_button.setEnabled(False)  # Désactivé pour l'instant

            # Assemblage des éléments dans le layout
            layout.addLayout(input_layout)
            layout.addWidget(self.task_list)
            layout.addWidget(self.delete_button)

            central_widget.setLayout(layout)
            self.setCentralWidget(central_widget)


    if __name__ == "__main__":
        app = QApplication(sys.argv)
        window = MainWindow()
        window.show()
        sys.exit(app.exec())
    ```

??? info "Exemple de solution pour la Partie 2"

    ```python title="taches2.py"
    import sys
    from PySide6.QtWidgets import (QApplication, QMainWindow, QWidget,
                                   QVBoxLayout, QHBoxLayout, QLineEdit,
                                   QPushButton, QListWidget, QListWidgetItem)


    class MainWindow(QMainWindow):
        def __init__(self):
            super().__init__()
            self.setWindowTitle("Gestionnaire de tâches")
            self.resize(450, 400)

            # Widget central et layout principal
            central_widget = QWidget()
            layout = QVBoxLayout()

            # Zone de saisie d'une tâche
            input_layout = QHBoxLayout()
            self.task_input = QLineEdit()
            self.task_input.setPlaceholderText("Nouvelle tâche à ajouter...")
            self.task_input.textChanged.connect(self.on_text_changed)
            self.task_input.returnPressed.connect(self.add_task)

            self.add_button = QPushButton("Ajouter")
            self.add_button.setEnabled(False)  # Désactivé tant que le champ est vide
            self.add_button.clicked.connect(self.add_task)

            input_layout.addWidget(self.task_input)
            input_layout.addWidget(self.add_button)

            # Liste des tâches
            self.task_list = QListWidget()
            self.task_list.itemSelectionChanged.connect(self.on_selection_changed)

            # Bouton de suppression de la sélection
            self.delete_button = QPushButton("Supprimer la sélection")
            self.delete_button.setEnabled(False)  # Désactivé tant qu'aucun item n'est sélectionné
            self.delete_button.clicked.connect(self.delete_selected_task)

            # Assemblage des éléments dans le layout
            layout.addLayout(input_layout)
            layout.addWidget(self.task_list)
            layout.addWidget(self.delete_button)

            central_widget.setLayout(layout)
            self.setCentralWidget(central_widget)

        def on_text_changed(self, text):
            """Active le bouton Ajouter uniquement si le texte n'est pas vide."""
            self.add_button.setEnabled(bool(text.strip()))

        def on_selection_changed(self):
            """Active le bouton Supprimer uniquement si une tâche est sélectionnée."""
            has_selection = len(self.task_list.selectedItems()) > 0
            self.delete_button.setEnabled(has_selection)

        def add_task(self):
            """Ajoute une nouvelle tâche à la liste."""
            text = self.task_input.text().strip()
            if text:
                item = QListWidgetItem(text)
                self.task_list.addItem(item)
                self.task_input.clear()
                self.task_input.setFocus()

        def delete_selected_task(self):
            """Supprime la tâche actuellement sélectionnée."""
            current_row = self.task_list.currentRow()
            if current_row >= 0:
                self.task_list.takeItem(current_row)


    if __name__ == "__main__":
        app = QApplication(sys.argv)
        window = MainWindow()
        window.show()
        sys.exit(app.exec())
    ```

??? info "Exemple de solution pour la Partie 3"

    ```python title="taches3.py"
    import sys
    from PySide6.QtWidgets import (QApplication, QMainWindow, QWidget,
                                   QVBoxLayout, QHBoxLayout, QLineEdit,
                                   QPushButton, QListWidget, QListWidgetItem,
                                   QComboBox)
    from PySide6.QtCore import Qt
    from PySide6.QtGui import QColor


    class MainWindow(QMainWindow):
        def __init__(self):
            super().__init__()
            self.setWindowTitle("Gestionnaire de tâches")
            self.resize(500, 420)

            # Widget central et layout principal
            central_widget = QWidget()
            layout = QVBoxLayout()

            # Zone de saisie d'une tâche avec priorité
            input_layout = QHBoxLayout()
            self.task_input = QLineEdit()
            self.task_input.setPlaceholderText("Nouvelle tâche à ajouter...")
            self.task_input.textChanged.connect(self.on_text_changed)
            self.task_input.returnPressed.connect(self.add_task)

            self.priority_combo = QComboBox()
            self.priority_combo.addItems(["Basse", "Moyenne", "Haute"])
            self.priority_combo.setCurrentText("Moyenne")

            self.add_button = QPushButton("Ajouter")
            self.add_button.setEnabled(False)  # Désactivé tant que le champ est vide
            self.add_button.clicked.connect(self.add_task)

            input_layout.addWidget(self.task_input)
            input_layout.addWidget(self.priority_combo)
            input_layout.addWidget(self.add_button)

            # Liste des tâches
            self.task_list = QListWidget()
            self.task_list.itemSelectionChanged.connect(self.on_selection_changed)
            self.task_list.itemChanged.connect(self.on_item_changed)

            # Bouton de suppression de la sélection
            self.delete_button = QPushButton("Supprimer la sélection")
            self.delete_button.setEnabled(False)  # Désactivé tant qu'aucun item n'est sélectionné
            self.delete_button.clicked.connect(self.delete_selected_task)

            # Assemblage des éléments dans le layout
            layout.addLayout(input_layout)
            layout.addWidget(self.task_list)
            layout.addWidget(self.delete_button)

            central_widget.setLayout(layout)
            self.setCentralWidget(central_widget)

        def on_text_changed(self, text):
            """Active le bouton Ajouter uniquement si le texte n'est pas vide."""
            self.add_button.setEnabled(bool(text.strip()))

        def on_selection_changed(self):
            """Active le bouton Supprimer uniquement si une tâche est sélectionnée."""
            has_selection = len(self.task_list.selectedItems()) > 0
            self.delete_button.setEnabled(has_selection)

        def add_task(self):
            """Ajoute une nouvelle tâche avec case à cocher et priorité."""
            text = self.task_input.text().strip()
            if text:
                priority = self.priority_combo.currentText()
                item = QListWidgetItem(f"[{priority}] {text}")

                # Rendre l'élément cochable
                item.setFlags(item.flags() | Qt.ItemFlag.ItemIsUserCheckable)
                item.setCheckState(Qt.CheckState.Unchecked)

                # Stocker les métadonnées (texte brut et priorité)
                item.setData(Qt.ItemDataRole.UserRole, {
                    "text": text,
                    "priority": priority
                })

                self.task_list.addItem(item)
                self.task_input.clear()
                self.task_input.setFocus()

        def on_item_changed(self, item):
            """Met à jour l'apparence de la tâche (barré/grisé) si cochée."""
            self.task_list.blockSignals(True)
            font = item.font()
            if item.checkState() == Qt.CheckState.Checked:
                font.setStrikeOut(True)
                item.setFont(font)
                item.setForeground(QColor("gray"))
            else:
                font.setStrikeOut(False)
                item.setFont(font)
                item.setForeground(QColor("black"))
            self.task_list.blockSignals(False)

        def delete_selected_task(self):
            """Supprime la tâche actuellement sélectionnée."""
            current_row = self.task_list.currentRow()
            if current_row >= 0:
                self.task_list.takeItem(current_row)


    if __name__ == "__main__":
        app = QApplication(sys.argv)
        window = MainWindow()
        window.show()
        sys.exit(app.exec())
    ```

??? info "Exemple de solution pour la Partie 4"

    ```python title="taches4.py"
    import sys
    from PySide6.QtWidgets import (QApplication, QMainWindow, QWidget,
                                   QVBoxLayout, QHBoxLayout, QLineEdit,
                                   QPushButton, QListWidget, QListWidgetItem,
                                   QComboBox, QMessageBox)
    from PySide6.QtCore import Qt
    from PySide6.QtGui import QColor, QAction, QKeySequence


    class MainWindow(QMainWindow):
        def __init__(self):
            super().__init__()
            self.setWindowTitle("Gestionnaire de tâches")
            self.resize(500, 420)

            # Création de la barre de menus
            self.create_menu_bar()

            # Widget central et layout principal
            central_widget = QWidget()
            layout = QVBoxLayout()

            # Zone de saisie d'une tâche avec priorité
            input_layout = QHBoxLayout()
            self.task_input = QLineEdit()
            self.task_input.setPlaceholderText("Nouvelle tâche à ajouter...")
            self.task_input.textChanged.connect(self.on_text_changed)
            self.task_input.returnPressed.connect(self.add_task)

            self.priority_combo = QComboBox()
            self.priority_combo.addItems(["Basse", "Moyenne", "Haute"])
            self.priority_combo.setCurrentText("Moyenne")

            self.add_button = QPushButton("Ajouter")
            self.add_button.setEnabled(False)  # Désactivé tant que le champ est vide
            self.add_button.clicked.connect(self.add_task)

            input_layout.addWidget(self.task_input)
            input_layout.addWidget(self.priority_combo)
            input_layout.addWidget(self.add_button)

            # Liste des tâches
            self.task_list = QListWidget()
            self.task_list.itemSelectionChanged.connect(self.on_selection_changed)
            self.task_list.itemChanged.connect(self.on_item_changed)

            # Bouton de suppression de la sélection
            self.delete_button = QPushButton("Supprimer la sélection")
            self.delete_button.setEnabled(False)  # Désactivé tant qu'aucun item n'est sélectionné
            self.delete_button.clicked.connect(self.delete_selected_task)

            # Assemblage des éléments dans le layout
            layout.addLayout(input_layout)
            layout.addWidget(self.task_list)
            layout.addWidget(self.delete_button)

            central_widget.setLayout(layout)
            self.setCentralWidget(central_widget)

        def create_menu_bar(self):
            """Configure la barre de menus et les actions."""
            menubar = self.menuBar()

            # Menu Fichier
            file_menu = menubar.addMenu("Fichier")

            new_action = QAction("Nouvelle liste", self)
            new_action.setShortcut(QKeySequence.StandardKey.New)
            new_action.triggered.connect(self.clear_all_tasks)
            file_menu.addAction(new_action)

            file_menu.addSeparator()

            quit_action = QAction("Quitter", self)
            quit_action.setShortcut(QKeySequence.StandardKey.Quit)
            quit_action.triggered.connect(self.close)
            file_menu.addAction(quit_action)

            # Menu Édition
            edit_menu = menubar.addMenu("Édition")
            self.delete_action = QAction("Supprimer la sélection", self)
            self.delete_action.setShortcut(QKeySequence.StandardKey.Delete)
            self.delete_action.setEnabled(False)
            self.delete_action.triggered.connect(self.delete_selected_task)
            edit_menu.addAction(self.delete_action)

        def on_text_changed(self, text):
            """Active le bouton Ajouter uniquement si le texte n'est pas vide."""
            self.add_button.setEnabled(bool(text.strip()))

        def on_selection_changed(self):
            """Active le bouton et l'action Supprimer uniquement si une tâche est sélectionnée."""
            has_selection = len(self.task_list.selectedItems()) > 0
            self.delete_button.setEnabled(has_selection)
            self.delete_action.setEnabled(has_selection)

        def add_task(self):
            """Ajoute une nouvelle tâche avec case à cocher et priorité."""
            text = self.task_input.text().strip()
            if text:
                priority = self.priority_combo.currentText()
                item = QListWidgetItem(f"[{priority}] {text}")

                # Rendre l'élément cochable
                item.setFlags(item.flags() | Qt.ItemFlag.ItemIsUserCheckable)
                item.setCheckState(Qt.CheckState.Unchecked)

                # Stocker les métadonnées (texte brut et priorité)
                item.setData(Qt.ItemDataRole.UserRole, {
                    "text": text,
                    "priority": priority
                })

                self.task_list.addItem(item)
                self.task_input.clear()
                self.task_input.setFocus()

        def on_item_changed(self, item):
            """Met à jour l'apparence de la tâche (barré/grisé) si cochée."""
            self.task_list.blockSignals(True)
            font = item.font()
            if item.checkState() == Qt.CheckState.Checked:
                font.setStrikeOut(True)
                item.setFont(font)
                item.setForeground(QColor("gray"))
            else:
                font.setStrikeOut(False)
                item.setFont(font)
                item.setForeground(QColor("black"))
            self.task_list.blockSignals(False)

        def delete_selected_task(self):
            """Supprime la tâche actuellement sélectionnée."""
            current_row = self.task_list.currentRow()
            if current_row >= 0:
                self.task_list.takeItem(current_row)

        def clear_all_tasks(self):
            """Efface toutes les tâches après confirmation de l'utilisateur."""
            if self.task_list.count() == 0:
                return

            reply = QMessageBox.question(
                self,
                "Confirmation",
                "Voulez-vous vraiment effacer toutes les tâches ?",
                QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
                QMessageBox.StandardButton.No
            )
            if reply == QMessageBox.StandardButton.Yes:
                self.task_list.clear()

        def keyPressEvent(self, event):
            """Gère la suppression rapide de l'élément sélectionné avec la touche Suppr."""
            if event.key() in (Qt.Key.Key_Delete, Qt.Key.Key_Backspace):
                if len(self.task_list.selectedItems()) > 0:
                    self.delete_selected_task()
                    event.accept()
                    return
            super().keyPressEvent(event)


    if __name__ == "__main__":
        app = QApplication(sys.argv)
        window = MainWindow()
        window.show()
        sys.exit(app.exec())
    ```

??? info "Exemple de solution pour la Partie 5"

    ```python title="taches5.py"
    import sys
    import json
    from PySide6.QtWidgets import (QApplication, QMainWindow, QWidget,
                                   QVBoxLayout, QHBoxLayout, QLineEdit,
                                   QPushButton, QListWidget, QListWidgetItem,
                                   QComboBox, QMessageBox, QFileDialog)
    from PySide6.QtCore import Qt
    from PySide6.QtGui import QColor, QAction, QKeySequence


    class MainWindow(QMainWindow):
        def __init__(self):
            super().__init__()
            self.setWindowTitle("Gestionnaire de tâches")
            self.resize(500, 420)

            # Création de la barre de menus
            self.create_menu_bar()

            # Widget central et layout principal
            central_widget = QWidget()
            layout = QVBoxLayout()

            # Zone de saisie d'une tâche avec priorité
            input_layout = QHBoxLayout()
            self.task_input = QLineEdit()
            self.task_input.setPlaceholderText("Nouvelle tâche à ajouter...")
            self.task_input.textChanged.connect(self.on_text_changed)
            self.task_input.returnPressed.connect(self.add_task)

            self.priority_combo = QComboBox()
            self.priority_combo.addItems(["Basse", "Moyenne", "Haute"])
            self.priority_combo.setCurrentText("Moyenne")

            self.add_button = QPushButton("Ajouter")
            self.add_button.setEnabled(False)  # Désactivé tant que le champ est vide
            self.add_button.clicked.connect(self.add_task)

            input_layout.addWidget(self.task_input)
            input_layout.addWidget(self.priority_combo)
            input_layout.addWidget(self.add_button)

            # Liste des tâches
            self.task_list = QListWidget()
            self.task_list.itemSelectionChanged.connect(self.on_selection_changed)
            self.task_list.itemChanged.connect(self.on_item_changed)

            # Bouton de suppression de la sélection
            self.delete_button = QPushButton("Supprimer la sélection")
            self.delete_button.setEnabled(False)  # Désactivé tant qu'aucun item n'est sélectionné
            self.delete_button.clicked.connect(self.delete_selected_task)

            # Assemblage des éléments dans le layout
            layout.addLayout(input_layout)
            layout.addWidget(self.task_list)
            layout.addWidget(self.delete_button)

            central_widget.setLayout(layout)
            self.setCentralWidget(central_widget)

        def create_menu_bar(self):
            """Configure la barre de menus et les actions."""
            menubar = self.menuBar()

            # Menu Fichier
            file_menu = menubar.addMenu("Fichier")

            new_action = QAction("Nouvelle liste", self)
            new_action.setShortcut(QKeySequence.StandardKey.New)
            new_action.triggered.connect(self.clear_all_tasks)
            file_menu.addAction(new_action)

            open_action = QAction("Ouvrir...", self)
            open_action.setShortcut(QKeySequence.StandardKey.Open)
            open_action.triggered.connect(self.open_file)
            file_menu.addAction(open_action)

            save_action = QAction("Enregistrer sous...", self)
            save_action.setShortcut(QKeySequence.StandardKey.Save)
            save_action.triggered.connect(self.save_file)
            file_menu.addAction(save_action)

            file_menu.addSeparator()

            quit_action = QAction("Quitter", self)
            quit_action.setShortcut(QKeySequence.StandardKey.Quit)
            quit_action.triggered.connect(self.close)
            file_menu.addAction(quit_action)

            # Menu Édition
            edit_menu = menubar.addMenu("Édition")
            self.delete_action = QAction("Supprimer la sélection", self)
            self.delete_action.setShortcut(QKeySequence.StandardKey.Delete)
            self.delete_action.setEnabled(False)
            self.delete_action.triggered.connect(self.delete_selected_task)
            edit_menu.addAction(self.delete_action)

        def on_text_changed(self, text):
            """Active le bouton Ajouter uniquement si le texte n'est pas vide."""
            self.add_button.setEnabled(bool(text.strip()))

        def on_selection_changed(self):
            """Active le bouton et l'action Supprimer uniquement si une tâche est sélectionnée."""
            has_selection = len(self.task_list.selectedItems()) > 0
            self.delete_button.setEnabled(has_selection)
            self.delete_action.setEnabled(has_selection)

        def add_task(self):
            """Ajoute une nouvelle tâche avec case à cocher et priorité."""
            text = self.task_input.text().strip()
            if text:
                priority = self.priority_combo.currentText()
                self.create_task_item(text, priority, completed=False)
                self.task_input.clear()
                self.task_input.setFocus()

        def create_task_item(self, text, priority, completed=False):
            """Crée et configure un item de tâche dans la liste."""
            item = QListWidgetItem(f"[{priority}] {text}")
            item.setFlags(item.flags() | Qt.ItemFlag.ItemIsUserCheckable)
            item.setCheckState(Qt.CheckState.Checked if completed else Qt.CheckState.Unchecked)

            item.setData(Qt.ItemDataRole.UserRole, {
                "text": text,
                "priority": priority
            })

            self.task_list.addItem(item)
            self.apply_item_style(item)
            return item

        def apply_item_style(self, item):
            """Applique le style visuel approprié selon l'état coché de la tâche."""
            self.task_list.blockSignals(True)
            font = item.font()
            if item.checkState() == Qt.CheckState.Checked:
                font.setStrikeOut(True)
                item.setFont(font)
                item.setForeground(QColor("gray"))
            else:
                font.setStrikeOut(False)
                item.setFont(font)
                item.setForeground(QColor("black"))
            self.task_list.blockSignals(False)

        def on_item_changed(self, item):
            """Met à jour l'apparence de la tâche lorsque la case est modifiée."""
            self.apply_item_style(item)

        def delete_selected_task(self):
            """Supprime la tâche actuellement sélectionnée."""
            current_row = self.task_list.currentRow()
            if current_row >= 0:
                self.task_list.takeItem(current_row)

        def clear_all_tasks(self):
            """Efface toutes les tâches après confirmation de l'utilisateur."""
            if self.task_list.count() == 0:
                return

            reply = QMessageBox.question(
                self,
                "Confirmation",
                "Voulez-vous vraiment effacer toutes les tâches ?",
                QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
                QMessageBox.StandardButton.No
            )
            if reply == QMessageBox.StandardButton.Yes:
                self.task_list.clear()

        def save_file(self):
            """Exporte les tâches actuelles dans un fichier JSON."""
            file_path, _ = QFileDialog.getSaveFileName(
                self, "Enregistrer les tâches", "", "Fichiers JSON (*.json);;Tous les fichiers (*)"
            )
            if not file_path:
                return

            tasks_data = []
            for i in range(self.task_list.count()):
                item = self.task_list.item(i)
                meta = item.data(Qt.ItemDataRole.UserRole) or {}
                tasks_data.append({
                    "text": meta.get("text", item.text()),
                    "priority": meta.get("priority", "Moyenne"),
                    "completed": item.checkState() == Qt.CheckState.Checked
                })

            try:
                with open(file_path, "w", encoding="utf-8") as file:
                    json.dump(tasks_data, file, indent=2, ensure_ascii=False)
                QMessageBox.information(self, "Succès", "Tâches enregistrées avec succès !")
            except Exception as e:
                QMessageBox.critical(self, "Erreur", f"Impossible d'enregistrer le fichier :\n{e}")

        def open_file(self):
            """Charge des tâches depuis un fichier JSON."""
            file_path, _ = QFileDialog.getOpenFileName(
                self, "Ouvrir un fichier de tâches", "", "Fichiers JSON (*.json);;Tous les fichiers (*)"
            )
            if not file_path:
                return

            try:
                with open(file_path, "r", encoding="utf-8") as file:
                    tasks_data = json.load(file)

                self.task_list.clear()
                for task in tasks_data:
                    text = task.get("text", "")
                    priority = task.get("priority", "Moyenne")
                    completed = task.get("completed", False)
                    self.create_task_item(text, priority, completed)

            except Exception as e:
                QMessageBox.critical(self, "Erreur", f"Impossible de charger le fichier :\n{e}")

        def keyPressEvent(self, event):
            """Gère la suppression rapide de l'élément sélectionné avec la touche Suppr."""
            if event.key() in (Qt.Key.Key_Delete, Qt.Key.Key_Backspace):
                if len(self.task_list.selectedItems()) > 0:
                    self.delete_selected_task()
                    event.accept()
                    return
            super().keyPressEvent(event)


    if __name__ == "__main__":
        app = QApplication(sys.argv)
        window = MainWindow()
        window.show()
        sys.exit(app.exec())
    ```

??? info "Exemple de solution pour la Partie 6"

    ```python title="taches6.py"
    import sys
    import json
    from PySide6.QtWidgets import (QApplication, QMainWindow, QWidget,
                                   QVBoxLayout, QHBoxLayout, QLineEdit,
                                   QPushButton, QListWidget, QListWidgetItem,
                                   QComboBox, QMessageBox, QFileDialog, QLabel)
    from PySide6.QtCore import Qt
    from PySide6.QtGui import QColor, QAction, QKeySequence


    class MainWindow(QMainWindow):
        def __init__(self):
            super().__init__()
            self.setWindowTitle("Gestionnaire de tâches")
            self.resize(520, 480)

            # Création de la barre de menus et de la barre d'état
            self.create_menu_bar()
            self.statusBar()  # Initialisation de la barre d'état

            # Widget central et layout principal
            central_widget = QWidget()
            layout = QVBoxLayout()

            # Zone de saisie d'une tâche avec priorité
            input_layout = QHBoxLayout()
            self.task_input = QLineEdit()
            self.task_input.setPlaceholderText("Nouvelle tâche à ajouter...")
            self.task_input.textChanged.connect(self.on_text_changed)
            self.task_input.returnPressed.connect(self.add_task)

            self.priority_combo = QComboBox()
            self.priority_combo.addItems(["Basse", "Moyenne", "Haute"])
            self.priority_combo.setCurrentText("Moyenne")

            self.add_button = QPushButton("Ajouter")
            self.add_button.setEnabled(False)  # Désactivé tant que le champ est vide
            self.add_button.clicked.connect(self.add_task)

            input_layout.addWidget(self.task_input)
            input_layout.addWidget(self.priority_combo)
            input_layout.addWidget(self.add_button)

            # Zone de filtrage des tâches
            filter_layout = QHBoxLayout()
            filter_layout.addWidget(QLabel("Filtrer :"))
            self.filter_combo = QComboBox()
            self.filter_combo.addItems(["Toutes les tâches", "À faire (en cours)", "Terminées"])
            self.filter_combo.currentTextChanged.connect(self.apply_filter)
            filter_layout.addWidget(self.filter_combo)
            filter_layout.addStretch()

            # Liste des tâches
            self.task_list = QListWidget()
            self.task_list.itemSelectionChanged.connect(self.on_selection_changed)
            self.task_list.itemChanged.connect(self.on_item_changed)

            # Bouton de suppression de la sélection
            self.delete_button = QPushButton("Supprimer la sélection")
            self.delete_button.setEnabled(False)  # Désactivé tant qu'aucun item n'est sélectionné
            self.delete_button.clicked.connect(self.delete_selected_task)

            # Assemblage des éléments dans le layout
            layout.addLayout(input_layout)
            layout.addLayout(filter_layout)
            layout.addWidget(self.task_list)
            layout.addWidget(self.delete_button)

            central_widget.setLayout(layout)
            self.setCentralWidget(central_widget)

            # Mise à jour initiale de la barre d'état
            self.update_status_bar()

        def create_menu_bar(self):
            """Configure la barre de menus et les actions."""
            menubar = self.menuBar()

            # Menu Fichier
            file_menu = menubar.addMenu("Fichier")

            new_action = QAction("Nouvelle liste", self)
            new_action.setShortcut(QKeySequence.StandardKey.New)
            new_action.triggered.connect(self.clear_all_tasks)
            file_menu.addAction(new_action)

            open_action = QAction("Ouvrir...", self)
            open_action.setShortcut(QKeySequence.StandardKey.Open)
            open_action.triggered.connect(self.open_file)
            file_menu.addAction(open_action)

            save_action = QAction("Enregistrer sous...", self)
            save_action.setShortcut(QKeySequence.StandardKey.Save)
            save_action.triggered.connect(self.save_file)
            file_menu.addAction(save_action)

            file_menu.addSeparator()

            quit_action = QAction("Quitter", self)
            quit_action.setShortcut(QKeySequence.StandardKey.Quit)
            quit_action.triggered.connect(self.close)
            file_menu.addAction(quit_action)

            # Menu Édition
            edit_menu = menubar.addMenu("Édition")
            self.delete_action = QAction("Supprimer la sélection", self)
            self.delete_action.setShortcut(QKeySequence.StandardKey.Delete)
            self.delete_action.setEnabled(False)
            self.delete_action.triggered.connect(self.delete_selected_task)
            edit_menu.addAction(self.delete_action)

        def on_text_changed(self, text):
            """Active le bouton Ajouter uniquement si le texte n'est pas vide."""
            self.add_button.setEnabled(bool(text.strip()))

        def on_selection_changed(self):
            """Active le bouton et l'action Supprimer uniquement si une tâche est sélectionnée."""
            has_selection = len(self.task_list.selectedItems()) > 0
            self.delete_button.setEnabled(has_selection)
            self.delete_action.setEnabled(has_selection)

        def add_task(self):
            """Ajoute une nouvelle tâche avec case à cocher et priorité."""
            text = self.task_input.text().strip()
            if text:
                priority = self.priority_combo.currentText()
                self.create_task_item(text, priority, completed=False)
                self.task_input.clear()
                self.task_input.setFocus()
                self.apply_filter()
                self.update_status_bar()

        def create_task_item(self, text, priority, completed=False):
            """Crée et configure un item de tâche dans la liste."""
            item = QListWidgetItem(f"[{priority}] {text}")
            item.setFlags(item.flags() | Qt.ItemFlag.ItemIsUserCheckable)
            item.setCheckState(Qt.CheckState.Checked if completed else Qt.CheckState.Unchecked)

            item.setData(Qt.ItemDataRole.UserRole, {
                "text": text,
                "priority": priority
            })

            self.task_list.addItem(item)
            self.apply_item_style(item)
            return item

        def apply_item_style(self, item):
            """Applique le style visuel approprié selon l'état coché de la tâche."""
            self.task_list.blockSignals(True)
            font = item.font()
            if item.checkState() == Qt.CheckState.Checked:
                font.setStrikeOut(True)
                item.setFont(font)
                item.setForeground(QColor("gray"))
            else:
                font.setStrikeOut(False)
                item.setFont(font)
                item.setForeground(QColor("black"))
            self.task_list.blockSignals(False)

        def on_item_changed(self, item):
            """Met à jour l'apparence, applique le filtre et met à jour le statut."""
            self.apply_item_style(item)
            self.apply_filter()
            self.update_status_bar()

        def apply_filter(self):
            """Masque ou affiche les tâches selon le filtre sélectionné."""
            current_filter = self.filter_combo.currentText()
            for i in range(self.task_list.count()):
                item = self.task_list.item(i)
                is_completed = (item.checkState() == Qt.CheckState.Checked)

                if current_filter == "À faire (en cours)":
                    item.setHidden(is_completed)
                elif current_filter == "Terminées":
                    item.setHidden(not is_completed)
                else:  # "Toutes les tâches"
                    item.setHidden(False)

        def update_status_bar(self):
            """Met à jour les statistiques de tâches dans la barre d'état."""
            total = self.task_list.count()
            completed = sum(
                1 for i in range(total)
                if self.task_list.item(i).checkState() == Qt.CheckState.Checked
            )
            pending = total - completed
            self.statusBar().showMessage(
                f"Total : {total} | À faire : {pending} | Terminées : {completed}"
            )

        def delete_selected_task(self):
            """Supprime la tâche actuellement sélectionnée."""
            current_row = self.task_list.currentRow()
            if current_row >= 0:
                self.task_list.takeItem(current_row)
                self.update_status_bar()

        def clear_all_tasks(self):
            """Efface toutes les tâches après confirmation de l'utilisateur."""
            if self.task_list.count() == 0:
                return

            reply = QMessageBox.question(
                self,
                "Confirmation",
                "Voulez-vous vraiment effacer toutes les tâches ?",
                QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
                QMessageBox.StandardButton.No
            )
            if reply == QMessageBox.StandardButton.Yes:
                self.task_list.clear()
                self.update_status_bar()

        def save_file(self):
            """Exporte les tâches actuelles dans un fichier JSON."""
            file_path, _ = QFileDialog.getSaveFileName(
                self, "Enregistrer les tâches", "", "Fichiers JSON (*.json);;Tous les fichiers (*)"
            )
            if not file_path:
                return

            tasks_data = []
            for i in range(self.task_list.count()):
                item = self.task_list.item(i)
                meta = item.data(Qt.ItemDataRole.UserRole) or {}
                tasks_data.append({
                    "text": meta.get("text", item.text()),
                    "priority": meta.get("priority", "Moyenne"),
                    "completed": item.checkState() == Qt.CheckState.Checked
                })

            try:
                with open(file_path, "w", encoding="utf-8") as file:
                    json.dump(tasks_data, file, indent=2, ensure_ascii=False)
                QMessageBox.information(self, "Succès", "Tâches enregistrées avec succès !")
            except Exception as e:
                QMessageBox.critical(self, "Erreur", f"Impossible d'enregistrer le fichier :\n{e}")

        def open_file(self):
            """Charge des tâches depuis un fichier JSON."""
            file_path, _ = QFileDialog.getOpenFileName(
                self, "Ouvrir un fichier de tâches", "", "Fichiers JSON (*.json);;Tous les fichiers (*)"
            )
            if not file_path:
                return

            try:
                with open(file_path, "r", encoding="utf-8") as file:
                    tasks_data = json.load(file)

                self.task_list.clear()
                for task in tasks_data:
                    text = task.get("text", "")
                    priority = task.get("priority", "Moyenne")
                    completed = task.get("completed", False)
                    self.create_task_item(text, priority, completed)

                self.apply_filter()
                self.update_status_bar()
            except Exception as e:
                QMessageBox.critical(self, "Erreur", f"Impossible de charger le fichier :\n{e}")

        def keyPressEvent(self, event):
            """Gère la suppression rapide de l'élément sélectionné avec la touche Suppr."""
            if event.key() in (Qt.Key.Key_Delete, Qt.Key.Key_Backspace):
                if len(self.task_list.selectedItems()) > 0:
                    self.delete_selected_task()
                    event.accept()
                    return
            super().keyPressEvent(event)

        def closeEvent(self, event):
            """Demande confirmation avant de quitter si des tâches existent."""
            if self.task_list.count() > 0:
                reply = QMessageBox.question(
                    self,
                    "Quitter l'application",
                    "Voulez-vous vraiment quitter le gestionnaire de tâches ?",
                    QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
                    QMessageBox.StandardButton.No
                )
                if reply == QMessageBox.StandardButton.Yes:
                    event.accept()
                else:
                    event.ignore()
            else:
                event.accept()


    if __name__ == "__main__":
        app = QApplication(sys.argv)
        window = MainWindow()
        window.show()
        sys.exit(app.exec())
    ```

---

Cet exercice illustre la manipulation dynamique de collections de widgets (`QListWidget`), la mise en forme
conditionnelle,
l'intégration de menus avec raccourcis, la persistance dans des fichiers au format JSON, et l'interception d'événements
clavier et de fermeture.
