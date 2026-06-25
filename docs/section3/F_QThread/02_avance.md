# Exemple Avancé

??? note "Code complet"

    ```python
    import sys
    import time
    from PySide6.QtCore import QThread, Signal, QTimer
    from PySide6.QtWidgets import (QApplication, QWidget, QVBoxLayout, QPushButton,
                                 QLabel, QProgressBar, QTextEdit)

    class AdvancedWorkerThread(QThread):
        """Thread worker amélioré avec rapport de progression et support d'annulation"""

        # Signaux pour la communication avec le thread principal
        progress_update = Signal(int)        # Pourcentage de progression (0-100)
        status_update = Signal(str)          # Message de statut
        task_finished = Signal(str)          # Message de complétion
        log_message = Signal(str)            # Entrée de journal

        def __init__(self, task_duration=10):
            super().__init__()
            self.task_duration = task_duration
            self.is_cancelled = False

        def cancel(self):
            """Demander l'annulation de la tâche"""
            self.is_cancelled = True

        def run(self):
            """Méthode principale de travail - s'exécute dans un thread séparé"""
            self.log_message.emit("Tâche démarrée...")
            self.status_update.emit("Initialisation...")

            total_steps = self.task_duration

            for step in range(total_steps):
                # Vérifier si l'annulation a été demandée
                if self.is_cancelled:
                    self.status_update.emit("Tâche annulée")
                    self.task_finished.emit("La tâche a été annulée par l'utilisateur")
                    self.log_message.emit(f"Tâche annulée à l'étape {step + 1}")
                    return

                # Simuler du travail
                time.sleep(1)

                # Calculer et rapport de progression
                progress = int(((step + 1) / total_steps) * 100)
                self.progress_update.emit(progress)
                self.status_update.emit(f"Traitement de l'étape {step + 1} sur {total_steps}")
                self.log_message.emit(f"Étape {step + 1} terminée")

            # Tâche terminée avec succès
            self.status_update.emit("Tâche terminée !")
            self.task_finished.emit("Tout le travail terminé avec succès !")
            self.log_message.emit("Tâche terminée avec succès")

    class AdvancedBackgroundExample(QWidget):
        def __init__(self):
            super().__init__()
            self.worker_thread = None
            self.init_ui()
            self.setup_timer()

        def init_ui(self):
            layout = QVBoxLayout()

            # Affichage du statut
            self.status_label = QLabel("Prêt à démarrer la tâche")
            layout.addWidget(self.status_label)

            # Barre de progression
            self.progress_bar = QProgressBar()
            self.progress_bar.setRange(0, 100)
            self.progress_bar.setValue(0)
            layout.addWidget(self.progress_bar)

            # Boutons de contrôle
            self.start_button = QPushButton("Démarrer tâche en arrière-plan")
            self.cancel_button = QPushButton("Annuler tâche")
            self.cancel_button.setEnabled(False)

            self.start_button.clicked.connect(self.start_task)
            self.cancel_button.clicked.connect(self.cancel_task)

            layout.addWidget(self.start_button)
            layout.addWidget(self.cancel_button)

            # Compteur interactif pour montrer que l'UI reste réactive
            self.counter_button = QPushButton("Test UI Compteur (0)")
            self.counter_button.clicked.connect(self.increment_counter)
            layout.addWidget(self.counter_button)

            # Affichage du journal
            log_label = QLabel("Journal des tâches :")
            layout.addWidget(log_label)

            self.log_display = QTextEdit()
            self.log_display.setMaximumHeight(150)
            self.log_display.setReadOnly(True)
            layout.addWidget(self.log_display)

            self.setLayout(layout)
            self.setWindowTitle("Exemple de tâche en arrière-plan avancée")
            self.resize(400, 350)

            # Initialiser le compteur
            self.counter = 0

        def setup_timer(self):
            """Configurer un minuteur pour afficher le temps écoulé pendant l'exécution de la tâche"""
            self.timer = QTimer()
            self.timer.timeout.connect(self.update_elapsed_time)
            self.start_time = None

        def start_task(self):
            """Démarrer la tâche en arrière-plan"""
            # Réinitialiser l'état de l'UI
            self.progress_bar.setValue(0)
            self.log_display.clear()

            # Mettre à jour les états des boutons
            self.start_button.setEnabled(False)
            self.cancel_button.setEnabled(True)

            # Créer et configurer le thread worker
            self.worker_thread = AdvancedWorkerThread(task_duration=8)

            # Connecter tous les signaux
            self.worker_thread.progress_update.connect(self.update_progress)
            self.worker_thread.status_update.connect(self.update_status)
            self.worker_thread.task_finished.connect(self.task_completed)
            self.worker_thread.log_message.connect(self.add_log_message)

            # Démarrer le thread et le minuteur
            self.start_time = time.time()
            self.timer.start(1000)  # Mise à jour toutes les secondes
            self.worker_thread.start()

            self.add_log_message("Tâche en arrière-plan démarrée")

        def cancel_task(self):
            """Annuler la tâche en cours"""
            if self.worker_thread and self.worker_thread.isRunning():
                self.worker_thread.cancel()
                self.add_log_message("Annulation demandée...")

        def update_progress(self, value):
            """Mettre à jour la barre de progression"""
            self.progress_bar.setValue(value)

        def update_status(self, message):
            """Mettre à jour l'étiquette de statut"""
            elapsed = ""
            if self.start_time:
                elapsed_seconds = int(time.time() - self.start_time)
                elapsed = f" (Temps écoulé : {elapsed_seconds}s)"

            self.status_label.setText(message + elapsed)

        def task_completed(self, message):
            """Gérer la fin de la tâche"""
            self.status_label.setText(message)

            # Réinitialiser les états des boutons
            self.start_button.setEnabled(True)
            self.cancel_button.setEnabled(False)

            # Arrêter le minuteur
            self.timer.stop()

            # Nettoyer le thread
            self.worker_thread = None

            self.add_log_message("Tâche terminée ou annulée")

        def add_log_message(self, message):
            """Ajouter un message à l'affichage du journal"""
            timestamp = time.strftime("%H:%M:%S")
            log_entry = f"[{timestamp}] {message}"
            self.log_display.append(log_entry)

        def update_elapsed_time(self):
            """Mettre à jour l'affichage du temps écoulé"""
            if self.start_time:
                elapsed_seconds = int(time.time() - self.start_time)
                current_text = self.status_label.text()
                # Supprimer le temps écoulé ancien s'il est présent
                if "(Temps écoulé:" in current_text:
                    current_text = current_text.split(" (Temps écoulé:")[0]
                self.status_label.setText(f"{current_text} (Temps écoulé : {elapsed_seconds}s)")

        def increment_counter(self):
            """Démontrer que l'UI reste réactive pendant la tâche en arrière-plan"""
            self.counter += 1
            self.counter_button.setText(f"Test UI Compteur ({self.counter})")

    if __name__ == "__main__":
        app = QApplication(sys.argv)
        window = AdvancedBackgroundExample()
        window.show()
        sys.exit(app.exec())
    ```

## Nouveaux concepts dans l'exemple avancé

### 1. **Annulation de tâche**

Dans l'exemple basique, une fois que vous aviez démarré une tâche, vous deviez attendre qu'elle se termine. L'exemple
avancé introduit l'**annulation** :

```python
def cancel(self):
    """Demander l'annulation de la tâche"""
    self.is_cancelled = True


def run(self):
    for step in range(total_steps):
        # Vérifier si l'annulation a été demandée
        if self.is_cancelled:
            self.status_update.emit("Tâche annulée")
            self.task_finished.emit("La tâche a été annulée par l'utilisateur")
            return  # Quitter la tâche tôt
```

**Points clés :**

- Nous utilisons un simple drapeau booléen (`self.is_cancelled`) pour signaler l'annulation
- Le thread worker vérifie régulièrement ce drapeau pendant son travail
- Quand annulé, le thread quitte tôt et notifie le thread principal
- Le thread principal peut demander l'annulation en appelant `worker_thread.cancel()`

### 2. **Rapport de progression**

L'exemple basique montrait seulement "en cours" ou "terminé". L'exemple avancé montre une **progression réelle** :

```python
# Dans le thread worker
progress_update = Signal(int)  # Nouveau signal pour le pourcentage de progression

# Calculer la progression en pourcentage
progress = int(((step + 1) / total_steps) * 100)
self.progress_update.emit(progress)
```

**Dans la fenêtre principale :**

```python
self.progress_bar = QProgressBar()
self.progress_bar.setRange(0, 100)  # 0% à 100%

# Connecter le signal de progression à la barre de progression
self.worker_thread.progress_update.connect(self.update_progress)
```

**Pourquoi cela compte :** Les utilisateurs peuvent voir combien de travail reste et prendre des décisions éclairées sur
l'attente ou l'annulation.

### 3. **Différents types de signaux**

Au lieu d'un seul signal, nous avons maintenant **quatre signaux différents** pour différentes fins :

```python
progress_update = Signal(int)  # Nombres (0-100)
status_update = Signal(str)  # Statut actuel
task_finished = Signal(str)  # Résultat final
log_message = Signal(str)  # Journal détaillé
```

**Cela démontre :** Vous pouvez avoir autant de signaux que nécessaire, chacun transportant différents types
d'informations.

### 4. **Gestion de l'état de l'UI**

L'exemple avancé montre une gestion correcte des **états des boutons** :

```python
def start_task(self):
    self.start_button.setEnabled(False)  # Désactiver le démarrage
    self.cancel_button.setEnabled(True)  # Activer l'annulation


def task_completed(self, message):
    self.start_button.setEnabled(True)  # Réactiver le démarrage
    self.cancel_button.setEnabled(False)  # Désactiver l'annulation
```

**Pourquoi cela compte :** Empêche les utilisateurs de démarrer plusieurs tâches simultanément ou d'essayer d'annuler
quand rien ne s'exécute.

### 5. **Journalisation en temps réel**

L'exemple avancé introduit un **affichage du journal** qui montre ce qui se passe :

```python
def add_log_message(self, message):
    timestamp = time.strftime("%H:%M:%S")
    log_entry = f"[{timestamp}] {message}"
    self.log_display.append(log_entry)
```

**Cela enseigne :** Comment fournir des retours détaillés aux utilisateurs et comment horodater les événements.

### 6. **Suivi du temps écoulé**

Nouveau concept : **QTimer** pour des mises à jour régulières :

```python
def setup_timer(self):
    self.timer = QTimer()
    self.timer.timeout.connect(self.update_elapsed_time)


# Démarrer le minuteur quand la tâche commence
self.timer.start(1000)  # Mise à jour toutes les 1000ms (1 seconde)
```

**Insight clé :** Vous pouvez exécuter plusieurs choses simultanément - la tâche en arrière-plan ET un minuteur pour les
mises à jour de l'UI.

### 7. **Expérience utilisateur améliorée**

L'exemple avancé montre plusieurs améliorations UX :

- **Retour visuel :** La barre de progression montre le pourcentage d'achèvement
- **Statut détaillé :** Les utilisateurs savent exactement quelle étape est en cours
- **Conscience du temps :** Le temps écoulé aide les utilisateurs à décider s'ils doivent attendre
- **Option d'annulation :** Les utilisateurs ne sont pas bloqués en attendant des tâches longues
- **Journalisation complète :** Les utilisateurs peuvent voir l'historique complet de ce qui s'est passé

## La vue d'ensemble

La progression de basique à avancé montre comment les applications réelles sont construites :

1. **Threading basique :** Résoudre le problème fondamental (ne pas bloquer l'UI)
2. **Threading amélioré :** Ajouter des fonctionnalités dont les utilisateurs ont vraiment besoin (progression,
   annulation, retours)
3. **Threading professionnel :** Gérer les cas limites et fournir une excellente expérience utilisateur

## Points à retenir

1. **Les threads peuvent être aussi simples ou complexes que nécessaire** - commencez simplement, ajoutez des
   fonctionnalités progressivement
2. **L'expérience utilisateur compte** - les barres de progression et l'annulation ne sont pas juste des "nice-to-have"
3. **Les signaux sont flexibles** - vous pouvez en créer autant que nécessaire pour différents types de données
4. **La gestion d'état est cruciale** - pensez toujours à quels boutons doivent être activés/désactivés
5. **Le timing est important** - QTimer vous permet de faire des mises à jour régulières sans bloquer

L'exemple avancé n'est pas juste "plus de code" : c'est "du code plus réfléchit" qui considère ce dont les utilisateurs
ont vraiment besoin lorsqu'ils utilisent une application avec des tâches en arrière-plan.