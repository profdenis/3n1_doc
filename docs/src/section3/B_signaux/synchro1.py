import sys
from PySide6.QtWidgets import QApplication, QWidget, QSlider, QDial, QLabel, QVBoxLayout
from PySide6.QtCore import Qt

class LinkedControlsApp(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()

        # Création des contrôles avec une plage de 1-10
        self.slider = QSlider(Qt.Orientation.Horizontal)
        self.dial = QDial()
        self.label = QLabel("Valeur : 1")

        # Définition des plages
        self.slider.setRange(1, 10)
        self.dial.setRange(1, 10)

        # Ajout au layout
        layout.addWidget(self.slider)
        layout.addWidget(self.dial)
        layout.addWidget(self.label)
        self.setLayout(layout)

        # Connexion des signaux avec prévention des boucles
        self.slider.valueChanged.connect(self.update_controls)
        self.dial.valueChanged.connect(self.update_controls)

    def update_controls(self, value):
        # Prévention des boucles de signaux
        sender = self.sender()

        if isinstance(sender, QSlider):
            widget = self.dial
        else:
            widget = self.slider

        widget.blockSignals(True)
        widget.setValue(value)
        widget.blockSignals(False)

        self.label.setText(f"Valeur : {value}")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = LinkedControlsApp()
    window.setWindowTitle("Démonstration de contrôles synchronisés")
    window.show()
    sys.exit(app.exec())
