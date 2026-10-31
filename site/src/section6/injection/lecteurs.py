import csv
import json
import sqlite3
from abc import ABC, abstractmethod
from pathlib import Path

try:
    from .personne import Personne
except (ImportError, ValueError):
    from personne import Personne


class LecteurPersonnes(ABC):
    """
    Interface / Contrat abstrait définissant la source de données.
    Le service métier dépendra uniquement de cette abstraction.
    """

    @abstractmethod
    def charger_personnes(self) -> list[Personne]:
        """Charge et retourne la liste des personnes depuis la source."""
        pass


class LecteurCSV(LecteurPersonnes):
    """Implémentation concrète pour la lecture depuis un fichier CSV."""

    def __init__(self, chemin_fichier: str | Path):
        self.chemin_fichier = Path(chemin_fichier)

    def charger_personnes(self) -> list[Personne]:
        if not self.chemin_fichier.exists():
            return []

        personnes: list[Personne] = []
        with open(self.chemin_fichier, mode="r", encoding="utf-8") as f:
            lecteur = csv.DictReader(f)
            for ligne in lecteur:
                personnes.append(
                    Personne(
                        id=int(ligne["id"]),
                        nom=ligne["nom"],
                        prenom=ligne["prenom"],
                        age=int(ligne["age"]),
                        courriel=ligne["courriel"],
                    )
                )
        return personnes


class LecteurJSON(LecteurPersonnes):
    """Implémentation concrète pour la lecture depuis un fichier JSON."""

    def __init__(self, chemin_fichier: str | Path):
        self.chemin_fichier = Path(chemin_fichier)

    def charger_personnes(self) -> list[Personne]:
        if not self.chemin_fichier.exists():
            return []

        with open(self.chemin_fichier, mode="r", encoding="utf-8") as f:
            donnees = json.load(f)

        return [
            Personne(
                id=int(item["id"]),
                nom=item["nom"],
                prenom=item["prenom"],
                age=int(item["age"]),
                courriel=item["courriel"],
            )
            for item in donnees
        ]


class LecteurSQLite(LecteurPersonnes):
    """Implémentation concrète pour la lecture depuis une base de données SQLite."""

    def __init__(self, chemin_bd: str | Path):
        self.chemin_bd = Path(chemin_bd)

    def charger_personnes(self) -> list[Personne]:
        if not self.chemin_bd.exists():
            return []

        personnes: list[Personne] = []
        with sqlite3.connect(self.chemin_bd) as conn:
            cursor = conn.cursor()
            cursor.execute(
                "SELECT id, nom, prenom, age, courriel FROM personnes ORDER BY id"
            )
            lignes = cursor.fetchall()
            for row in lignes:
                personnes.append(
                    Personne(
                        id=row[0],
                        nom=row[1],
                        prenom=row[2],
                        age=row[3],
                        courriel=row[4],
                    )
                )
        return personnes


class LecteurMemoire(LecteurPersonnes):
    """
    Implémentation en mémoire (idéale pour les tests unitaires / bouchons).
    """

    def __init__(self, personnes: list[Personne] | None = None):
        self._personnes = list(personnes) if personnes is not None else []

    def ajouter_personne(self, personne: Personne) -> None:
        self._personnes.append(personne)

    def charger_personnes(self) -> list[Personne]:
        return list(self._personnes)
