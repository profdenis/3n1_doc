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
