import sys
from PySide6.QtWidgets import (
    QApplication, QWidget, QGridLayout,
    QTextEdit, QListWidget, QPushButton, QLabel
)
from PySide6.QtGui import QPalette, QColor


class ColorWidget(QWidget):
    """Widget coloré pour visualiser les cellules vides."""

    def __init__(self, color):
        super().__init__()
        palette = self.palette()
        palette.setColor(self.backgroundRole(), QColor(color))
        self.setAutoFillBackground(True)
        self.setPalette(palette)
        self.setMinimumHeight(24)  # Hauteur minimale pour la visibilité


class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("QGridLayout avec étendue et couleurs")

        layout = QGridLayout()

        # QTextEdit occupant 2 lignes et 2 colonnes (haut-gauche)
        text_edit = QTextEdit("QTextEdit\n(2 lignes x 2 colonnes)")
        layout.addWidget(text_edit, 0, 0, 2, 2)  # (ligne, colonne, étendue_lignes, étendue_colonnes)

        # QListWidget occupant 1 ligne et 2 colonnes (haut-droite)
        list_widget = QListWidget()
        list_widget.addItems(["Élément 1", "Élément 2", "Élément 3"])
        layout.addWidget(list_widget, 0, 2, 1, 2)

        # Remplissage des cellules sous le QListWidget (ligne 1, colonnes 2 et 3)
        layout.addWidget(ColorWidget("lightblue"), 1, 2)
        layout.addWidget(ColorWidget("lightgreen"), 1, 3)

        # QPushButton occupant 2 lignes et 1 colonne (bas-gauche)
        button = QPushButton("Bouton étendu\n(2 lignes x 1 colonne)")
        layout.addWidget(button, 2, 0, 2, 1)

        # Remplissage de la cellule à droite du bouton (ligne 2, colonne 1)
        layout.addWidget(ColorWidget("yellow"), 2, 1)

        # QLabel dans une seule cellule (ligne 2, colonne 2)
        label = QLabel("Étiquette en cellule unique")
        layout.addWidget(label, 2, 2)

        # Remplissage des cellules restantes
        layout.addWidget(ColorWidget("orange"), 2, 3)
        layout.addWidget(ColorWidget("pink"), 3, 1)
        layout.addWidget(ColorWidget("violet"), 3, 2)
        layout.addWidget(ColorWidget("lightgray"), 3, 3)

        self.setLayout(layout)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())