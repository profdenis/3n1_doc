# Gestion des tâches en arrière-plan

## Pourquoi les tâches en arrière-plan sont importantes

Dans les applications GUI, le thread principal (également appelé thread UI ou thread d'événements) est responsable de :

- Gérer les interactions utilisateur (clics, entrée clavier)
- Mettre à jour l'interface utilisateur
- Traiter les événements du système d'exploitation

Lorsque vous exécutez une tâche longue directement dans le thread principal, toute l'application devient non réactive.
Les utilisateurs ne peuvent pas cliquer sur des boutons, la fenêtre peut ne pas se redessiner correctement, et
l'application semble "gelée".

## Le problème : Bloquer le thread principal

Voici ce qui se passe lorsque vous exécutez une tâche longue dans le thread principal :

```python
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
```

**Essayez cet exemple :** Cliquez sur "Démarrer tâche longue" puis essayez de cliquer sur le bouton du compteur. Toute
l'application se fige !

## La solution : QThread

PySide6 fournit `QThread` pour exécuter des tâches dans des threads séparés. Voici la bonne façon de gérer les tâches en
arrière-plan :

```python
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
```

**Essayez cet exemple :** Cliquez sur "Démarrer tâche longue" puis cliquez immédiatement sur le bouton du compteur. Le
compteur fonctionne pendant que la tâche en arrière-plan s'exécute !

## Concepts clés expliqués

### 1. Communication entre threads avec les signaux

- Les threads ne peuvent pas mettre à jour directement les éléments GUI
- Utilisez `Signal` pour envoyer des données du thread worker au thread principal
- Le thread principal reçoit les signaux et met à jour le GUI

### 2. Connexion signal et slot

```python
# Dans la classe du thread worker
progress_update = Signal(str)  # Définir le signal

# Dans le thread principal
self.worker_thread.progress_update.connect(self.update_status)  # Connecter au slot
```

### 3. Cycle de vie du thread

- Créer une instance de thread
- Connecter les signaux avant de démarrer
- Appeler `start()` pour commencer l'exécution
- Nettoyer quand terminé

## Bonnes pratiques

1. **Utilisez toujours des signaux pour la communication entre threads**
2. **Désactivez les éléments UI pendant les tâches en arrière-plan** pour éviter les conflits
3. **Fournissez un retour utilisateur** sur la progression de la tâche
4. **Gérez correctement le nettoyage des threads**
5. **Ne créez pas trop de threads** - ils consomment des ressources système

## Erreurs courantes à éviter

- **Ne mettez jamais à jour le GUI directement depuis le thread worker**
- **N'oubliez pas** de réactiver les boutons après la fin de la tâche
- **Vérifiez toujours** si le thread est encore en cours d'exécution avant d'en créer un nouveau
- **Rappelez-vous** de connecter les signaux avant de démarrer le thread

## Prochaines étapes

Ce schéma de base peut être étendu pour :

- Traitement de fichiers avec barres de progression
- Téléchargements réseau avec indicateurs de progression
- Traitement de données avec support d'annulation
- Plusieurs tâches concurrentes

Le principe clé reste le même : gardez le thread principal libre pour les mises à jour de l'interface utilisateur, et
utilisez des threads séparés pour le travail lourd.