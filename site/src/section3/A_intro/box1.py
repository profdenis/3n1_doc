import sys
from PySide6.QtWidgets import (
    QApplication, QWidget, QVBoxLayout,
    QLabel, QPushButton, QLineEdit, QCheckBox, QRadioButton
)


class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Exemple de QVBoxLayout")
        self.resize(300, 200)  # Taille initiale

        # Création du layout vertical
        layout = QVBoxLayout()

        # Ajout des widgets (empilés verticalement)
        layout.addWidget(QLabel("Ce texte est dans un QLabel"))
        layout.addWidget(QPushButton("Bouton cliquable"))
        layout.addWidget(QLineEdit("Champ de texte éditable"))
        layout.addWidget(QCheckBox("Case à cocher"))
        layout.addWidget(QRadioButton("Bouton radio"))

        # Application du layout à la fenêtre
        self.setLayout(layout)


app = QApplication(sys.argv)
window = MainWindow()
window.show()
sys.exit(app.exec())