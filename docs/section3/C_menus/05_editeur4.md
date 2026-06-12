# **5. Éditeur de texte : Gestion de l'état du document**

??? note "Éditeur Version 4"
      ```python
      import sys
      
      from PySide6.QtWidgets import (QApplication, QMainWindow, QTextEdit,
                                     QFileDialog, QScrollArea, QToolBar, QLabel, QMessageBox)
      from PySide6.QtGui import QAction, QFont, QShortcut, QKeySequence
      from PySide6.QtCore import Qt, Signal
      
      
      class TextEditorApp(QMainWindow):
          def __init__(self):
              super().__init__()
              self.is_modified = None  # Indique si le document a été modifié
              self.current_file = None
              self.init_ui()
      
          def init_ui(self):
              self.setWindowTitle('Éditeur de texte')
              self.setGeometry(100, 100, 800, 600)
      
              self.create_text_edit()
              self.create_file_menu()
              self.create_settings_menu()
              self.add_toolbar()
              self.add_shortcuts()
      
          def mark_modified(self):
              """Marque le document comme modifié."""
              self.is_modified = True
      
          def create_text_edit(self):
              # Création de la zone défilante et du champ de texte
              self.text_edit = WheelAwareTextEdit()
              self.text_edit.ctrl_wheel.connect(self.handle_ctrl_wheel)
              self.text_edit.setLineWrapMode(QTextEdit.LineWrapMode.NoWrap)
              self.text_edit.textChanged.connect(self.mark_modified)  # Connexion au signal de modification
      
              self.font_size = 12  # Taille de police par défaut
              font = QFont("Courier New")
              font.setStyleHint(QFont.StyleHint.Monospace)
              font.setFixedPitch(True)
              font.setPointSize(self.font_size)
              self.text_edit.setFont(font)
      
              scroll = QScrollArea()
              scroll.setWidget(self.text_edit)
              scroll.setWidgetResizable(True)
      
              self.setCentralWidget(scroll)
      
          def create_file_menu(self):
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
              # Ajout des actions au menu
              file_menu.addAction(new_action)
              file_menu.addAction(open_action)
              file_menu.addAction(save_action)
              file_menu.addAction(save_as_action)
              file_menu.addSeparator()
              file_menu.addAction(quit_action)
      
          def new_file(self):
              """Crée un nouveau document."""
              if not self.maybe_save():  # Vérifie si on doit sauvegarder
                  return
              self.current_file = None
              self.text_edit.clear()
              self.is_modified = False
      
          def open_file(self):
              """Ouvre un fichier existant."""
              if not self.maybe_save():
                  return
              file_path, _ = QFileDialog.getOpenFileName(
                  self, "Ouvrir un fichier", "", "Fichiers texte (*.txt);;Fichiers Markdown (*.md);;Tous les fichiers (*)"
              )
              if file_path:
                  try:
                      with open(file_path, 'r', encoding='utf-8') as file:
                          self.text_edit.setText(file.read())
                      self.current_file = file_path
                      self.is_modified = False
                  except Exception as e:
                      self.show_error(str(e))
      
          def save_file(self):
              """Enregistre le fichier actuel."""
              if self.current_file:
                  try:
                      with open(self.current_file, 'w', encoding='utf-8') as file:
                          file.write(self.text_edit.toPlainText())
                      self.is_modified = False  # Réinitialise l'indicateur de modification
                  except Exception as e:
                      self.show_error(str(e))
              else:
                  self.save_file_as()
      
          def save_file_as(self):
              """Enregistre le fichier sous un nouveau nom."""
              file_path, _ = QFileDialog.getSaveFileName(
                  self, "Enregistrer le fichier", "", "Fichiers texte (*.txt);;Tous les fichiers (*)"
              )
              if file_path:
                  try:
                      with open(file_path, 'w') as file:
                          file.write(self.text_edit.toPlainText())
                      self.current_file = file_path
                      self.is_modified = False
                  except Exception as e:
                      self.show_error(str(e))
      
          def maybe_save(self):
              """
              Vérifie s'il y a des modifications non sauvegardées et demande à l'utilisateur de les sauvegarder.
              Si le document n'a pas été modifié ou si l'utilisateur confirme l'action, la méthode retourne True.
              Sinon, selon la réponse de l'utilisateur, elle peut demander de sauvegarder, abandonner les modifications
              ou annuler.
      
              QMessageBox.StandardButton.Yes: Sauvegarde le fichier et poursuit après confirmation.
              QMessageBox.StandardButton.No: Abandonne les modifications non sauvegardées et poursuit après confirmation.
              QMessageBox.StandardButton.Cancel: Annule l'opération et ne prend pas d'autre action.
      
              :return:
                  True si l'utilisateur choisit de sauvegarder ou d'abandonner les modifications,
                  ou s'il n'y a pas de modifications non sauvegardées.
                  False si l'utilisateur annule l'action.
              :rtype: bool
              """
              if self.is_modified:
                  reply = QMessageBox.question(
                      self, "Modifications non sauvegardées",
                      "Vous avez des modifications non sauvegardées. Voulez-vous les sauvegarder ?",
                      QMessageBox.StandardButton.Yes |
                      QMessageBox.StandardButton.No |
                      QMessageBox.StandardButton.Cancel
                  )
                  if reply == QMessageBox.StandardButton.Yes:
                      self.save_file()
                      return True
                  elif reply == QMessageBox.StandardButton.No:
                      return True
                  else:
                      return False
              return True
      
          def show_error(self, message):
              """Affiche une boîte de dialogue d'erreur."""
              error_dialog = QFileDialog(self)
              error_dialog.setWindowTitle("Erreur")
              error_dialog.setText(message)
              error_dialog.exec()
      
          def set_textedit_font(self):
              """Définie la police du champ de texte."""
              font = QFont("Source Code Pro")
              font.setStyleHint(QFont.StyleHint.Monospace)
              font.setFixedPitch(True)
              font.setPointSize(self.font_size)
              self.text_edit.setFont(font)
      
          def increase_font_size(self):
              """Augmente la taille de police."""
              self.font_size += 1
              self.set_textedit_font()
      
          def decrease_font_size(self):
              """Diminue la taille de police."""
              if self.font_size > 1:
                  self.font_size -= 1
                  self.set_textedit_font()
      
          def create_settings_menu(self):
              """Crée le menu Paramètres."""
              menubar = self.menuBar()
              settings_menu = menubar.addMenu('Paramètres')
      
              increase_font_action = QAction('Augmenter la taille de police', self)
              increase_font_action.triggered.connect(self.increase_font_size)
              settings_menu.addAction(increase_font_action)
      
              decrease_font_action = QAction('Diminuer la taille de police', self)
              decrease_font_action.triggered.connect(self.decrease_font_size)
              settings_menu.addAction(decrease_font_action)
      
          def add_toolbar(self):
              """Ajoute une barre d'outils."""
              toolbar = QToolBar("Outils de police")
              self.addToolBar(toolbar)
      
              toolbar.addWidget(QLabel("Taille de police:"))
              toolbar.addAction("+", self.increase_font_size)
              toolbar.addAction("-", self.decrease_font_size)
      
          def add_shortcuts(self):
              """Ajoute des raccourcis clavier."""
              QShortcut(QKeySequence("Ctrl++"), self).activated.connect(self.increase_font_size)
              QShortcut(QKeySequence("Ctrl+-"), self).activated.connect(self.decrease_font_size)
      
          def handle_ctrl_wheel(self, delta):
              """Gère l'événement de molette avec Ctrl enfoncé."""
              if delta > 0:  # Molette scrollée vers le haut
                  self.increase_font_size()
              else:  # Molette scrollée vers le bas
                  self.decrease_font_size()
      
          def closeEvent(self, event):
              """Gère l'événement de fermeture de la fenêtre."""
              if self.maybe_save():  # Vérifie si on doit sauvegarder avant de fermer
                  event.accept()
              else:
                  event.ignore()
      
      
      class WheelAwareTextEdit(QTextEdit):
          ctrl_wheel = Signal(int)  # Émet la valeur de défilement
      
          def wheelEvent(self, event):
              """Surcharge l'événement de molette pour détecter Ctrl+molette."""
              if event.modifiers() & Qt.KeyboardModifier.ControlModifier:
                  self.ctrl_wheel.emit(event.angleDelta().y())
                  event.accept()
              else:
                  super().wheelEvent(event)
      
      
      if __name__ == '__main__':
          app = QApplication(sys.argv)
          editor = TextEditorApp()
          editor.show()
          sys.exit(app.exec())
      ```

## **Modifications clés dans cette version**

Cette version de l'éditeur de texte introduit un concept important dans les applications basées sur des documents : le
suivi et la gestion de l'état de modification du document. Concentrons-nous sur ces changements et leur impact sur le
flux de travail piloté par les menus.

## **1. Suivi des modifications du document**

L'ajout le plus significatif est le suivi de la modification du document :

```python
def __init__(self):
    super().__init__()
    self.is_modified = None  # Nouvelle variable d'état
    self.current_file = None
    self.init_ui()
```

L'application maintient maintenant un indicateur `is_modified` pour suivre si le document a des modifications non
sauvegardées.

```python
def create_text_edit(self):
    # ...
    self.text_edit.textChanged.connect(self.mark_modified)
    # ...
```

```python
def mark_modified(self):
    self.is_modified = True
```

L'application se connecte au signal `textChanged` de l'éditeur de texte, qui est émis chaque fois que le texte est
modifié. Cela définit automatiquement l'indicateur `is_modified` à `True`.

## **2. Boîte de dialogue pour les modifications non sauvegardées**

Une amélioration majeure est l'ajout d'une boîte de confirmation lorsque l'on tente de fermer un document avec des
modifications non sauvegardées :

```python
def maybe_save(self):
    if self.is_modified:
        reply = QMessageBox.question(
            self, "Modifications non sauvegardées",
            "Vous avez des modifications non sauvegardées. Voulez-vous les sauvegarder ?",
            QMessageBox.StandardButton.Yes |
            QMessageBox.StandardButton.No |
            QMessageBox.StandardButton.Cancel
        )
        if reply == QMessageBox.StandardButton.Yes:
            self.save_file()
            return True
        elif reply == QMessageBox.StandardButton.No:
            return True
        else:
            return False
    return True
```

Cette méthode :

1. Vérifie si le document a été modifié
2. Si modifié, affiche une boîte de dialogue demandant à l'utilisateur s'il souhaite sauvegarder les modifications
3. Gère la réponse de l'utilisateur (Oui, Non ou Annuler)
4. Retourne `True` si l'opération doit continuer, `False` si elle doit être annulée

## **3. Intégration avec les opérations sur les fichiers**

La méthode `maybe_save()` est maintenant appelée avant les opérations qui abandonneraient le document actuel :

```python
def new_file(self):
    if not self.maybe_save():
        return
    self.current_file = None
    self.text_edit.clear()
```

```python
def open_file(self):
    if not self.maybe_save():
        return
    # ... reste du code de open_file ...
```

Cela garantit que les utilisateurs sont invités à sauvegarder les modifications non sauvegardées avant que ces
opérations ne se poursuivent.

## **4. Réinitialisation de l'indicateur de modification**

Lorsque qu'un fichier est sauvegardé ou ouvert, l'indicateur `is_modified` est réinitialisé à `False` :

```python
def save_file(self):
    if self.current_file:
        try:
            with open(self.current_file, 'w', encoding='utf-8') as file:
                file.write(self.text_edit.toPlainText())
            self.is_modified = False  # Réinitialise l'indicateur de modification après sauvegarde
        except Exception as e:
            self.show_error(str(e))
    else:
        self.save_file_as()
```

Un code similaire apparaît dans `save_file_as()` et `open_file()`.

## **5. Gestion des événements de fermeture de l'application**

L'application intercepte maintenant les événements de fermeture pour vérifier les modifications non sauvegardées :

```python
def closeEvent(self, event):
    if self.maybe_save():
        event.accept()
    else:
        event.ignore()
```

Cela garantit que les utilisateurs sont invités à sauvegarder les modifications non sauvegardées même lors de la
fermeture de la fenêtre de l'application.

## **Impact sur le flux de travail piloté par les menus**

Ces changements améliorent considérablement le flux de travail piloté par les menus en :

1. **Prévenant la perte de données** : L'application empêche maintenant les utilisateurs de perdre accidentellement leur
   travail non sauvegardé.
2. **Fournissant des choix adaptés au contexte** : Les utilisateurs se voient proposer des options appropriées (
   Sauvegarder, Ne pas sauvegarder, Annuler) lors d'actions qui abandonneraient les modifications.
3. **Maintenant l'état du document** : L'application suit l'état du document et fournit des feedbacks et options
   appropriés en fonction de cet état.
4. **Comportement cohérent** : La même gestion de l'état du document s'applique que l'on utilise des commandes de menu,
   des raccourcis clavier ou des événements de fermeture de fenêtre.

## **Comportement standard d'une application**

Cette version implémente un comportement que les utilisateurs attendent des applications professionnelles d'édition de
documents :

1. **Indicateur de document modifié** : L'application suit si le document a été modifié.
2. **Invitations à sauvegarder** : Les utilisateurs sont invités à sauvegarder les modifications avant les actions qui
   les abandonneraient.
3. **Option d'annulation** : Les utilisateurs peuvent annuler les opérations qui abandonneraient leur travail.
4. **Gestion cohérente de l'état** : L'état modifié est mis à jour de manière cohérente dans toutes les opérations.

## **Enseignements pratiques pour les étudiants**

1. **Gestion d'état** : Le suivi de l'état de l'application (comme la modification du document) est crucial pour fournir
   une bonne expérience utilisateur.
2. **Confirmation utilisateur** : Demandez toujours confirmation aux utilisateurs avant des actions potentiellement
   destructrices.
3. **Connexions de signaux** : Connectez-vous à des signaux appropriés (comme `textChanged`) pour maintenir les
   informations d'état à jour.
4. **Gestion des événements** : Remplacez les événements comme `closeEvent` pour intégrer la gestion de l'état avec les
   interactions au niveau système.
5. **Comportement cohérent** : Assurez un comportement cohérent dans toutes les façons de déclencher la même
   fonctionnalité.

Cet exemple démontre comment construire une application plus robuste et conviviale qui protège le travail des
utilisateurs tout en maintenant une interface propre pilotée par les menus.