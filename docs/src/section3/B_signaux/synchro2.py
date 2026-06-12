import sys
from PySide6.QtWidgets import QApplication, QWidget, QSlider, QDial, QLabel, QVBoxLayout
from PySide6.QtCore import Qt

class DialWithLabel(QWidget):
    """
    Widget composite qui regroupe un QDial et un QLabel.
    Le label affiche toujours la valeur actuelle du cadran.
    Ce widget fournit une méthode setValue pour mettre à jour le cadran et le label ensemble.
    """

    def __init__(self, min_val, max_val):
        """
        Initialise le cadran et le label, et configure le layout.

        Args:
            min_val (int): Valeur minimale pour le cadran.
            max_val (int): Valeur maximale pour le cadran.
        """
        super().__init__()
        self.dial = QDial()
        self.label = QLabel()

        # Configuration du cadran
        self.dial.setNotchesVisible(True)
        self.dial.setRange(min_val, max_val)

        # Configuration du label
        self.label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # Disposition verticale des widgets
        layout = QVBoxLayout()
        layout.addWidget(self.dial)
        layout.addWidget(self.label)
        self.setLayout(layout)

    def setValue(self, value):
        """
        Définit la valeur du cadran et met à jour le label pour correspondre.

        Args:
            value (int): La valeur à définir sur le cadran et à afficher sur le label.
        """
        self.dial.setValue(value)
        self.label.setText(f"Valeur : {value}")

class LinkedControlsApp(QWidget):
    """
    Fenêtre principale de l'application.
    Contient un QSlider et un DialWithLabel.
    Garde les deux contrôles synchronisés, donc changer l'un met à jour l'autre.
    """

    def __init__(self):
        """
        Initialise la fenêtre de l'application et les contrôles.
        """
        super().__init__()
        self.current_value = 1  # Stocke la valeur actuelle partagée par le curseur et le cadran
        self.init_ui()

    def init_ui(self):
        """
        Configure l'interface utilisateur, connecte les signaux et initialise les valeurs des contrôles.
        """
        layout = QVBoxLayout()

        # Création du curseur et du widget composite cadran-avec-label
        self.slider = QSlider(Qt.Orientation.Horizontal)
        self.dial_widget = DialWithLabel(1, 10)

        # Définition de la plage du curseur pour correspondre au cadran
        self.slider.setRange(1, 10)

        # Ajout des widgets au layout
        layout.addWidget(self.slider)
        layout.addWidget(self.dial_widget)
        self.setLayout(layout)

        # Connexion des signaux valueChanged à la méthode de synchronisation
        self.slider.valueChanged.connect(self.set_current_value)
        self.dial_widget.dial.valueChanged.connect(self.set_current_value)

        # Définition des valeurs initiales pour les deux contrôles
        self.slider.setValue(self.current_value)
        self.dial_widget.setValue(self.current_value)

    def set_current_value(self, value):
        """
        Synchronise le curseur et le cadran pour qu'ils affichent toujours la même valeur.
        Met également à jour le label dans le widget du cadran.

        Args:
            value (int): La nouvelle valeur à définir sur les deux contrôles.
        """
        self.current_value = value

        # Détermine quel widget doit être mis à jour
        if self.sender() == self.slider:
            # Si le curseur a changé, met à jour le widget du cadran
            widget = self.dial_widget
        else:
            # Si le cadran a changé, met à jour le curseur et le label du widget du cadran
            widget = self.slider
            self.dial_widget.setValue(value)

        # Empêche les boucles de rétroaction des signaux lors de la mise à jour de l'autre widget
        widget.blockSignals(True)
        widget.setValue(value)
        widget.blockSignals(False)

if __name__ == "__main__":
    # Configuration standard d'une application PySide6
    app = QApplication(sys.argv)
    window = LinkedControlsApp()
    window.setWindowTitle("Contrôles synchronisés avec état")
    window.show()
    sys.exit(app.exec())
