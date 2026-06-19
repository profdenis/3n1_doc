import sys
from PySide6.QtWidgets import (QApplication, QMainWindow, QWidget,
                               QVBoxLayout, QLabel, QPushButton, QSpinBox, QHBoxLayout)

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Compteur")
        self.setGeometry(100, 100, 300, 250)
        self.counter = 0
        self.step_size = 1

        # Création du widget central
        central_widget = QWidget()
        layout = QVBoxLayout()

        # Label pour afficher le compteur
        self.counter_label = QLabel(str(self.counter))
        self.counter_label.setStyleSheet("font-size: 24px;")

        # Boutons plus et moins
        button_layout = QHBoxLayout()
        self.minus_button = QPushButton("-")
        self.plus_button = QPushButton("+")
        self.minus_button.clicked.connect(self.decrement_counter)
        self.plus_button.clicked.connect(self.increment_counter)

        # Boîte de spin pour la taille de pas
        self.step_spinbox = QSpinBox()
        self.step_spinbox.setRange(1, 10)
        self.step_spinbox.setValue(self.step_size)
        self.step_spinbox.valueChanged.connect(self.update_step_size)

        button_layout.addWidget(self.minus_button)
        button_layout.addWidget(self.plus_button)
        layout.addWidget(self.counter_label)
        layout.addLayout(button_layout)
        layout.addWidget(QLabel("Taille de pas:"))
        layout.addWidget(self.step_spinbox)

        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)

    def update_step_size(self, value):
        """Met à jour la taille de pas."""
        self.step_size = value

    def increment_counter(self):
        """Incrémente le compteur et met à jour l'affichage."""
        self.counter += self.step_size
        self.counter_label.setText(str(self.counter))

    def decrement_counter(self):
        """Décrémente le compteur et met à jour l'affichage."""
        self.counter -= self.step_size
        self.counter_label.setText(str(self.counter))

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
