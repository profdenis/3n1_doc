import sys
from PySide6.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QLabel, QPushButton

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Compteur")
        self.setGeometry(100, 100, 300, 200)

        # Création du widget central
        central_widget = QWidget()
        layout = QVBoxLayout()

        # Label pour afficher le compteur
        self.counter_label = QLabel("0")
        self.counter_label.setStyleSheet("font-size: 24px;")

        # Bouton plus
        self.plus_button = QPushButton("+")
        self.plus_button.setEnabled(False)  # Désactivé pour l'instant

        # Ajout des widgets au layout
        layout.addWidget(self.counter_label)
        layout.addWidget(self.plus_button)

        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
