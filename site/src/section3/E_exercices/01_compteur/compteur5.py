import sys
from PySide6.QtWidgets import (QApplication, QMainWindow, QWidget,
                               QVBoxLayout, QLabel, QPushButton, QSpinBox,
                               QDialog, QHBoxLayout)
from PySide6.QtCore import Signal

class SettingsDialog(QDialog):
    """Fenêtre de paramètres pour le compteur."""
    step_size_changed = Signal(int)  # Signal personnalisé
    reset_requested = Signal()       # Signal pour réinitialiser

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
