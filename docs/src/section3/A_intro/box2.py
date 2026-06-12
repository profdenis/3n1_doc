import sys
from PySide6.QtWidgets import (
    QApplication, QWidget, QHBoxLayout,
    QComboBox, QListWidget, QSlider, QSpinBox, QDial
)
from PySide6.QtCore import Qt  # Pour l'orientation du slider


class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Exemple de QHBoxLayout")
        self.resize(500, 100)  # Taille initiale

        # Création du layout horizontal
        layout = QHBoxLayout()

        # Ajout des widgets (alignés horizontalement)
        combo = QComboBox()
        combo.addItems(["Option 1", "Option 2", "Option 3"])
        layout.addWidget(combo)

        list_widget = QListWidget()
        list_widget.addItems(["Élément A", "Élément B", "Élément C"])
        layout.addWidget(list_widget)

        slider = QSlider(Qt.Orientation.Horizontal)
        slider.setRange(0, 100)  # Valeurs de 0 à 100
        slider.setValue(50)  # Valeur initiale
        layout.addWidget(slider)

        spinbox = QSpinBox()
        spinbox.setRange(0, 100)
        spinbox.setValue(10)
        layout.addWidget(spinbox)

        dial = QDial()
        dial.setRange(0, 100)
        dial.setValue(25)
        layout.addWidget(dial)

        # Application du layout à la fenêtre
        self.setLayout(layout)


app = QApplication(sys.argv)
window = MainWindow()
window.show()
sys.exit(app.exec())