# **3. Éditeur de texte : menu des paramètres**

??? note "Éditeur Version 2"
      ```python
      import sys
      
      from PySide6.QtWidgets import (QApplication, QMainWindow, QTextEdit,
                                     QFileDialog, QScrollArea)
      from PySide6.QtGui import QAction, QFont
      
      
      class TextEditorApp(QMainWindow):
          def __init__(self):
              super().__init__()
              self.current_file = None
              self.init_ui()
      
          def init_ui(self):
              self.setWindowTitle('Éditeur de texte')
              self.setGeometry(100, 100, 800, 600)
      
              # Création de la zone défilante et du champ de texte
              scroll = QScrollArea()
              self.text_area = QTextEdit()
              self.text_area.setLineWrapMode(QTextEdit.LineWrapMode.NoWrap)
              self.font_size = 12  # Taille de police par défaut
              font = QFont("Courier New")
              font.setStyleHint(QFont.StyleHint.Monospace)
              font.setFixedPitch(True)
              font.setPointSize(self.font_size)
              self.text_area.setFont(font)
      
              scroll.setWidget(self.text_area)
              scroll.setWidgetResizable(True)
              self.setCentralWidget(scroll)
      
              # Création de la barre de menus
              menubar = self.menuBar()
      
              # Menu Fichier
              file_menu = menubar.addMenu('Fichier')
      
              # Action Nouveau
              new_action = QAction('Nouveau', self)
              new_action.triggered.connect(self.new_file)
      
              # Action Ouvrir
              open_action = QAction('Ouvrir...', self)
              open_action.triggered.connect(self.open_file)
      
              # Action Enregistrer
              save_action = QAction('Enregistrer', self)
              save_action.triggered.connect(self.save_file)
      
              # Action Enregistrer sous...
              save_as_action = QAction('Enregistrer sous...', self)
              save_as_action.triggered.connect(self.save_file_as)
      
              # Action Quitter
              quit_action = QAction('Quitter', self)
              quit_action.triggered.connect(self.close)
      
              # Ajout des actions au menu Fichier
              file_menu.addAction(new_action)
              file_menu.addAction(open_action)
              file_menu.addAction(save_action)
              file_menu.addAction(save_as_action)
              file_menu.addSeparator()
              file_menu.addAction(quit_action)
      
              self.create_settings_menu()
      
          def new_file(self):
              self.current_file = None
              self.text_area.clear()
      
          def open_file(self):
              file_path, _ = QFileDialog.getOpenFileName(
                  self, "Ouvrir un fichier", "", "Fichiers texte (*.txt);;Fichiers Markdown (*.md);;Tous les fichiers (*)"
              )
              if file_path:
                  try:
                      with open(file_path, 'r', encoding='utf-8') as file:
                          self.text_area.setText(file.read())
                      self.current_file = file_path
                  except Exception as e:
                      self.show_error(str(e))
      
          def save_file(self):
              if self.current_file:
                  try:
                      with open(self.current_file, 'w', encoding='utf-8') as file:
                          file.write(self.text_area.toPlainText())
                  except Exception as e:
                      self.show_error(str(e))
              else:
                  self.save_file_as()
      
          def save_file_as(self):
              file_path, _ = QFileDialog.getSaveFileName(
                  self, "Enregistrer le fichier", "", "Fichiers texte (*.txt);;Tous les fichiers (*)"
              )
              if file_path:
                  try:
                      with open(file_path, 'w') as file:
                          file.write(self.text_area.toPlainText())
                      self.current_file = file_path
                  except Exception as e:
                      self.show_error(str(e))
      
          def show_error(self, message):
              error_dialog = QFileDialog(self)
              error_dialog.setWindowTitle("Erreur")
              error_dialog.setText(message)
              error_dialog.exec()
      
          def set_textedit_font(self):
              font = QFont("Source Code Pro")
              font.setStyleHint(QFont.StyleHint.Monospace)
              font.setFixedPitch(True)
              font.setPointSize(self.font_size)
              self.text_area.setFont(font)
      
          def increase_font_size(self):
              self.font_size += 1
              self.set_textedit_font()
      
          def decrease_font_size(self):
              if self.font_size > 1:
                  self.font_size -= 1
                  self.set_textedit_font()
      
          def create_settings_menu(self):
              menubar = self.menuBar()
              settings_menu = menubar.addMenu('Paramètres')
      
              increase_font_action = QAction('Augmenter la taille de police', self)
              increase_font_action.triggered.connect(self.increase_font_size)
              settings_menu.addAction(increase_font_action)
      
              decrease_font_action = QAction('Diminuer la taille de police', self)
              decrease_font_action.triggered.connect(self.decrease_font_size)
              settings_menu.addAction(decrease_font_action)
      
      
      if __name__ == '__main__':
          app = QApplication(sys.argv)
          editor = TextEditorApp()
          editor.show()
          sys.exit(app.exec())
      ```

## **Différences clés par rapport à l'exemple précédent**

Cet éditeur de texte modifié s'appuie sur le précédent en ajoutant plusieurs nouvelles fonctionnalités importantes,
notamment dans le système de menus. Concentrons-nous sur ces différences :

## **1. Plusieurs menus**

La différence la plus significative est l'ajout d'un deuxième menu appelé "Paramètres" :

```python
def create_settings_menu(self):
    menubar = self.menuBar()
    settings_menu = menubar.addMenu('Paramètres')

    # Ajout des actions au menu Paramètres
    increase_font_action = QAction('Augmenter la taille de police', self)
    increase_font_action.triggered.connect(self.increase_font_size)
    settings_menu.addAction(increase_font_action)

    decrease_font_action = QAction('Diminuer la taille de police', self)
    decrease_font_action.triggered.connect(self.decrease_font_size)
    settings_menu.addAction(decrease_font_action)
```

Cela démontre comment créer plusieurs menus dans la barre de menus. L'application contient maintenant :

- Un menu "Fichier" pour les opérations sur les documents
- Un menu "Paramètres" pour les préférences de l'application

## **2. Organisation des menus avec une méthode séparée**

Le code utilise une méthode séparée `create_settings_menu()` pour organiser la création du menu Paramètres :

```python
def init_ui(self):
    # ... autre code ...

    # Création du menu Fichier et de ses actions
    # ... (code pour le menu Fichier) ...

    # Création du menu Paramètres en utilisant une méthode séparée
    self.create_settings_menu()
```

C'est une bonne pratique pour organiser le code lorsqu'on a plusieurs menus. Chaque menu peut avoir sa propre méthode de
configuration, rendant le code plus modulaire et plus facile à maintenir.

## **3. Actions de configuration de police**

Le menu Paramètres contient des actions qui affectent l'apparence de l'application :

```python
increase_font_action = QAction('Augmenter la taille de police', self)
increase_font_action.triggered.connect(self.increase_font_size)

decrease_font_action = QAction('Diminuer la taille de police', self)
decrease_font_action.triggered.connect(self.decrease_font_size)
```

Ces actions démontrent comment les menus peuvent contrôler les paramètres de l'application plutôt que d'effectuer
simplement des opérations sur les fichiers.

## **4. Gestion de l'état**

L'application maintient maintenant des informations d'état pour la taille de police :

```python
self.font_size = 12  # Taille de police par défaut
```

Cette variable d'état est modifiée par les actions du menu :

```python
def increase_font_size(self):
    self.font_size += 1
    self.set_textedit_font()


def decrease_font_size(self):
    if self.font_size > 1:
        self.font_size -= 1
        self.set_textedit_font()
```

Cela démontre comment les actions de menu peuvent mettre à jour l'état de l'application et déclencher des changements
visuels.

## **5. Méthodes auxiliaires pour les actions**

Le code inclut des méthodes auxiliaires qui implémentent la fonctionnalité déclenchée par les actions du menu :

```python
def set_textedit_font(self):
    font = QFont("Source Code Pro")
    font.setStyleHint(QFont.StyleHint.Monospace)
    font.setFixedPitch(True)
    font.setPointSize(self.font_size)
    self.text_area.setFont(font)
```

Cette méthode est appelée par les deux actions de taille de police, montrant comment réutiliser la fonctionnalité à
travers plusieurs éléments de menu.

## **Principes de conception des menus démontrés**

1. **Groupement logique** : Les fonctions apparentées sont regroupées dans leurs propres menus (opérations sur les
   fichiers dans "Fichier", paramètres d'apparence dans "Paramètres").

2. **Organisation hiérarchique** : La barre de menus contient plusieurs menus de niveau supérieur, chacun avec son
   propre ensemble d'actions.

3. **Nommage cohérent** : Les éléments de menu utilisent des noms clairs et orientés action qui décrivent ce qu'ils
   font.

4. **Séparation fonctionnelle** : Différents types de fonctionnalités sont séparés dans différents menus.

5. **Gestion d'état** : Les actions de menu peuvent à la fois lire et modifier l'état de l'application.

## **Applications pratiques**

Ce système de menus amélioré démontre des schémas que les étudiants peuvent appliquer à leurs propres applications :

1. **Contrôle des paramètres** : Les menus peuvent être utilisés pour contrôler les paramètres et préférences de
   l'application.

2. **Catégories de menus multiples** : Les applications peuvent organiser la fonctionnalité en plusieurs catégories
   logiques.

3. **Mises à jour dynamiques de l'interface utilisateur** : Les actions de menu peuvent déclencher des changements
   visuels dans l'application.

4. **Organisation du code** : La création de menus peut être organisée en méthodes séparées pour une meilleure structure
   de code.