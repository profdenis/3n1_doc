import sys
import random
from PySide6.QtWidgets import (
    QApplication,
    QMainWindow,
    QPushButton,
    QLabel,
    QVBoxLayout,
    QWidget  # Nécessaire pour le conteneur central
)
from PySide6.QtCore import Qt

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Générateur de nombres")
        self.label = QLabel("Appuyez sur le bouton !", alignment=Qt.AlignmentFlag.AlignCenter)
        self.button = QPushButton("Générer un nombre")
        self.button.clicked.connect(self.update_label)

        # Création d'un conteneur central avec layout
        central_widget = QWidget()
        self.setCentralWidget(central_widget)  # Définir le widget central

        # Configuration du layout vertical
        layout = QVBoxLayout(central_widget)
        layout.addWidget(self.label)    # Ajoute le label en haut
        layout.addWidget(self.button)   # Ajoute le bouton en dessous

    def update_label(self):
        random_number = random.randint(0, 100)
        self.label.setText(f"Nombre généré : {random_number}")

app = QApplication(sys.argv)
window = MainWindow()
window.resize(300, 200)  # Taille de la fenêtre
window.show()
sys.exit(app.exec())
