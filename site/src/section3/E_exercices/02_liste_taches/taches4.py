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
