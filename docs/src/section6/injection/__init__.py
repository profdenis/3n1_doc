"""
Module de démonstration pour le patron Injection de Dépendances.
"""

from .personne import Personne
from .lecteurs import (
    LecteurPersonnes,
    LecteurCSV,
    LecteurJSON,
    LecteurSQLite,
    LecteurMemoire,
)
from .service import GestionnairePersonnes

__all__ = [
    "Personne",
    "LecteurPersonnes",
    "LecteurCSV",
    "LecteurJSON",
    "LecteurSQLite",
    "LecteurMemoire",
    "GestionnairePersonnes",
]
