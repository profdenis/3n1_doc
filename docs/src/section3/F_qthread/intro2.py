import sys
import time
from PySide6.QtCore import QThread, Signal
from PySide6.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QLabel


class WorkerThread(QThread):
    """Thread séparé pour les tâches longues"""

    # Définir des signaux pour communiquer avec le thread principal
    progress_update = Signal(str)  # Envoyer des messages de statut
    task_finished = Signal(str)  # Envoyer un message de complétion

    def run(self):
        """Cette méthode s'exécute dans le thread séparé"""
        # Émettre un signal pour mettre à jour l'UI
        self.progress_update.emit("Démarrage de la tâche...")

        # Simuler une tâche longue avec des mises à jour de progression
        for i in range(5):
            time.sleep(1)  # Simuler du travail
            self.progress_update.emit(f"Travail en cours... Étape {i + 1}/5")

        # Tâche terminée
        self.task_finished.emit("Tâche terminée avec succès !")


class NonBlockingExample(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()
        self.worker_thread = None

    def init_ui(self):
        layout = QVBoxLayout()

        self.status_label = QLabel("Prêt")
        self.start_button = QPushButton("Démarrer tâche longue")
        self.counter_button = QPushButton("Cliquez-moi ! (0)")

        self.start_button.clicked.connect(self.start_background_task)
        self.counter_button.clicked.connect(self.increment_counter)

        layout.addWidget(self.status_label)
        layout.addWidget(self.start_button)
        layout.addWidget(self.counter_button)

        self.setLayout(layout)
        self.setWindowTitle("Exemple non-bloquant - BON !")
        self.counter = 0

    def start_background_task(self):
        """Démarrer la tâche dans un thread séparé"""
        # Désactiver le bouton pour empêcher plusieurs tâches
        self.start_button.setEnabled(False)

        # Créer et configurer le thread worker
        self.worker_thread = WorkerThread()

        # Connecter les signaux pour mettre à jour l'UI
        self.worker_thread.progress_update.connect(self.update_status)
        self.worker_thread.task_finished.connect(self.task_completed)

        # Démarrer le thread
        self.worker_thread.start()

    def update_status(self, message):
        """Appelé lorsque le thread worker envoie une mise à jour de progression"""
        self.status_label.setText(message)

    def task_completed(self, message):
        """Appelé lorsque le thread worker termine"""
        self.status_label.setText(message)
        self.start_button.setEnabled(True)  # Réactiver le bouton

        # Nettoyer le thread
        self.worker_thread = None

    def increment_counter(self):
        """Ceci fonctionne même pendant l'exécution de la tâche en arrière-plan !"""
        self.counter += 1
        self.counter_button.setText(f"Cliquez-moi ! ({self.counter})")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = NonBlockingExample()
    window.show()
    sys.exit(app.exec())
