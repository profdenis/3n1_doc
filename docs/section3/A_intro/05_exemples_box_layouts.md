# **Documentation : Exemples de Box Layouts**

## **1. Introduction**

Ce document présente deux exemples d'interfaces graphiques simples utilisant des layouts en PySide6 :

- Un layout vertical (`QVBoxLayout`) pour organiser les widgets de haut en bas.
- Un layout horizontal (`QHBoxLayout`) pour aligner les widgets côte à côte.

---

## **2. Exemple 1 : QVBoxLayout (Vertical)**

### **Code complet**

```python
import sys
from PySide6.QtWidgets import (
    QApplication, QWidget, QVBoxLayout,
    QLabel, QPushButton, QLineEdit, QCheckBox, QRadioButton
)


class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Exemple de QVBoxLayout")
        self.resize(300, 200)  # Taille initiale

        # Création du layout vertical
        layout = QVBoxLayout()

        # Ajout des widgets (empilés verticalement)
        layout.addWidget(QLabel("Ce texte est dans un QLabel"))
        layout.addWidget(QPushButton("Bouton cliquable"))
        layout.addWidget(QLineEdit("Champ de texte éditable"))
        layout.addWidget(QCheckBox("Case à cocher"))
        layout.addWidget(QRadioButton("Bouton radio"))

        # Application du layout à la fenêtre
        self.setLayout(layout)


app = QApplication(sys.argv)
window = MainWindow()
window.show()
sys.exit(app.exec())
```

### **Explications**

1. **Structure** :
    - `QVBoxLayout` dispose les widgets **verticalement**, les uns en dessous des autres.
    - Chaque widget est ajouté avec `layout.addWidget()`.

2. **Widgets utilisés** :
    - `QLabel` : Affiche du texte non modifiable.
    - `QPushButton` : Bouton cliquable.
    - `QLineEdit` : Champ pour saisir du texte en une ligne.
    - `QCheckBox` : Case à cocher (état binaire).
    - `QRadioButton` : Bouton radio (choix exclusif dans un groupe).

3. **Résultat visuel** :
   ```
   [QLabel]
   [QPushButton]
   [QLineEdit]
   [QCheckBox]
   [QRadioButton]
   ```

---

## **3. Exemple 2 : QHBoxLayout (Horizontal)**

### **Code complet**

```python
import sys
from PySide6.QtWidgets import (
    QApplication, QWidget, QHBoxLayout,
    QComboBox, QListWidget, QSlider, QSpinBox, QDial
)
from PySide6.QtCore import Qt  # Pour l'orientation du slider


class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Exemple de QHBoxLayout")
        self.resize(500, 100)  # Taille initiale

        # Création du layout horizontal
        layout = QHBoxLayout()

        # Ajout des widgets (alignés horizontalement)
        combo = QComboBox()
        combo.addItems(["Option 1", "Option 2", "Option 3"])
        layout.addWidget(combo)

        list_widget = QListWidget()
        list_widget.addItems(["Élément A", "Élément B", "Élément C"])
        layout.addWidget(list_widget)

        slider = QSlider(Qt.Orientation.Horizontal)
        slider.setRange(0, 100)  # Valeurs de 0 à 100
        slider.setValue(50)  # Valeur initiale
        layout.addWidget(slider)

        spinbox = QSpinBox()
        spinbox.setRange(0, 100)
        spinbox.setValue(10)
        layout.addWidget(spinbox)

        dial = QDial()
        dial.setRange(0, 100)
        dial.setValue(25)
        layout.addWidget(dial)

        # Application du layout à la fenêtre
        self.setLayout(layout)


app = QApplication(sys.argv)
window = MainWindow()
window.show()
sys.exit(app.exec())
```

### **Explications**

1. **Structure** :
    - `QHBoxLayout` dispose les widgets **horizontalement**, les uns à côté des autres.
    - Chaque widget est ajouté avec `layout.addWidget()`.

2. **Widgets utilisés** :
    - `QComboBox` : Liste déroulante pour sélectionner une option.
    - `QListWidget` : Liste d'éléments sélectionnables.
    - `QSlider` : Curseur horizontal pour choisir une valeur numérique.
    - `QSpinBox` : Champ numérique avec flèches de navigation.
    - `QDial` : Bouton rotatif (comme un cadran).

3. **Résultat visuel** :
   ```
   [QComboBox] [QListWidget] [QSlider] [QSpinBox] [QDial]
   ```

---

## **4. Comparaison des deux exemples**

| Aspect          | QVBoxLayout                     | QHBoxLayout                      |
|-----------------|---------------------------------|----------------------------------|
| **Direction**   | Vertical (haut → bas)           | Horizontal (gauche → droite)     |
| **Widgets**     | Textuels et interactifs simples | Widgets de sélection et contrôle |
| **Utilisation** | Formulaires, menus              | Barres d'outils, en-têtes        |

---

## **5. Prochaines étapes**

Ces exemples peuvent être étendus pour :

- Ajouter des signaux/slots (ex: bouton qui modifie un label).
- Combiner plusieurs layouts (`QVBoxLayout` + `QHBoxLayout`).
- Utiliser d'autres types de layouts (`QGridLayout`, `QFormLayout`).
