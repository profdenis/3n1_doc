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
