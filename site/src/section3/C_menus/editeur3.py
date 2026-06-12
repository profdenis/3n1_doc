import sys

from PySide6.QtWidgets import (QApplication, QMainWindow, QTextEdit,
                               QFileDialog, QScrollArea, QToolBar, QLabel)
from PySide6.QtGui import QAction, QFont, QShortcut, QKeySequence
from PySide6.QtCore import Qt, Signal

class TextEditorApp(QMainWindow):
    def __init__(self):
        super().__init__()
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

    def create_text_edit(self):
        # Création de la zone défilante et du champ de texte
        self.text_area = WheelAwareTextEdit()
        self.text_area.ctrl_wheel.connect(self.handle_ctrl_wheel)
        self.text_area.setLineWrapMode(QTextEdit.LineWrapMode.NoWrap)

        self.font_size = 12  # Taille de police par défaut
        font = QFont("Courier New")
        font.setStyleHint(QFont.StyleHint.Monospace)
        font.setFixedPitch(True)
        font.setPointSize(self.font_size)
        self.text_area.setFont(font)

        scroll = QScrollArea()
        scroll.setWidget(self.text_area)
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

    def add_toolbar(self):
        toolbar = QToolBar("Outils de police")
        self.addToolBar(toolbar)

        toolbar.addWidget(QLabel("Taille de police:"))
        toolbar.addAction("+", self.increase_font_size)
        toolbar.addAction("-", self.decrease_font_size)

    def add_shortcuts(self):
        QShortcut(QKeySequence("Ctrl++"), self).activated.connect(self.increase_font_size)
        QShortcut(QKeySequence("Ctrl+-"), self).activated.connect(self.decrease_font_size)

    def handle_ctrl_wheel(self, delta):
        if delta > 0:  # Molette scrollée vers le haut
            self.increase_font_size()
        else:  # Molette scrollée vers le bas
            self.decrease_font_size()

class WheelAwareTextEdit(QTextEdit):
    ctrl_wheel = Signal(int)  # Émet la valeur de défilement

    def wheelEvent(self, event):
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
