"""
Produits de la Fabrique Abstraite (Abstract Factory) :
Hiérarchies des formes géométriques pour Canvas et pour ASCII Art.
"""

from __future__ import annotations
import math
from abc import ABC, abstractmethod
from typing import List

from PySide6.QtCore import Qt, QPointF
from PySide6.QtGui import QPainter, QPen, QBrush, QColor


# ==============================================================================
# Interface racine pour toutes les formes
# ==============================================================================

class Forme(ABC):
    """Interface de base pour toutes les formes géométriques."""
    pass


# ==============================================================================
# Famille 1 : Formes graphiques pour Canvas (QPainter)
# ==============================================================================

class FormeCanvas(Forme, ABC):
    """Forme géométrique dessinable via QPainter."""

    @abstractmethod
    def dessiner(self, painter: QPainter) -> None:
        """Dessine la forme sur le QPainter fourni."""
        pass


class RectangleCanvas(FormeCanvas):
    def __init__(self, x: float, y: float, largeur: float, hauteur: float, couleur: QColor = QColor("steelblue")):
        self.x = x
        self.y = y
        self.largeur = largeur
        self.hauteur = hauteur
        self.couleur = couleur

    def dessiner(self, painter: QPainter) -> None:
        painter.setPen(QPen(Qt.GlobalColor.black, 2))
        painter.setBrush(QBrush(self.couleur))
        painter.drawRect(int(self.x), int(self.y), int(self.largeur), int(self.hauteur))


class CercleCanvas(FormeCanvas):
    def __init__(self, cx: float, cy: float, rayon: float, couleur: QColor = QColor("salmon")):
        self.cx = cx
        self.cy = cy
        self.rayon = rayon
        self.couleur = couleur

    def dessiner(self, painter: QPainter) -> None:
        painter.setPen(QPen(Qt.GlobalColor.black, 2))
        painter.setBrush(QBrush(self.couleur))
        painter.drawEllipse(QPointF(self.cx, self.cy), self.rayon, self.rayon)


class LigneCanvas(FormeCanvas):
    def __init__(self, x1: float, y1: float, x2: float, y2: float, couleur: QColor = QColor("darkgreen")):
        self.x1 = x1
        self.y1 = y1
        self.x2 = x2
        self.y2 = y2
        self.couleur = couleur

    def dessiner(self, painter: QPainter) -> None:
        painter.setPen(QPen(self.couleur, 3, Qt.PenStyle.SolidLine, Qt.PenCapStyle.RoundCap))
        painter.drawLine(int(self.x1), int(self.y1), int(self.x2), int(self.y2))


# ==============================================================================
# Famille 2 : Formes textuelles pour AsciiDoc (Caractères ASCII)
# ==============================================================================

class FormeAscii(Forme, ABC):
    """Forme géométrique rendue dans une grille de caractères ASCII."""

    @abstractmethod
    def rendre_ascii(self, grille: List[List[str]]) -> None:
        """Inscrit la forme dans la grille 2D de caractères."""
        pass


class RectangleAscii(FormeAscii):
    def __init__(self, x: int, y: int, largeur: int, hauteur: int):
        self.x = x
        self.y = y
        self.largeur = max(2, largeur)
        self.hauteur = max(2, hauteur)

    def rendre_ascii(self, grille: List[List[str]]) -> None:
        nb_lignes = len(grille)
        nb_cols = len(grille[0]) if nb_lignes > 0 else 0

        for r in range(self.y, min(nb_lignes, self.y + self.hauteur)):
            for c in range(self.x, min(nb_cols, self.x + self.largeur)):
                is_top = (r == self.y)
                is_bottom = (r == self.y + self.hauteur - 1)
                is_left = (c == self.x)
                is_right = (c == self.x + self.largeur - 1)

                if (is_top or is_bottom) and (is_left or is_right):
                    grille[r][c] = "+"
                elif is_top or is_bottom:
                    grille[r][c] = "-"
                elif is_left or is_right:
                    grille[r][c] = "|"


class CercleAscii(FormeAscii):
    def __init__(self, cx: int, cy: int, rayon: int):
        self.cx = cx
        self.cy = cy
        self.rayon = max(1, rayon)

    def rendre_ascii(self, grille: List[List[str]]) -> None:
        nb_lignes = len(grille)
        nb_cols = len(grille[0]) if nb_lignes > 0 else 0

        # Rendu approximatif d'un cercle dans une grille textuelle (compensation ratio 2:1)
        for angle_deg in range(0, 360, 10):
            rad = math.radians(angle_deg)
            c = int(round(self.cx + self.rayon * 2.0 * math.cos(rad)))
            r = int(round(self.cy + self.rayon * math.sin(rad)))
            if 0 <= r < nb_lignes and 0 <= c < nb_cols:
                grille[r][c] = "O"


class LigneAscii(FormeAscii):
    def __init__(self, x1: int, y1: int, x2: int, y2: int):
        self.x1 = x1
        self.y1 = y1
        self.x2 = x2
        self.y2 = y2

    def rendre_ascii(self, grille: List[List[str]]) -> None:
        nb_lignes = len(grille)
        nb_cols = len(grille[0]) if nb_lignes > 0 else 0

        steps = max(abs(self.x2 - self.x1), abs(self.y2 - self.y1), 1)
        for i in range(steps + 1):
            t = i / steps
            c = int(round(self.x1 + t * (self.x2 - self.x1)))
            r = int(round(self.y1 + t * (self.y2 - self.y1)))
            if 0 <= r < nb_lignes and 0 <= c < nb_cols:
                grille[r][c] = "*"
