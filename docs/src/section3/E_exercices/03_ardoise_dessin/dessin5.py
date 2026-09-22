import sys
from PySide6.QtWidgets import (QApplication, QMainWindow, QWidget,
                               QVBoxLayout, QHBoxLayout, QLabel,
                               QSlider, QSpinBox, QPushButton, QColorDialog,
                               QFileDialog, QMessageBox)
from PySide6.QtCore import Qt, QPoint, Signal
from PySide6.QtGui import (QPainter, QPen, QColor, QPixmap,
                           QAction, QActionGroup, QKeySequence)


class CanvasWidget(QWidget):
    """Widget de dessin personnalisé gérant les événements de la souris."""
    drawing_changed = Signal()
    mouse_moved = Signal(QPoint)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setFixedSize(600, 400)
        self.setMouseTracking(True)  # Suivre les mouvements même sans clic

        # Création d'un pixmap blanc sur lequel dessiner
        self.pixmap = QPixmap(self.size())
        self.pixmap.fill(Qt.GlobalColor.white)

        # Propriétés du tracé
        self.pen_color = QColor("black")
        self.pen_width = 3
        self.mode = "pen"  # "pen" ou "eraser"
        self.last_point = None

    def set_pen_width(self, width):
        """Modifie l'épaisseur du pinceau."""
        self.pen_width = width

    def set_pen_color(self, color):
        """Modifie la couleur du pinceau."""
        self.pen_color = color

    def set_mode(self, mode):
        """Définit le mode d'outil ('pen' ou 'eraser')."""
        self.mode = mode

    def clear_canvas(self):
        """Efface tout le contenu du canevas en le repeignant en blanc."""
        self.pixmap.fill(Qt.GlobalColor.white)
        self.update()
        self.drawing_changed.emit()

    def paintEvent(self, event):
        """Dessine le pixmap sur la surface du widget."""
        painter = QPainter(self)
        painter.drawPixmap(0, 0, self.pixmap)

    def mousePressEvent(self, event):
        """Enregistre le point de départ lors du clic gauche."""
        if event.button() == Qt.MouseButton.LeftButton:
            self.last_point = event.position().toPoint()

    def mouseMoveEvent(self, event):
        """Met à jour la position du curseur et trace si le bouton gauche est enfoncé."""
        current_point = event.position().toPoint()
        self.mouse_moved.emit(current_point)

        if (event.buttons() & Qt.MouseButton.LeftButton) and self.last_point is not None:
            painter = QPainter(self.pixmap)

            # Couleur selon le mode actif
            draw_color = Qt.GlobalColor.white if self.mode == "eraser" else self.pen_color
            pen = QPen(
                draw_color,
                self.pen_width,
                Qt.PenStyle.SolidLine,
                Qt.PenCapStyle.RoundCap,
                Qt.PenJoinStyle.RoundJoin
            )
            painter.setPen(pen)

            painter.drawLine(self.last_point, current_point)
            painter.end()

            self.last_point = current_point
            self.update()
            self.drawing_changed.emit()

    def mouseReleaseEvent(self, event):
        """Réinitialise le point de tracé lorsque le clic est relâché."""
        if event.button() == Qt.MouseButton.LeftButton:
            self.last_point = None


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Ardoise de dessin")
        self.is_modified = False

        # Canevas de dessin
        self.canvas = CanvasWidget()
        self.canvas.drawing_changed.connect(self.on_drawing_changed)
        self.canvas.mouse_moved.connect(self.on_mouse_moved)

        # Menus, barre d'outils et barre d'état
        self.create_menu_bar()
        self.create_tool_bar()
        self.statusBar()

        # Widget central et layout principal
        central_widget = QWidget()
        layout = QVBoxLayout()

        # Barre de contrôle (épaisseur et couleur)
        control_layout = QHBoxLayout()
        control_layout.addWidget(QLabel("Épaisseur :"))

        self.width_slider = QSlider(Qt.Orientation.Horizontal)
        self.width_slider.setRange(1, 30)
        self.width_slider.setValue(3)

        self.width_spinbox = QSpinBox()
        self.width_spinbox.setRange(1, 30)
        self.width_spinbox.setValue(3)

        # Synchronisation slider / spinbox
        self.width_slider.valueChanged.connect(self.width_spinbox.setValue)
        self.width_spinbox.valueChanged.connect(self.width_slider.setValue)
        self.width_slider.valueChanged.connect(self.canvas.set_pen_width)
        self.width_slider.valueChanged.connect(self.update_status_message)

        control_layout.addWidget(self.width_slider)
        control_layout.addWidget(self.width_spinbox)

        # Contrôles de sélection de couleur
        control_layout.addSpacing(15)
        self.color_button = QPushButton("Couleur...")
        self.color_button.clicked.connect(self.choose_color)
        control_layout.addWidget(self.color_button)

        # Aperçu de la couleur sélectionnée
        self.color_sample = QLabel()
        self.color_sample.setFixedSize(24, 24)
        self.color_sample.setStyleSheet(
            f"background-color: {self.canvas.pen_color.name()}; border: 1px solid #333;"
        )
        control_layout.addWidget(self.color_sample)

        control_layout.addStretch()

        layout.addLayout(control_layout)
        layout.addWidget(self.canvas)

        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)

        self.cursor_pos = QPoint(0, 0)
        self.update_status_message()

    def create_menu_bar(self):
        """Crée la barre de menus avec les actions Fichier."""
        menubar = self.menuBar()
        file_menu = menubar.addMenu("Fichier")

        new_action = QAction("Nouveau dessin", self)
        new_action.setShortcut(QKeySequence.StandardKey.New)
        new_action.triggered.connect(self.new_drawing)
        file_menu.addAction(new_action)

        save_action = QAction("Enregistrer sous...", self)
        save_action.setShortcut(QKeySequence.StandardKey.Save)
        save_action.triggered.connect(self.save_image)
        file_menu.addAction(save_action)

        file_menu.addSeparator()

        quit_action = QAction("Quitter", self)
        quit_action.setShortcut(QKeySequence.StandardKey.Quit)
        quit_action.triggered.connect(self.close)
        file_menu.addAction(quit_action)

    def create_tool_bar(self):
        """Crée la barre d'outils avec les modes Pinceau, Gomme et Effacer."""
        toolbar = self.addToolBar("Outils")

        tool_group = QActionGroup(self)

        self.pen_action = QAction("Pinceau", self)
        self.pen_action.setCheckable(True)
        self.pen_action.setChecked(True)
        self.pen_action.triggered.connect(lambda: self.set_tool_mode("pen"))
        tool_group.addAction(self.pen_action)
        toolbar.addAction(self.pen_action)

        self.eraser_action = QAction("Gomme", self)
        self.eraser_action.setCheckable(True)
        self.eraser_action.triggered.connect(lambda: self.set_tool_mode("eraser"))
        tool_group.addAction(self.eraser_action)
        toolbar.addAction(self.eraser_action)

        toolbar.addSeparator()

        clear_action = QAction("Effacer tout", self)
        clear_action.triggered.connect(self.canvas.clear_canvas)
        toolbar.addAction(clear_action)

    def set_tool_mode(self, mode):
        """Modifie le mode de tracé et met à jour l'affichage."""
        self.canvas.set_mode(mode)
        self.update_status_message()

    def choose_color(self):
        """Ouvre une boîte de dialogue standard pour sélectionner une couleur."""
        color = QColorDialog.getColor(self.canvas.pen_color, self, "Choisir la couleur du pinceau")
        if color.isValid():
            self.canvas.set_pen_color(color)
            self.color_sample.setStyleSheet(
                f"background-color: {color.name()}; border: 1px solid #333;"
            )
            self.pen_action.setChecked(True)
            self.set_tool_mode("pen")

    def on_drawing_changed(self):
        """Marque l'image comme modifiée."""
        self.is_modified = True

    def on_mouse_moved(self, point):
        """Met à jour les coordonnées affichées dans la barre d'état."""
        self.cursor_pos = point
        self.update_status_message()

    def update_status_message(self):
        """Affiche les informations d'outil et de position dans la barre d'état."""
        tool_name = "Gomme" if self.canvas.mode == "eraser" else "Pinceau"
        width = self.canvas.pen_width
        x, y = self.cursor_pos.x(), self.cursor_pos.y()
        self.statusBar().showMessage(
            f"Outil : {tool_name} | Épaisseur : {width}px | Position : ({x}, {y})"
        )

    def new_drawing(self):
        """Réinitialise le canevas après confirmation si modifié."""
        if self.is_modified:
            reply = QMessageBox.question(
                self,
                "Nouveau dessin",
                "Le dessin actuel n'est pas enregistré. Voulez-vous vraiment le réinitialiser ?",
                QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
                QMessageBox.StandardButton.No
            )
            if reply != QMessageBox.StandardButton.Yes:
                return

        self.canvas.clear_canvas()
        self.is_modified = False

    def save_image(self):
        """Exporte le dessin sous forme de fichier image (PNG, JPG)."""
        file_path, _ = QFileDialog.getSaveFileName(
            self,
            "Enregistrer le dessin",
            "mon_dessin.png",
            "Images PNG (*.png);;Images JPEG (*.jpg *.jpeg);;Tous les fichiers (*)"
        )
        if not file_path:
            return False

        if self.canvas.pixmap.save(file_path):
            self.is_modified = False
            QMessageBox.information(self, "Succès", "Image enregistrée avec succès !")
            return True
        else:
            QMessageBox.critical(self, "Erreur", "Impossible d'enregistrer l'image.")
            return False

    def closeEvent(self, event):
        """Demande confirmation avant fermeture si le dessin contient des modifications non enregistrées."""
        if self.is_modified:
            reply = QMessageBox.question(
                self,
                "Quitter",
                "Votre dessin contient des modifications non enregistrées.\nVoulez-vous vraiment quitter sans enregistrer ?",
                QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
                QMessageBox.StandardButton.No
            )
            if reply == QMessageBox.StandardButton.Yes:
                event.accept()
            else:
                event.ignore()
        else:
            event.accept()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
