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
