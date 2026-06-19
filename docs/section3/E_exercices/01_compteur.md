# **Exercice 1 : Construction d'une application compteur**

## **Partie 1 : Créer le layout de base**

- Créez une nouvelle application PySide6 avec une fenêtre principale.
- Ajoutez un label pour afficher un nombre (commencez à 0).
- Ajoutez un bouton étiqueté « + » (plus) en dessous du label.
- Disposez le label et le bouton verticalement en utilisant un gestionnaire de layout.
- À ce stade, n'ajoutez pas d'interactivité ; construisez simplement l'interface statique.

---

## **Partie 2 : Ajouter une interactivité de base**

- Rendez le bouton « + » fonctionnel : lorsqu'il est cliqué, il doit augmenter le nombre affiché de 1.
- Assurez-vous que le label se met à jour immédiatement pour montrer la nouvelle valeur.
- Utilisez des mécanismes appropriés signaux/slots pour connecter le bouton à la logique qui met à jour le compteur.

---

## **Partie 3 : Ajouter plus de contrôles**

- Ajoutez un bouton « - » (moins) pour permettre de décrémenter le compteur.
- Ajoutez une boîte de spin (entrée numérique) qui permet à l'utilisateur de choisir la quantité par laquelle le
  compteur augmente ou diminue.
- Mettez à jour la logique afin que les boutons « + » et « - » utilisent la valeur de la boîte de spin comme taille de
  pas pour incrémenter ou décrémenter.
- Placez les nouveaux contrôles proprement dans le layout.

---

## **Partie 4 : Créer une fenêtre de paramètres**

- Ajoutez une fenêtre de paramètres séparée que l'utilisateur peut ouvrir depuis la fenêtre principale (par exemple,
  avec un bouton « Paramètres »).
- Dans la fenêtre de paramètres, incluez un contrôle (comme une boîte de spin) qui permet à l'utilisateur de définir la
  taille de pas globale pour le compteur.
- Lorsque la taille de pas est modifiée dans la fenêtre de paramètres, elle doit automatiquement mettre à jour la taille
  de pas dans la boîte de spin de la fenêtre principale.
- Utilisez des signaux personnalisés si nécessaire pour communiquer les changements de la fenêtre de paramètres vers la
  fenêtre principale.

---

## **Partie 5 : Ajouter une fonctionnalité de réinitialisation via la fenêtre de paramètres**

- Dans la fenêtre de paramètres, ajoutez un bouton « Réinitialiser ».
- Lorsque l'utilisateur clique sur « Réinitialiser », le compteur dans la fenêtre principale doit être réinitialisé à
  zéro.
- Assurez-vous que la communication entre la fenêtre de paramètres et la fenêtre principale est gérée à l'aide de
  signaux/slots.

---

## **Partie 6 : Widgets réutilisables & Connexions multiples de signaux**

**Tâche :** Créer 3 compteurs indépendants qui répondent tous aux paramètres globaux
**Objectifs :**

1. Créer une classe `CounterWidget` réutilisable avec une fonctionnalité autonome
2. Montrer plusieurs widgets connectés aux mêmes signaux
3. Contrôle centralisé via des paramètres partagés

---

**Défi bonus :**

- Ajoutez des fonctionnalités supplémentaires que vous pouvez imaginer, comme changer le schéma de couleurs depuis la
  fenêtre de paramètres, ou afficher un message lorsque le compteur atteint une certaine valeur.

---

**Instructions :**

- Pour chaque partie, commencez à partir de votre solution précédente et ajoutez les nouvelles fonctionnalités décrites.
  Testez votre application après chaque étape pour vous assurer que tout fonctionne comme prévu. Concentrez-vous sur
  l'organisation de votre code et l'utilisation efficace des signaux/slots de PySide6.
- Gardez vos différentes versions dans différents fichiers, par exemple dans les fichiers nommés `compteur1.py`,
  `compteur2.py`, `compteur3.py`, ...

---

??? info "Exemple de solution pour la Partie 1"
    
    ```python
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
    ```

??? info "Exemple de solution pour la Partie 2"

    ```python
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
    ```

??? info "Exemple de solution pour la Partie 3"

    ```python
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
    ```

??? info "Exemple de solution pour la Partie 4"

    ```python
    import sys
    from PySide6.QtWidgets import (QApplication, QMainWindow, QWidget,
                                   QVBoxLayout, QLabel, QPushButton, QSpinBox,
                                   QDialog, QHBoxLayout)
    from PySide6.QtCore import Signal
    
    
    class SettingsDialog(QDialog):
        """Fenêtre de paramètres pour le compteur."""
        step_size_changed = Signal(int)  # Signal personnalisé
    
        def __init__(self, parent=None):
            super().__init__(parent)
            self.setWindowTitle("Paramètres")
            self.setGeometry(200, 200, 300, 150)
    
            layout = QVBoxLayout()
    
            # Boîte de spin pour la taille de pas globale
            self.global_step_spinbox = QSpinBox()
            self.global_step_spinbox.setRange(1, 10)
            self.global_step_spinbox.valueChanged.connect(self.emit_step_change)
    
            layout.addWidget(QLabel("Taille de pas globale:"))
            layout.addWidget(self.global_step_spinbox)
    
            # Bouton OK
            ok_button = QPushButton("OK")
            ok_button.clicked.connect(self.accept)
            layout.addWidget(ok_button)
    
            self.setLayout(layout)
    
        def emit_step_change(self, value):
            """Émet le signal lorsque la taille de pas change."""
            self.step_size_changed.emit(value)
    
    
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
    
            # Bouton paramètres
            self.settings_button = QPushButton("Paramètres")
            self.settings_button.clicked.connect(self.show_settings)
            layout.addWidget(self.settings_button)
    
            central_widget.setLayout(layout)
            self.setCentralWidget(central_widget)
    
        def show_settings(self):
            """Affiche la fenêtre de paramètres."""
            self.settings_dialog = SettingsDialog()
            self.settings_dialog.global_step_spinbox.setValue(self.step_size)
            self.settings_dialog.step_size_changed.connect(self.update_global_step)
            self.settings_dialog.exec()
    
        def update_global_step(self, value):
            """Met à jour la taille de pas globale."""
            self.step_size = value
            self.step_spinbox.setValue(value)
    
        def update_step_size(self, value):
            """Met à jour la taille de pas locale."""
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
    ```

??? info "Exemple de solution pour la Partie 5"

    ```python
    import sys
    from PySide6.QtWidgets import (QApplication, QMainWindow, QWidget,
                                   QVBoxLayout, QLabel, QPushButton, QSpinBox,
                                   QDialog, QHBoxLayout)
    from PySide6.QtCore import Signal
    
    
    class SettingsDialog(QDialog):
        """Fenêtre de paramètres pour le compteur."""
        step_size_changed = Signal(int)  # Signal personnalisé
        reset_requested = Signal()  # Signal pour réinitialiser
    
        def __init__(self, parent=None):
            super().__init__(parent)
            self.setWindowTitle("Paramètres")
            self.setGeometry(200, 200, 300, 180)
    
            layout = QVBoxLayout()
    
            # Boîte de spin pour la taille de pas globale
            self.global_step_spinbox = QSpinBox()
            self.global_step_spinbox.setRange(1, 10)
            self.global_step_spinbox.valueChanged.connect(self.emit_step_change)
    
            layout.addWidget(QLabel("Taille de pas globale:"))
            layout.addWidget(self.global_step_spinbox)
    
            # Bouton Réinitialiser
            reset_button = QPushButton("Réinitialiser")
            reset_button.clicked.connect(self.emit_reset)
            layout.addWidget(reset_button)
    
            # Bouton OK
            ok_button = QPushButton("OK")
            ok_button.clicked.connect(self.accept)
            layout.addWidget(ok_button)
    
            self.setLayout(layout)
    
        def emit_step_change(self, value):
            """Émet le signal lorsque la taille de pas change."""
            self.step_size_changed.emit(value)
    
        def emit_reset(self):
            """Émet le signal pour réinitialiser le compteur."""
            self.reset_requested.emit()
    
    
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
    
            # Bouton paramètres
            self.settings_button = QPushButton("Paramètres")
            self.settings_button.clicked.connect(self.show_settings)
            layout.addWidget(self.settings_button)
    
            central_widget.setLayout(layout)
            self.setCentralWidget(central_widget)
    
        def show_settings(self):
            """Affiche la fenêtre de paramètres."""
            self.settings_dialog = SettingsDialog()
            self.settings_dialog.global_step_spinbox.setValue(self.step_size)
            self.settings_dialog.step_size_changed.connect(self.update_global_step)
            self.settings_dialog.reset_requested.connect(self.reset_counter)
            self.settings_dialog.exec()
    
        def update_global_step(self, value):
            """Met à jour la taille de pas globale."""
            self.step_size = value
            self.step_spinbox.setValue(value)
    
        def update_step_size(self, value):
            """Met à jour la taille de pas locale."""
            self.step_size = value
    
        def increment_counter(self):
            """Incrémente le compteur et met à jour l'affichage."""
            self.counter += self.step_size
            self.counter_label.setText(str(self.counter))
    
        def decrement_counter(self):
            """Décrémente le compteur et met à jour l'affichage."""
            self.counter -= self.step_size
            self.counter_label.setText(str(self.counter))
    
        def reset_counter(self):
            """Réinitialise le compteur à zéro."""
            self.counter = 0
            self.counter_label.setText(str(self.counter))
    
    
    if __name__ == "__main__":
        app = QApplication(sys.argv)
        window = MainWindow()
        window.show()
        sys.exit(app.exec())
    ```

??? info "Exemple de solution pour la Partie 6"

    ```python
    import sys
    from PySide6.QtWidgets import (QApplication, QMainWindow, QWidget,
                                   QVBoxLayout, QLabel, QPushButton, QSpinBox,
                                   QDialog, QHBoxLayout)
    from PySide6.QtCore import Signal
    
    
    class SettingsDialog(QDialog):
        """Fenêtre de paramètres pour le compteur."""
        step_size_changed = Signal(int)  # Signal personnalisé
        reset_requested = Signal()  # Signal pour réinitialiser
    
        def __init__(self, parent=None):
            super().__init__(parent)
            self.setWindowTitle("Paramètres")
            self.setGeometry(200, 200, 300, 180)
    
            layout = QVBoxLayout()
    
            # Boîte de spin pour la taille de pas globale
            self.global_step_spinbox = QSpinBox()
            self.global_step_spinbox.setRange(1, 10)
            self.global_step_spinbox.valueChanged.connect(self.emit_step_change)
    
            layout.addWidget(QLabel("Taille de pas globale:"))
            layout.addWidget(self.global_step_spinbox)
    
            # Bouton Réinitialiser
            reset_button = QPushButton("Réinitialiser")
            reset_button.clicked.connect(self.emit_reset)
            layout.addWidget(reset_button)
    
            # Bouton OK
            ok_button = QPushButton("OK")
            ok_button.clicked.connect(self.accept)
            layout.addWidget(ok_button)
    
            self.setLayout(layout)
    
        def emit_step_change(self, value):
            """Émet le signal lorsque la taille de pas change."""
            self.step_size_changed.emit(value)
    
        def emit_reset(self):
            """Émet le signal pour réinitialiser le compteur."""
            self.reset_requested.emit()
    
    
    class CounterWidget(QWidget):
        """Widget compteur réutilisable."""
        counter_changed = Signal(int)  # Signal émis lorsque le compteur change
    
        def __init__(self, parent=None):
            super().__init__(parent)
            self.counter = 0
            self.step_size = 1
    
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
    
            self.setLayout(layout)
    
        def update_step_size(self, value):
            """Met à jour la taille de pas locale."""
            self.step_size = value
    
        def increment_counter(self):
            """Incrémente le compteur et met à jour l'affichage."""
            self.counter += self.step_size
            self.counter_label.setText(str(self.counter))
            self.counter_changed.emit(self.counter)
    
        def decrement_counter(self):
            """Décrémente le compteur et met à jour l'affichage."""
            self.counter -= self.step_size
            self.counter_label.setText(str(self.counter))
            self.counter_changed.emit(self.counter)
    
        def reset_counter(self):
            """Réinitialise le compteur à zéro."""
            self.counter = 0
            self.counter_label.setText(str(self.counter))
            self.counter_changed.emit(self.counter)
    
    
    class MainWindow(QMainWindow):
        def __init__(self):
            super().__init__()
            self.setWindowTitle("Compteurs multiples")
            self.setGeometry(100, 100, 500, 400)
            self.step_size = 1
    
            # Création du widget central
            central_widget = QWidget()
            layout = QVBoxLayout()
    
            # Bouton paramètres
            settings_button = QPushButton("Paramètres")
            settings_button.clicked.connect(self.show_settings)
            layout.addWidget(settings_button)
    
            # Création de 3 compteurs indépendants
            self.counters = []
            for i in range(3):
                counter = CounterWidget()
                counter.step_spinbox.setValue(self.step_size)
                counter.counter_changed.connect(lambda value, idx=i: print(f"Compteur {idx + 1}: {value}"))
                layout.addWidget(counter)
                self.counters.append(counter)
    
            central_widget.setLayout(layout)
            self.setCentralWidget(central_widget)
    
        def show_settings(self):
            """Affiche la fenêtre de paramètres."""
            self.settings_dialog = SettingsDialog()
            self.settings_dialog.global_step_spinbox.setValue(self.step_size)
            self.settings_dialog.step_size_changed.connect(self.update_global_step)
            self.settings_dialog.reset_requested.connect(self.reset_all_counters)
            self.settings_dialog.exec()
    
        def update_global_step(self, value):
            """Met à jour la taille de pas globale pour tous les compteurs."""
            self.step_size = value
            for counter in self.counters:
                counter.step_spinbox.setValue(value)
    
        def reset_all_counters(self):
            """Réinitialise tous les compteurs."""
            for counter in self.counters:
                counter.reset_counter()
    
    
    if __name__ == "__main__":
        app = QApplication(sys.argv)
        window = MainWindow()
        window.show()
        sys.exit(app.exec())
    ```

---

Ces exemples montrent comment construire progressivement une application compteur avec PySide6, en utilisant les
signaux/slots pour la communication entre widgets et en créant des composants réutilisables.