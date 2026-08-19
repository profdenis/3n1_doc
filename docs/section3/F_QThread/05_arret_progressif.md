# Fermeture progressive

L'approche de fermeture progressive dans `closeEvent` est la méthode professionnelle pour gérer la fermeture d'une
application. Voici ce que l'exemple démontre :

## Le processus de fermeture en trois étapes :

### **Étape 1 : Annulation coopérative (3 secondes)**

```python
self.worker_thread.cancel()  # Définir le drapeau d'annulation
if self.worker_thread.wait(3000):  # Attendre 3 secondes
    # Le thread s'est arrêté proprement - nous avons terminé !
```

### **Étape 2 : Signal de sortie (2 secondes)**

```python
self.worker_thread.quit()  # Envoyer le signal de sortie à la boucle d'événements
if self.worker_thread.wait(2000):  # Attendre 2 secondes
    # Le thread a répondu au signal de sortie - nous avons terminé !
```

### **Étape 3 : Choix utilisateur + Terminaison forcée**

```python
# Demander la permission à l'utilisateur en premier !
reply = QMessageBox.question(self, "Terminer de force ?", ...)

if reply == Yes:
    self.worker_thread.terminate()  # Tuer de force
    self.worker_thread.wait(1000)  # Attendre le nettoyage
```

## Points clés :

### **1. Temps de réponse progressifs**

- **3 secondes** pour l'annulation coopérative (le plus long, le plus doux)
- **2 secondes** pour le signal de sortie (plus court, plus urgent)
- **1 seconde** pour le nettoyage après terminaison (juste le temps de nettoyage)

### **2. Implication de l'utilisateur**

- Ne terminez pas de force sans demander à l'utilisateur
- Les utilisateurs doivent comprendre les conséquences
- Donnez-leur la possibilité d'annuler la fermeture et d'attendre

### **3. Gestion correcte des événements**

```python
event.accept()  # Autoriser la fermeture
event.ignore()  # Annuler la fermeture
```

### **4. Gestion de l'état**

- Suivre `shutdown_in_progress` pour éviter les doublons dans le journal
- Continuer à journaliser tout au long du processus
- Utiliser `QApplication.processEvents()` pour garantir les mises à jour de l'UI

## Pourquoi cette approche est supérieure :

**Pour les threads bien comportés :**

- L'étape 1 (coopérative) réussit → fermeture rapide et propre
- Aucune terminaison forcée nécessaire

**Pour les threads modérément problématiques :**

- L'étape 1 échoue, mais l'étape 2 (signal de sortie) réussit
- Évite toujours la terminaison forcée dangereuse

**Pour les threads vraiment bloqués :**

- Les deux étapes échouent → l'utilisateur peut décider
- L'utilisateur comprend le risque avant la terminaison forcée
- L'application ne reste pas bloquée pour toujours

## Applications du monde réel :

Ce schéma est essentiel pour :

- **Applications de traitement de fichiers** (ne pas corrompre les fichiers)
- **Applications réseau** (fermer les connexions proprement)
- **Outils d'analyse de données** (enregistrer les résultats intermédiaires)
- **Tout logiciel professionnel** (les utilisateurs s'attendent à une fermeture gracieuse)

L'exemple montre à la fois des workers coopératifs et têtus, donc nous pouvons tester les deux scénarios et voir comment
l'approche progressive gère chaque cas de manière appropriée.

## Code complet

```python title="arret.py"
import sys
import time
from PySide6.QtCore import QThread, Signal, QTimer
from PySide6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout,
                               QPushButton, QLabel, QTextEdit, QProgressBar,
                               QMessageBox)


class LongRunningWorker(QThread):
    """Thread worker qui peut être annulé de manière coopérative"""

    progress_update = Signal(int)
    status_update = Signal(str)
    log_message = Signal(str)

    def __init__(self, task_duration=20):
        super().__init__()
        self.task_duration = task_duration
        self.is_cancelled = False

    def cancel(self):
        """Demander une annulation coopérative"""
        self.is_cancelled = True

    def run(self):
        """Tâche longue qui vérifie l'annulation"""
        self.log_message.emit("Thread worker démarré")

        for i in range(self.task_duration):
            # Vérifier la demande d'annulation
            if self.is_cancelled:
                self.log_message.emit("Thread worker annulé de manière coopérative")
                self.status_update.emit("Tâche annulée")
                return

            # Simuler le travail
            time.sleep(1)
            progress = int(((i + 1) / self.task_duration) * 100)
            self.progress_update.emit(progress)
            self.status_update.emit(f"Travail en cours... {i + 1}/{self.task_duration}")

            if i % 3 == 0:  # Journaliser tous les quelques étapes
                self.log_message.emit(f"Étape {i + 1} terminée")

        self.log_message.emit("Thread worker terminé normalement")
        self.status_update.emit("Tâche terminée !")


class GracefulShutdownApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.worker_thread = None
        self.shutdown_in_progress = False
        self.init_ui()

    def init_ui(self):
        # Créer le widget central
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout(central_widget)

        # Titre
        title = QLabel("Démonstration de fermeture gracieuse")
        title.setStyleSheet("font-size: 16px; font-weight: bold; margin: 10px;")
        layout.addWidget(title)

        # Affichage du statut
        self.status_label = QLabel("Prêt à démarrer la tâche")
        layout.addWidget(self.status_label)

        # Barre de progression
        self.progress_bar = QProgressBar()
        self.progress_bar.setVisible(False)
        layout.addWidget(self.progress_bar)

        # Boutons de contrôle
        self.start_button = QPushButton("Démarrer une longue tâche (20 secondes)")
        self.cancel_button = QPushButton("Annuler la tâche")
        self.cancel_button.setEnabled(False)

        self.start_button.clicked.connect(self.start_task)
        self.cancel_button.clicked.connect(self.cancel_task)

        layout.addWidget(self.start_button)
        layout.addWidget(self.cancel_button)

        # Instructions
        instructions = QLabel("""
Instructions :
1. Cliquez sur 'Démarrer une longue tâche' pour commencer une tâche d'arrière-plan de 20 secondes
2. Essayez de fermer la fenêtre pendant que la tâche s'exécute
3. Observez le processus de fermeture gracieuse dans le journal ci-dessous
        """)
        instructions.setStyleSheet("margin: 10px; padding: 10px;")
        layout.addWidget(instructions)

        # Affichage du journal
        log_label = QLabel("Journal du processus de fermeture :")
        layout.addWidget(log_label)

        self.log_display = QTextEdit()
        self.log_display.setMaximumHeight(200)
        self.log_display.setReadOnly(True)
        layout.addWidget(self.log_display)

        # Paramètres de la fenêtre
        self.setWindowTitle("Exemple de fermeture gracieuse")
        self.setGeometry(300, 300, 600, 500)

    def start_task(self):
        """Démarrer la tâche d'arrière-plan"""
        self.log_display.clear()
        self.add_log_message("=== Démarrage d'une nouvelle tâche ===")

        # Mettre à jour l'UI
        self.start_button.setEnabled(False)
        self.cancel_button.setEnabled(True)
        self.progress_bar.setVisible(True)
        self.progress_bar.setValue(0)

        # Créer et démarrer le worker
        self.worker_thread = LongRunningWorker()
        # self.worker_thread = StubbornWorker()  # Décommenter pour tester avec un worker têtu qui ignore l'annulation

        # Connecter les signaux
        self.worker_thread.progress_update.connect(self.update_progress)
        self.worker_thread.status_update.connect(self.update_status)
        self.worker_thread.log_message.connect(self.add_log_message)
        self.worker_thread.finished.connect(self.task_finished)

        # Démarrer le thread
        self.worker_thread.start()

    def cancel_task(self):
        """Annuler la tâche en cours"""
        if self.worker_thread and self.worker_thread.isRunning():
            self.add_log_message("Demande d'annulation de la tâche...")
            self.worker_thread.cancel()

    def task_finished(self):
        """Gérer la fin de la tâche"""
        self.start_button.setEnabled(True)
        self.cancel_button.setEnabled(False)
        self.progress_bar.setVisible(False)
        self.worker_thread = None

        if not self.shutdown_in_progress:
            self.add_log_message("=== Tâche terminée ===")

    def update_progress(self, value):
        self.progress_bar.setValue(value)

    def update_status(self, message):
        self.status_label.setText(message)

    def add_log_message(self, message):
        timestamp = time.strftime("%H:%M:%S")
        log_entry = f"[{timestamp}] {message}"
        self.log_display.append(log_entry)

        # Forcer une mise à jour immédiate de l'affichage
        QApplication.processEvents()

    def closeEvent(self, event):
        """
        Gérer la fermeture de l'application avec une approche de terminaison progressive des threads
        """
        # Si aucun thread ne s'exécute, fermer immédiatement
        if not self.worker_thread or not self.worker_thread.isRunning():
            self.add_log_message("Aucune tâche d'arrière-plan en cours - fermeture immédiate")
            event.accept()
            return

        self.shutdown_in_progress = True
        self.add_log_message("=== FERMETURE DE L'APPLICATION DEMANDÉE ===")
        self.add_log_message("Thread d'arrière-plan détecté - tentative de fermeture gracieuse...")

        # ÉTAPE 1 : Essayer l'annulation coopérative
        self.add_log_message("Étape 1 : Demande d'annulation coopérative...")
        self.worker_thread.cancel()

        # Attendre la fermeture coopérative (donner un temps raisonnable)
        self.add_log_message("Attente jusqu'à 3 secondes pour une fermeture coopérative...")
        if self.worker_thread.wait(3000):  # 3 secondes
            self.add_log_message("✓ Thread arrêté de manière coopérative - fermeture de l'application")
            event.accept()
            return

        self.add_log_message("✗ Annulation coopérative échouée")

        # ÉTAPE 2 : Essayer le signal quit()
        self.add_log_message("Étape 2 : Envoi du signal de sortie au thread...")
        self.worker_thread.quit()

        # Attendre que le signal de sortie fonctionne
        self.add_log_message("Attente jusqu'à 2 secondes pour la réponse au signal de sortie...")
        if self.worker_thread.wait(2000):  # 2 secondes
            self.add_log_message("✓ Thread arrêté après le signal de sortie - fermeture de l'application")
            event.accept()
            return

        self.add_log_message("✗ Signal de sortie échoué")

        # ÉTAPE 3 : Demander à l'utilisateur s'il veut terminer de force
        self.add_log_message(
            "Étape 3 : Le thread ne répond pas - demande de permission à l'utilisateur pour terminer de force")

        reply = QMessageBox.question(
            self,
            "Terminer le thread de force ?",
            "La tâche d'arrière-plan ne répond pas aux demandes de fermeture.\n\n"
            "Terminer le thread de force ?\n"
            "⚠️ Attention : Cela peut entraîner une perte ou une corruption des données.\n\n"
            "Choisir :\n"
            "• Oui : Terminer de force et fermer\n"
            "• Non : Annuler la fermeture et attendre",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
            QMessageBox.StandardButton.No
        )

        if reply == QMessageBox.StandardButton.Yes:
            # ÉTAPE 4 : Terminaison forcée
            self.add_log_message("⚠️ TERMINAISON FORCÉE DU THREAD ⚠️")
            self.worker_thread.terminate()

            # Attendre que la terminaison se termine
            if self.worker_thread.wait(1000):  # 1 seconde
                self.add_log_message("✓ Thread terminé de force - fermeture de l'application")
            else:
                self.add_log_message("⚠️ La terminaison du thread peut ne pas s'être terminée proprement")

            event.accept()
        else:
            # L'utilisateur a choisi d'annuler la fermeture
            self.add_log_message("L'utilisateur a annulé la fermeture - l'application restera ouverte")
            self.add_log_message(
                "Le thread est toujours en cours d'exécution - vous devrez peut-être attendre ou essayer de fermer à nouveau")
            self.shutdown_in_progress = False
            event.ignore()  # Ne pas fermer l'application


class StubbornWorker(QThread):
    progress_update = Signal(int)
    status_update = Signal(str)
    log_message = Signal(str)

    def __init__(self):
        super().__init__()
        self.is_cancelled = False

    def cancel(self):
        self.is_cancelled = True
        self.log_message.emit("Annulation demandée (mais je vais l'ignorer !)")

    def run(self):
        self.log_message.emit("Worker têtu démarré - j'ignore l'annulation !")

        for i in range(30):  # Tâche plus longue
            # Volontairement NE PAS vérifier self.is_cancelled !
            time.sleep(1)
            progress = int(((i + 1) / 30) * 100)
            self.progress_update.emit(progress)
            self.status_update.emit(f"Travail têtu... {i + 1}/30")

            if i % 5 == 0:
                self.log_message.emit(f"Toujours en train d'ignorer l'annulation à l'étape {i + 1}")

        self.log_message.emit("Worker têtu terminé (n'a jamais été annulé)")


if __name__ == "__main__":
    app = QApplication(sys.argv)

    # Créer la fenêtre principale
    window = GracefulShutdownApp()

    window.show()

    print("Instructions :")
    print("1. Démarrer une longue tâche")
    print("2. Essayer de fermer la fenêtre")
    print("3. Observer le processus de fermeture gracieuse")

    sys.exit(app.exec())
```