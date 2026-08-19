# **Exemples de QGridLayout**

## **Exemple 1 : Grille 3x5 avec des étiquettes**

Voici comment créer une grille de **3 lignes et 5 colonnes** avec `QGridLayout` et des widgets `QLabel` en PySide6.
Chaque étiquette indique sa position (ligne, colonne) :

```python title="grid1.py"
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


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
```

### **Fonctionnement**

- La boucle externe (`range(3)`) parcourt les 3 lignes.
- La boucle interne (`range(5)`) parcourt les 5 colonnes.
- Chaque cellule de la grille contient un `QLabel` affichant sa position.

**Résultat** : Une fenêtre avec une grille 3x5 d'étiquettes.

---

## **Exemple 2 : Grille avec des widgets étendus**

Un widget dans un `QGridLayout` peut occuper plusieurs lignes et/ou colonnes en utilisant les arguments supplémentaires
de la méthode `addWidget()` pour spécifier l'étendue (`rowSpan`, `columnSpan`).

### **Exemple pratique**

- Un `QTextEdit` occupe 2 lignes et 2 colonnes (en haut à gauche).
- Un `QListWidget` occupe 1 ligne et 2 colonnes (en haut à droite).
- Un `QPushButton` occupe 2 lignes et 1 colonne (en bas à gauche).
- Un `QLabel` occupe une seule cellule (en bas à droite).

```python title="grid2.py"
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


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
```

### **Explications**

1. **`addWidget(row, column, rowSpan, columnSpan)`** :
    - Permet à un widget d'occuper plusieurs cellules.
    - Exemple : `layout.addWidget(widget, 0, 0, 2, 2)` → Le widget commence en (0,0) et couvre 2 lignes/colonnes.

2. **`ColorWidget`** :
    - Classe auxiliaire pour colorer les cellules vides et visualiser l'étendue des widgets.
    - Utilise `QPalette` pour définir la couleur de fond.

3. **Utilité** :
    - Idéal pour des interfaces complexes où certains widgets nécessitent plus d'espace.

---

## **Tableau récapitulatif**

| Méthode                                         | Description                                               |
|-------------------------------------------------|-----------------------------------------------------------|
| `addWidget(widget, row, col)`                   | Place un widget dans une cellule spécifique.              |
| `addWidget(widget, row, col, rowSpan, colSpan)` | Étend le widget sur plusieurs cellules (lignes/colonnes). |

Ces exemples montrent comment créer des grilles flexibles avec PySide6. Pour des cas plus avancés, combinez
`QGridLayout` avec d'autres layouts (`QVBoxLayout`, etc.).