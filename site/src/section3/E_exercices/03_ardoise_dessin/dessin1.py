import sys
from PySide6.QtWidgets import QApplication, QMainWindow, QWidget
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
            self.update()  # Demande le rafraîchissement du widget

    def mouseReleaseEvent(self, event):
        """Réinitialise le point de tracé lorsque le clic est relâché."""
        if event.button() == Qt.MouseButton.LeftButton:
            self.last_point = None


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Ardoise de dessin")

        self.canvas = CanvasWidget()
        self.setCentralWidget(self.canvas)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
