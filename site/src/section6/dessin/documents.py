"""
Produits de la Méthode de Fabrique (Factory Method) :
Hiérarchie abstraite Document et implémentations concrètes (CanvasDoc, AsciiDoc),
ainsi que les composants graphiques PySide6 associés.
"""

from __future__ import annotations
from abc import ABC, abstractmethod
from typing import List

from PySide6.QtCore import Qt
from PySide6.QtGui import QPainter, QFont
from PySide6.QtWidgets import QWidget, QPlainTextEdit

try:
    from .formes import Forme, FormeCanvas, FormeAscii
except (ImportError, ValueError):
    from formes import Forme, FormeCanvas, FormeAscii


# ==============================================================================
# Classe de base abstraite : Document
# ==============================================================================

class Document(ABC):
    """Classe abstraite représentant un document."""

    def __init__(self, titre: str):
        self.titre = titre
        self.formes: List[Forme] = []

    def ajouter_forme(self, forme: Forme) -> None:
        """Ajoute une forme au document et actualise son affichage."""
        self.formes.append(forme)
        self.actualiser()

    def effacer(self) -> None:
        """Efface toutes les formes du document."""
        self.formes.clear()
        self.actualiser()

    @abstractmethod
    def obtenir_widget(self) -> QWidget:
        """Retourne le composant graphique PySide6 affichant le document."""
        pass

    @abstractmethod
    def actualiser(self) -> None:
        """Actualise le rendu du document."""
        pass


# ==============================================================================
# Document Graphique : CanvasDoc & WidgetCanevas
# ==============================================================================

class WidgetCanevas(QWidget):
    """Widget personnalisé PySide6 pour peindre les formes Canvas."""

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setMinimumSize(450, 280)
        self.setStyleSheet("background-color: white; border: 2px solid #333333;")
        self.formes: List[FormeCanvas] = []

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)

        # Fond blanc
        painter.fillRect(self.rect(), Qt.GlobalColor.white)

        # Tracé de toutes les formes
        for forme in self.formes:
            forme.dessiner(painter)


class CanvasDoc(Document):
    """Document graphique (Canevas avec rendu vectoriel QPainter)."""

    def __init__(self, titre: str = "Document Graphique"):
        super().__init__(titre)
        self._widget = WidgetCanevas()

    def obtenir_widget(self) -> QWidget:
        return self._widget

    def actualiser(self) -> None:
        self._widget.formes = [f for f in self.formes if isinstance(f, FormeCanvas)]
        self._widget.update()


# ==============================================================================
# Document Textuel : AsciiDoc
# ==============================================================================

class AsciiDoc(Document):
    """Document texte ASCII (Rendu matriciel de caractères dans un champ texte)."""

    LARGEUR = 52
    HAUTEUR = 18

    def __init__(self, titre: str = "Document ASCII Art"):
        super().__init__(titre)
        self._widget = QPlainTextEdit()
        self._widget.setReadOnly(True)
        self._widget.setStyleSheet("background-color: #1E1E1E; color: #00FF66; border: 2px solid #333333;")

        font = QFont("Monospace", 10)
        font.setStyleHint(QFont.StyleHint.Monospace)
        self._widget.setFont(font)

        self.actualiser()

    def obtenir_widget(self) -> QWidget:
        return self._widget

    def actualiser(self) -> None:
        # Initialise une grille vide avec des espaces
        grille = [[" " for _ in range(self.LARGEUR)] for _ in range(self.HAUTEUR)]

        # Dessine le cadre du document ASCII
        for c in range(self.LARGEUR):
            grille[0][c] = "="
            grille[self.HAUTEUR - 1][c] = "="
        for r in range(self.HAUTEUR):
            grille[r][0] = "#"
            grille[r][self.LARGEUR - 1] = "#"

        # Rendu de toutes les formes ASCII
        for forme in self.formes:
            if isinstance(forme, FormeAscii):
                forme.rendre_ascii(grille)

        # Conversion de la grille 2D en texte multi-lignes
        lignes = ["".join(ligne) for ligne in grille]
        texte = "\n".join(lignes)
        self._widget.setPlainText(texte)
