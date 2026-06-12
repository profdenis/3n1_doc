from PySide6.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QLabel
from PySide6.QtGui import QCursor
import sys

class CustomButton(QPushButton):
    def __init__(self, label, parent=None):
        super().__init__(label, parent)
        self.position_label = None

    def mousePressEvent(self, event):
        if self.position_label:
            pos = event.position()
            self.position_label.setText(f"Méthode de sous-classe : {pos.x():.0f}, {pos.y():.0f}")
        super().mousePressEvent(event)

class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Position de la souris sur QPushButton")
        self.resize(300, 200)

        layout = QVBoxLayout()

        # Label pour afficher la position
        self.position_label = QLabel("Cliquez sur un bouton pour voir la position")
        layout.addWidget(self.position_label)

        # Bouton utilisant la méthode QCursor
        self.cursor_button = QPushButton("Position via curseur")
        self.cursor_button.clicked.connect(self.show_cursor_position)
        layout.addWidget(self.cursor_button)

        # Bouton utilisant la méthode de sous-classe
        self.subclass_button = CustomButton("Méthode de sous-classe")
        self.subclass_button.position_label = self.position_label
        layout.addWidget(self.subclass_button)

        self.setLayout(layout)

    def show_cursor_position(self):
        pos = self.cursor_button.mapFromGlobal(QCursor.pos())
        self.position_label.setText(f"Méthode curseur : {pos.x()}, {pos.y()}")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
