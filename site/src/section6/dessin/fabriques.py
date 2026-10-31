"""
Patron Fabrique Abstraite (Abstract Factory) :
Définition de l'interface abstraite et des fabriques concrètes de formes
(FabriqueFormesCanvas et FabriqueFormesAscii).
"""

from __future__ import annotations
import random
from abc import ABC, abstractmethod

from PySide6.QtGui import QColor

try:
    from .formes import (
        Forme,
        RectangleCanvas,
        CercleCanvas,
        LigneCanvas,
        RectangleAscii,
        CercleAscii,
        LigneAscii,
    )
except (ImportError, ValueError):
    from formes import (
        Forme,
        RectangleCanvas,
        CercleCanvas,
        LigneCanvas,
        RectangleAscii,
        CercleAscii,
        LigneAscii,
    )


class FabriqueFormes(ABC):
    """Interface de la Fabrique Abstraite déclarant la création des familles de formes."""

    @abstractmethod
    def creer_rectangle(self) -> Forme:
        """Crée un rectangle adapté au document courant."""
        pass

    @abstractmethod
    def creer_cercle(self) -> Forme:
        """Crée un cercle adapté au document courant."""
        pass

    @abstractmethod
    def creer_ligne(self) -> Forme:
        """Crée une ligne adaptée au document courant."""
        pass


class FabriqueFormesCanvas(FabriqueFormes):
    """Fabrique concrète créant des formes géométriques pour Canvas."""

    def creer_rectangle(self) -> RectangleCanvas:
        x = random.randint(30, 260)
        y = random.randint(30, 160)
        largeur = random.randint(80, 150)
        hauteur = random.randint(50, 100)
        couleur = random.choice([QColor("#4A90E2"), QColor("#50E3C2"), QColor("#B8E986"), QColor("#BD10E0")])
        return RectangleCanvas(x, y, largeur, hauteur, couleur)

    def creer_cercle(self) -> CercleCanvas:
        cx = random.randint(80, 320)
        cy = random.randint(80, 200)
        rayon = random.randint(30, 60)
        couleur = random.choice([QColor("#F5A623"), QColor("#E94E77"), QColor("#F8E71C")])
        return CercleCanvas(cx, cy, rayon, couleur)

    def creer_ligne(self) -> LigneCanvas:
        x1 = random.randint(20, 200)
        y1 = random.randint(20, 250)
        x2 = random.randint(220, 420)
        y2 = random.randint(20, 250)
        couleur = random.choice([QColor("#D0021B"), QColor("#417505"), QColor("#9013FE")])
        return LigneCanvas(x1, y1, x2, y2, couleur)


class FabriqueFormesAscii(FabriqueFormes):
    """Fabrique concrète créant des formes textuelles pour AsciiDoc."""

    def creer_rectangle(self) -> RectangleAscii:
        x = random.randint(2, 25)
        y = random.randint(2, 10)
        largeur = random.randint(12, 22)
        hauteur = random.randint(5, 8)
        return RectangleAscii(x, y, largeur, hauteur)

    def creer_cercle(self) -> CercleAscii:
        cx = random.randint(15, 35)
        cy = random.randint(6, 12)
        rayon = random.randint(3, 5)
        return CercleAscii(cx, cy, rayon)

    def creer_ligne(self) -> LigneAscii:
        x1 = random.randint(2, 20)
        y1 = random.randint(2, 16)
        x2 = random.randint(25, 48)
        y2 = random.randint(2, 16)
        return LigneAscii(x1, y1, x2, y2)
