"""
Patron Méthode de Fabrique (Factory Method) :
Hiérarchie créatrice des éditeurs (EditeurDocument, EditeurCanvas, EditeurAscii).
"""

from __future__ import annotations
from abc import ABC, abstractmethod

try:
    from .documents import Document, CanvasDoc, AsciiDoc
    from .fabriques import FabriqueFormes, FabriqueFormesCanvas, FabriqueFormesAscii
except (ImportError, ValueError):
    from documents import Document, CanvasDoc, AsciiDoc
    from fabriques import FabriqueFormes, FabriqueFormesCanvas, FabriqueFormesAscii


class EditeurDocument(ABC):
    """
    Classe créatrice abstraite (Creator dans le patron Factory Method).
    Elle gère le document courant et définit la méthode de fabrique 'creer_document'.
    Elle contient également une référence vers la Fabrique Abstraite correspondante.
    """

    def __init__(self, nom_format: str, fabrique_formes: FabriqueFormes):
        self.nom_format = nom_format
        self.fabrique_formes = fabrique_formes
        self.document_courant: Document | None = None

    @abstractmethod
    def creer_document(self) -> Document:
        """MÉTHODE DE FABRIQUE (Factory Method) abstraite."""
        pass

    def nouveau_document(self) -> Document:
        """
        Logique commune de création et d'initialisation d'un document.
        Délègue l'instanciation exacte à la méthode de fabrique polymorphique.
        """
        self.document_courant = self.creer_document()
        return self.document_courant


class EditeurCanvas(EditeurDocument):
    """Créateur concret pour l'environnement graphique Canvas."""

    def __init__(self):
        super().__init__("Canvas Graphique", FabriqueFormesCanvas())

    def creer_document(self) -> CanvasDoc:
        """Implémentation de la méthode de fabrique retournant un CanvasDoc."""
        return CanvasDoc("Nouveau Canevas")


class EditeurAscii(EditeurDocument):
    """Créateur concret pour l'environnement texte ASCII Art."""

    def __init__(self):
        super().__init__("ASCII Art", FabriqueFormesAscii())

    def creer_document(self) -> AsciiDoc:
        """Implémentation de la méthode de fabrique retournant un AsciiDoc."""
        return AsciiDoc("Nouveau Document ASCII")
