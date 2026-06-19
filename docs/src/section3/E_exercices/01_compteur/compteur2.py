import sys
from PySide6.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QLabel, QPushButton

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Compteur")
        self.setGeometry(100, 100, 300, 200)
        self.counter = 0

        # Création du widget central
        central_widget = QWidget()
        layout = QVBoxLayout()

        # Label pour afficher le compteur
        self.counter_label = QLabel(str(self.counter))
        self.counter_label.setStyleSheet("font-size: 24px;")

        # Bouton plus
        self.plus_button = QPushButton("+")
        self.plus_button.clicked.connect(self.increment_counter)

        # Ajout des widgets au layout
        layout.addWidget(self.counter_label)
        layout.addWidget(self.plus_button)

        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)

    def increment_counter(self):
        """Incrémente le compteur et met à jour l'affichage."""
        self.counter += 1
        self.counter_label.setText(str(self.counter))

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
