import sys
from PySide6.QtWidgets import (QApplication, QMainWindow, QWidget,
                               QVBoxLayout, QHBoxLayout, QLabel,
                               QSlider, QSpinBox)
from PySide6.QtCore import Qt, QPoint
from PySide6.QtGui import QPainter, QPen, QColor, QPixmap


class CanvasWidget(QWidget):
    """Widget de dessin personnalisé gérant les événements de la souris."""
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setFixedSize(600, 400)

        # Création d'un pixmap blanc sur lequel dessiner
        self.pixmap = QPixmap(self.size())
        self.pixmap.fill(Qt.GlobalColor.white)

        # Propriétés du tracé
        self.pen_color = QColor("black")
        self.pen_width = 3
        self.last_point = None

    def set_pen_width(self, width):
        """Modifie l'épaisseur du pinceau."""
        self.pen_width = width

    def paintEvent(self, event):
        """Dessine le pixmap sur la surface du widget."""
        painter = QPainter(self)
        painter.drawPixmap(0, 0, self.pixmap)

    def mousePressEvent(self, event):
        """Enregistre le point de départ lors du clic gauche."""
        if event.button() == Qt.MouseButton.LeftButton:
            self.last_point = event.position().toPoint()

    def mouseMoveEvent(self, event):
        """Trace une ligne continue tant que le bouton gauche est maintenu."""
        if (event.buttons() & Qt.MouseButton.LeftButton) and self.last_point is not None:
            painter = QPainter(self.pixmap)
            pen = QPen(
                self.pen_color,
                self.pen_width,
                Qt.PenStyle.SolidLine,
                Qt.PenCapStyle.RoundCap,
                Qt.PenJoinStyle.RoundJoin
            )
            painter.setPen(pen)

            current_point = event.position().toPoint()
            painter.drawLine(self.last_point, current_point)
            painter.end()

            self.last_point = current_point
            self.update()

    def mouseReleaseEvent(self, event):
        """Réinitialise le point de tracé lorsque le clic est relâché."""
        if event.button() == Qt.MouseButton.LeftButton:
            self.last_point = None


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Ardoise de dessin")

        # Widget central et layout principal
        central_widget = QWidget()
        layout = QVBoxLayout()

        # Canevas de dessin
        self.canvas = CanvasWidget()

        # Barre de contrôle de l'épaisseur
        control_layout = QHBoxLayout()
        control_layout.addWidget(QLabel("Épaisseur :"))

        self.width_slider = QSlider(Qt.Orientation.Horizontal)
        self.width_slider.setRange(1, 30)
        self.width_slider.setValue(3)

        self.width_spinbox = QSpinBox()
        self.width_spinbox.setRange(1, 30)
        self.width_spinbox.setValue(3)

        # Synchronisation entre le Slider et le SpinBox
        self.width_slider.valueChanged.connect(self.width_spinbox.setValue)
        self.width_spinbox.valueChanged.connect(self.width_slider.setValue)

        # Connexion avec le canevas
        self.width_slider.valueChanged.connect(self.canvas.set_pen_width)

        control_layout.addWidget(self.width_slider)
        control_layout.addWidget(self.width_spinbox)
        control_layout.addStretch()

        layout.addLayout(control_layout)
        layout.addWidget(self.canvas)

        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
