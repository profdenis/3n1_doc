import sys
from PySide6.QtWidgets import QApplication, QWidget, QLabel, QGridLayout


class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Exemple de QGridLayout 3x5")

        # Création d'une instance QGridLayout
        layout = QGridLayout()

        # Ajout des widgets QLabel dans la grille 3x5
        for row in range(3):  # Boucle pour les lignes (0 à 2)
            for col in range(5):  # Boucle pour les colonnes (0 à 4)
                label = QLabel(f"Ligne {row}, Colonne {col}")
                layout.addWidget(label, row, col)  # Ajout à la grille

        # Application du layout à la fenêtre
        self.setLayout(layout)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())