# **2. Éditeur de texte simple**

Cet exemple s'appuie sur notre précédent exemple de menu pour créer un éditeur de texte fonctionnel avec un système de
menus plus complet. Concentrons-nous sur la manière dont les menus sont implémentés et comment ils se connectent à la
fonctionnalité de l'application.

```python title="editeur1.py"
import sys

from PySide6.QtWidgets import (QApplication, QMainWindow, QTextEdit,
                               QFileDialog, QScrollArea)
from PySide6.QtGui import QAction


class TextEditorApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.current_file = None
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle("Éditeur de texte")
        self.setGeometry(100, 100, 800, 600)

        # Création de la zone défilante et du champ de texte
        scroll = QScrollArea()
        self.text_area = QTextEdit()
        self.text_area.setLineWrapMode(QTextEdit.LineWrapMode.NoWrap)
        scroll.setWidget(self.text_area)
        scroll.setWidgetResizable(True)
        self.setCentralWidget(scroll)

        # Création de la barre de menus
        menubar = self.menuBar()

        # Menu Fichier
        file_menu = menubar.addMenu("Fichier")

        # Action Nouveau
        new_action = QAction("Nouveau", self)
        new_action.triggered.connect(self.new_file)

        # Action Ouvrir
        open_action = QAction("Ouvrir...", self)
        open_action.triggered.connect(self.open_file)

        # Action Enregistrer
        save_action = QAction("Enregistrer", self)
        save_action.triggered.connect(self.save_file)

        # Action Enregistrer sous...
        save_as_action = QAction("Enregistrer sous...", self)
        save_as_action.triggered.connect(self.save_file_as)

        # Action Quitter
        quit_action = QAction("Quitter", self)
        quit_action.triggered.connect(self.close)

        # Ajout des actions au menu
        file_menu.addAction(new_action)
        file_menu.addAction(open_action)
        file_menu.addAction(save_action)
        file_menu.addAction(save_as_action)
        file_menu.addSeparator()  # Ajoute une ligne horizontale dans le menu
        file_menu.addAction(quit_action)

    def new_file(self):
        self.current_file = None
        self.text_area.clear()

    def open_file(self):
        file_path, _ = QFileDialog.getOpenFileName(
            self, "Ouvrir un fichier", "", "Fichiers texte (*.txt);;Fichiers Markdown (*.md);;Tous les fichiers (*)"
        )
        if file_path:
            try:
                with open(file_path, "r", encoding="utf-8") as file:
                    self.text_area.setText(file.read())
                self.current_file = file_path
            except Exception as e:
                self.show_error(str(e))

    def save_file(self):
        if self.current_file:
            try:
                with open(self.current_file, "w", encoding="utf-8") as file:
                    file.write(self.text_area.toPlainText())
            except Exception as e:
                self.show_error(str(e))
        else:
            self.save_file_as()

    def save_file_as(self):
        file_path, _ = QFileDialog.getSaveFileName(
            self, "Enregistrer le fichier", "",
            "Fichiers texte (*.txt);;Fichiers Markdown (*.md);;Tous les fichiers (*)"
        )
        if file_path:
            try:
                with open(file_path, "w", encoding="utf-8") as file:
                    file.write(self.text_area.toPlainText())
                self.current_file = file_path
            except Exception as e:
                self.show_error(str(e))

    def show_error(self, message):
        error_dialog = QFileDialog(self)
        error_dialog.setWindowTitle("Erreur")
        error_dialog.setText(message)
        error_dialog.exec()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    editor = TextEditorApp()
    editor.show()
    sys.exit(app.exec())
```

## **Structure du menu dans cet exemple**

Dans cette application d'éditeur de texte, nous créons une structure de menu plus sophistiquée avec plusieurs actions et
un séparateur :

```python
# Création de la barre de menus
menubar = self.menuBar()

# Menu Fichier
file_menu = menubar.addMenu("Fichier")
```

Comme dans notre précédent exemple, nous commençons par obtenir la barre de menus et y ajouter un menu 'Fichier'.

### **Création de plusieurs actions de menu**

```python
# Action Nouveau
new_action = QAction("Nouveau", self)
new_action.triggered.connect(self.new_file)

# Action Ouvrir
open_action = QAction("Ouvrir...", self)
open_action.triggered.connect(self.open_file)

# Action Enregistrer
save_action = QAction("Enregistrer", self)
save_action.triggered.connect(self.save_file)

# Action Enregistrer sous...
save_as_action = QAction("Enregistrer sous...", self)
save_as_action.triggered.connect(self.save_file_as)

# Action Quitter
quit_action = QAction("Quitter", self)
quit_action.triggered.connect(self.close)
```

Nous créons cinq actions différentes pour notre menu Fichier :

1. **Nouveau** - Crée un nouveau document vide
2. **Ouvrir...** - Ouvre un fichier existant
3. **Enregistrer** - Enregistre le fichier actuel
4. **Enregistrer sous...** - Enregistre le fichier actuel avec un nouveau nom
5. **Quitter** - Quitte l'application

Chaque action suit le même schéma :

- Créer une `QAction` avec une étiquette descriptive
- Connecter son signal `triggered` à la méthode appropriée

### **Ajout des actions au menu avec un séparateur**

```python
# Ajout des actions au menu
file_menu.addAction(new_action)
file_menu.addAction(open_action)
file_menu.addAction(save_action)
file_menu.addAction(save_as_action)
file_menu.addSeparator()  # Cela ajoute une ligne horizontale dans le menu
file_menu.addAction(quit_action)
```

Après avoir créé les actions, nous les ajoutons au menu. Remarquez la méthode `addSeparator()`, qui ajoute une ligne
horizontale entre les éléments de menu. C'est un motif d'interface utilisateur courant utilisé pour regrouper des
actions apparentées. Dans ce cas, il sépare les opérations sur les fichiers de la commande de sortie de l'application.

## **Connexion des actions de menu à la fonctionnalité**

Chaque action de menu est connectée à une méthode qui effectue l'opération correspondante :

```python
def new_file(self):
    self.current_file = None
    self.text_area.clear()
```

La méthode `new_file` réinitialise le fichier actuel à `None` et efface la zone de texte.

```python
def open_file(self):
    file_path, _ = QFileDialog.getOpenFileName(
        self, "Ouvrir un fichier", "", "Fichiers texte (*.txt);;Fichiers Markdown (*.md);;Tous les fichiers (*)"
    )
    if file_path:
        try:
            with open(file_path, "r", encoding="utf-8") as file:
                self.text_area.setText(file.read())
            self.current_file = file_path
        except Exception as e:
            self.show_error(str(e))
```

La méthode `open_file` utilise `QFileDialog.getOpenFileName()` pour afficher une boîte de dialogue de sélection de
fichier. Si un fichier est sélectionné, il lit le contenu et l'affiche dans la zone de texte.

Des implémentations similaires existent pour `save_file` et `save_file_as`.

## **Concepts clés des menus démontrés**

1. **Actions multiples** : Un menu du monde réel contient généralement plusieurs actions apparentées.
2. **Séparateurs** : La méthode `addSeparator()` ajoute une séparation visuelle entre les groupes d'éléments de menu
   apparentés.
3. **Intégration des boîtes de dialogue** : Les actions de menu déclenchent souvent des boîtes de dialogue, comme les
   boîtes de dialogue d'ouverture/enregistrement de fichiers montrées ici.
4. **Nommage conventionnel** : Remarquez comment les éléments de menu qui ouvrent des boîtes de dialogue se terminent
   par "..." (par exemple, "Ouvrir..."). C'est une convention d'interface utilisateur indiquant que la sélection de
   cette option nécessitera une entrée supplémentaire.
5. **Gestion des erreurs** : Les méthodes connectées aux actions de menu incluent une gestion des erreurs pour gérer les
   problèmes potentiels.

## **Bonnes pratiques pour la conception de menus**

1. **Groupement logique** : Regroupez les actions apparentées ensemble (les opérations sur les fichiers sont regroupées,
   avec Quitter séparé).
2. **Menus standards** : Suivez les conventions pour les noms et l'organisation des menus (Fichier, Édition, Affichage,
   etc.).
3. **Étiquettes claires** : Utilisez des étiquettes claires et concises pour les éléments de menu.
4. **Terminologie cohérente** : Utilisez des termes cohérents dans toute votre application.

Cet exemple démontre comment créer un système de menus pratique qui suit les conventions d'interface utilisateur
standard et se connecte à la fonctionnalité réelle de l'application. Les étudiants peuvent utiliser cela comme modèle
pour créer leurs propres applications pilotées par des menus.
