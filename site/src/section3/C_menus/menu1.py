from PySide6.QtWidgets import QApplication, QMainWindow
from PySide6.QtGui import QAction

import sys

class SimpleMenuApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle('Application avec menu simple')
        self.setGeometry(100, 100, 400, 300)

        # Création de la barre de menus
        menubar = self.menuBar()

        # Ajout du menu Fichier
        file_menu = menubar.addMenu('Fichier')

        # Ajout de l'action Quitter
        quit_action = QAction('Quitter', self)
        quit_action.triggered.connect(self.close)  # Ferme l'application quand déclenché
        file_menu.addAction(quit_action)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = SimpleMenuApp()
    ex.show()
    sys.exit(app.exec())
