import sys
import random
from PySide6.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QLabel

class RandomNumberApp(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        self.layout = QVBoxLayout()

        self.label = QLabel("Cliquez sur le bouton pour obtenir un nombre aléatoire !", self)
        self.button = QPushButton("Générer un nombre aléatoire", self)

        self.layout.addWidget(self.label)
        self.layout.addWidget(self.button)
        self.setLayout(self.layout)

        # Connexion du signal 'clicked' du bouton au slot (fonction de gestion)
        self.button.clicked.connect(self.show_random_number)

    def show_random_number(self):
        number = random.randint(1, 100)
        self.label.setText(f"Nombre aléatoire : {number}")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = RandomNumberApp()
    window.setWindowTitle("Générateur de nombres aléatoires")
    window.show()
    sys.exit(app.exec())
