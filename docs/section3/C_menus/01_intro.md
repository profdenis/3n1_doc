# **1. Menus**

## **Introduction aux menus**

```python title="menu1.py"
from PySide6.QtWidgets import QApplication, QMainWindow
from PySide6.QtGui import QAction

import sys

class SimpleMenuApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle("Application avec menu simple")
        self.setGeometry(100, 100, 400, 300)

        # Création de la barre de menus
        menubar = self.menuBar()

        # Ajout du menu Fichier
        file_menu = menubar.addMenu("Fichier")

        # Ajout de l'action Quitter
        quit_action = QAction("Quitter", self)
        quit_action.triggered.connect(self.close)  # Ferme l'application quand déclenché
        file_menu.addAction(quit_action)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    ex = SimpleMenuApp()
    ex.show()
    sys.exit(app.exec())
```

Dans cet exemple, nous créons une application PySide6 simple qui démontre comment ajouter une barre de menus à votre interface graphique. Les menus sont une partie essentielle de la plupart des applications de bureau, permettant d'organiser les commandes et fonctionnalités dans une structure hiérarchique.

## **Analyse du code**

Analysons cet exemple étape par étape, en nous concentrant sur l'implémentation des menus :

```python
from PySide6.QtWidgets import QApplication, QMainWindow
from PySide6.QtGui import QAction

import sys
```

Tout d'abord, nous importons les classes nécessaires :

- `QMainWindow` : Classe principale de la fenêtre qui fournit un cadre pour construire l'interface utilisateur avec menus, barres d'outils, etc.
- `QAction` : Cette classe fournit une action d'interface utilisateur abstraite qui peut être insérée dans des menus et barres d'outils.

```python
class SimpleMenuApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.init_ui()
```

Nous créons une classe qui hérite de `QMainWindow`, ce qui nous donne automatiquement la capacité d'ajouter des menus, barres d'outils et barres d'état.

### **Processus de création de menu**

```python
def init_ui(self):
    self.setWindowTitle("Application avec menu simple")
    self.setGeometry(100, 100, 400, 300)

    # Création de la barre de menus
    menubar = self.menuBar()
```

La méthode `menuBar()` retourne la barre de menus pour la fenêtre principale. Si la barre de menus n'existe pas encore, une nouvelle est créée. C'est votre première étape dans la création des menus.

```python
# Ajout du menu Fichier
file_menu = menubar.addMenu("Fichier")
```

La méthode `addMenu()` crée un nouveau menu dans la barre de menus avec le titre 'Fichier'. Cela retourne un objet `QMenu` auquel nous pouvons ajouter des actions.

```python
# Ajout de l'action Quitter
quit_action = QAction("Quitter", self)
quit_action.triggered.connect(self.close)  # Ferme l'application quand déclenché
file_menu.addAction(quit_action)
```

Voici où nous créons un élément de menu :

1. Nous créons une `QAction` avec le texte 'Quitter'
2. Nous connectons son signal `triggered` à la méthode `close()` de notre fenêtre
3. Nous ajoutons cette action à notre menu Fichier en utilisant `addAction()`

Quand un utilisateur clique sur "Fichier" dans la barre de menus, une liste déroulante apparaît avec "Quitter" comme option. Cliquer sur "Quitter" déclenchera l'action, qui appellera `self.close()` pour fermer l'application.

## **Concepts clés sur les menus**

1. **Hiérarchie des menus** : Les menus dans PySide6 suivent une hiérarchie :
   - Barre de menus (niveau supérieur)
   - Menus (comme Fichier, Édition, Affichage)
   - Actions (les commandes réelles que les utilisateurs peuvent sélectionner)

2. **QAction** : Cette classe représente un élément qu'un utilisateur peut sélectionner dans un menu. Les actions peuvent :
   - Afficher du texte et/ou une icône
   - Avoir un raccourci clavier
   - Montrer des infobulles d'état
   - Émettre un signal quand activées

3. **Mécanisme signal-slot** : La ligne `quit_action.triggered.connect(self.close)` démontre le mécanisme signal-slot de PySide6. Quand l'action est déclenchée (cliquée), elle émet un signal qui est connecté au slot `close()`.

## **Exemple d'extension**

Pour ajouter plus d'actions à votre menu :

```python
# Ajout d'une action Nouveau dans le menu Fichier
new_action = QAction("Nouveau", self)
new_action.setShortcut("Ctrl+N")  # Raccourci clavier
file_menu.addAction(new_action)

# Connexion de l'action Nouveau à une méthode
new_action.triggered.connect(self.create_new_file)
```

Cette approche permet de créer des interfaces utilisateur riches et intuitives avec des menus complets.