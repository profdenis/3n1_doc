# **Interfaces Graphiques avec PySide6 et Qt**

## **1. Introduction à Qt et PySide6**

### **1.1 Qu'est-ce que Qt ?**

Qt est un framework open-source pour le développement d'applications graphiques (GUI) multiplateformes. Il est écrit en
C++ mais propose des bindings pour plusieurs langages, dont Python via **PySide** (maintenu par Qt) ou PyQt (maintenu
par une tierce partie).

### **1.2 Pourquoi utiliser PySide6 ?**

- **Multiplateforme** : Une seule base de code pour Windows, macOS et Linux.
- **Richesse des widgets** : Boutons, tableaux, graphiques, etc., prêts à l'emploi.
- **Intégration avec Python** : Syntaxe simple et accès aux fonctionnalités avancées de Qt.

### **1.3 Historique rapide**

- **1991** : Création de Qt par Trolltech (Norvège).
- **2008** : Acquisition par Nokia, puis par Digia en 2012.
- **2014** : Qt devient une société indépendante.
- **PySide6** : Version moderne (Qt6) avec support Python 3.7+.

---

## **2. Installation de PySide6**

### **2.1 Sous Linux (Ubuntu/Debian)**

```bash
sudo apt update
sudo apt install python3-pyside6
```

*Vérification* :

```python
from PySide6.QtWidgets import QApplication, QLabel

print("PySide6 installé !")
```

### **2.2 Sous Windows**

- **Via pip** (recommandé) :
  ```bash
  pip install pyside6
  ```
- **Via l'installateur Qt** : [Télécharger Qt](https://www.qt.io/download) (optionnel pour les outils de développement).

### **2.3 Sous macOS**

```bash
brew install python
pip install pyside6
```

### **2.4 Installation via PyCharm**

1. Ouvrir PyCharm → `File` → `Settings` → `Project: [votre projet]` → `Python Interpreter`.
2. Cliquer sur `+` → `Install` → Taper `pyside6` → Installer.

---

## **3. Exemple "Hello World"**

### **Code complet**

```python
import sys
from PySide6.QtWidgets import QApplication, QLabel

# Création de l'application Qt
app = QApplication(sys.argv)

# Widget principal (une étiquette avec du texte)
label = QLabel("Hello, World!")
label.show()  # Affiche la fenêtre

# Exécution de la boucle principale
sys.exit(app.exec())
```

### **Explication ligne par ligne**

1. **`import sys`** : Nécessaire pour gérer les arguments de la ligne de commande.
2. **`QApplication`** : Classe centrale de Qt qui gère l'application et ses événements.
3. **`QLabel`** : Widget simple affichant du texte (ou une image).
4. **`label.show()`** : Rend le widget visible à l'écran.
5. **`app.exec()`** : Lance la boucle d'événements (attend les interactions utilisateur).

---

## **4. Structure de base d'une application Qt**

### **Diagramme simplifié**

```
QApplication
   │
   ├── QWidget (ou sous-classe comme QMainWindow)
   │    │
   │    ├── QLabel, QPushButton, etc.
   │    └── Layouts (QVBoxLayout, QHBoxLayout)
   │
   └── Event Loop (app.exec())
```

### **Exemple avec une fenêtre principale**

```python
import sys
from PySide6.QtWidgets import QMainWindow, QPushButton, QApplication

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Ma Fenêtre")
        button = QPushButton("Cliquez-moi !")
        self.setCentralWidget(button)  # Ajoute le bouton au centre


app = QApplication(sys.argv)
window = MainWindow()
window.show()
sys.exit(app.exec())
```

---

### **Ressources utiles**

- [Documentation officielle PySide6](https://doc.qt.io/qtforpython/)
- [Tutoriel Qt pour débutants](https://wiki.qt.io/Category:Tutorials)
