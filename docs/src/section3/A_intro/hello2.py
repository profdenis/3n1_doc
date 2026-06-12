import sys
from PySide6.QtWidgets import QMainWindow, QPushButton, QApplication


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Ma Fenêtre")
        button = QPushButton("Cliquez-moi !")
        self.setCentralWidget(button)  # Ajoute le bouton au centre


app = QApplication(sys.argv)
window = MainWindow()
window.show()
sys.exit(app.exec())