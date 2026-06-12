import sys
from PySide6.QtWidgets import QApplication, QLabel

# Création de l'application Qt
app = QApplication(sys.argv)

# Widget principal (une étiquette avec du texte)
label = QLabel("Hello, World!")
label.show()  # Affiche la fenêtre

# Exécution de la boucle principale
sys.exit(app.exec())