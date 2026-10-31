"""
Module de démonstration des Patrons de Conception de Création :
- Méthode de Fabrique (Factory Method)
- Fabrique Abstraite (Abstract Factory)
"""

try:
    from .formes import (
        Forme,
        FormeCanvas,
        RectangleCanvas,
        CercleCanvas,
        LigneCanvas,
        FormeAscii,
        RectangleAscii,
        CercleAscii,
        LigneAscii,
    )
    from .fabriques import (
        FabriqueFormes,
        FabriqueFormesCanvas,
        FabriqueFormesAscii,
    )
    from .documents import (
        Document,
        WidgetCanevas,
        CanvasDoc,
        AsciiDoc,
    )
    from .editeurs import (
        EditeurDocument,
        EditeurCanvas,
        EditeurAscii,
    )
    from .app import MainWindow
except (ImportError, ValueError):
    from formes import (
        Forme,
        FormeCanvas,
        RectangleCanvas,
        CercleCanvas,
        LigneCanvas,
        FormeAscii,
        RectangleAscii,
        CercleAscii,
        LigneAscii,
    )
    from fabriques import (
        FabriqueFormes,
        FabriqueFormesCanvas,
        FabriqueFormesAscii,
    )
    from documents import (
        Document,
        WidgetCanevas,
        CanvasDoc,
        AsciiDoc,
    )
    from editeurs import (
        EditeurDocument,
        EditeurCanvas,
        EditeurAscii,
    )
    from app import MainWindow

__all__ = [
    "Forme",
    "FormeCanvas",
    "RectangleCanvas",
    "CercleCanvas",
    "LigneCanvas",
    "FormeAscii",
    "RectangleAscii",
    "CercleAscii",
    "LigneAscii",
    "FabriqueFormes",
    "FabriqueFormesCanvas",
    "FabriqueFormesAscii",
    "Document",
    "WidgetCanevas",
    "CanvasDoc",
    "AsciiDoc",
    "EditeurDocument",
    "EditeurCanvas",
    "EditeurAscii",
    "MainWindow",
]
