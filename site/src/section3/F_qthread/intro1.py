import sys
import time
from PySide6.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QLabel


class BlockingExample(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()

        self.status_label = QLabel("Prêt")
        self.start_button = QPushButton("Démarrer tâche longue")
        self.counter_button = QPushButton("Cliquez-moi ! (0)")

        self.start_button.clicked.connect(self.blocking_task)
        self.counter_button.clicked.connect(self.increment_counter)

        layout.addWidget(self.status_label)
        layout.addWidget(self.start_button)
        layout.addWidget(self.counter_button)

        self.setLayout(layout)
        self.setWindowTitle("Exemple de blocage - MAUVAIS !")
        self.counter = 0

    def blocking_task(self):
        """Ceci bloque le thread principal - NE FAITES PAS ÇA !"""
        self.status_label.setText("Travail en cours... (L'application va se figer !)")

        # Simuler une tâche longue - ceci bloque tout !
        time.sleep(5)

        self.status_label.setText("Tâche terminée !")

    def increment_counter(self):
        self.counter += 1
        self.counter_button.setText(f"Cliquez-moi ! ({self.counter})")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = BlockingExample()
    window.show()
    sys.exit(app.exec())