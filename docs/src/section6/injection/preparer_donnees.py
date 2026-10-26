import csv
import json
import sqlite3
from pathlib import Path


def preparer_fichiers_donnees(dossier: Path) -> None:
    """Génère les 3 sources de données (CSV, JSON, SQLite) avec un contenu de test."""
    dossier.mkdir(parents=True, exist_ok=True)

    donnees = [
        {"id": 1, "nom": "Tremblay", "prenom": "Alice", "age": 28, "courriel": "alice.tremblay@exemple.qc.ca"},
        {"id": 2, "nom": "Gagnon", "prenom": "Bob", "age": 34, "courriel": "bob.gagnon@exemple.qc.ca"},
        {"id": 3, "nom": "Roy", "prenom": "Charlie", "age": 22, "courriel": "charlie.roy@exemple.qc.ca"},
        {"id": 4, "nom": "Bouchard", "prenom": "Diane", "age": 45, "courriel": "diane.bouchard@exemple.qc.ca"},
    ]

    # 1. Fichier CSV
    chemin_csv = dossier / "personnes.csv"
    with open(chemin_csv, mode="w", encoding="utf-8", newline="") as f:
        champs = ["id", "nom", "prenom", "age", "courriel"]
        writer = csv.DictWriter(f, fieldnames=champs)
        writer.writeheader()
        writer.writerows(donnees)

    # 2. Fichier JSON
    chemin_json = dossier / "personnes.json"
    with open(chemin_json, mode="w", encoding="utf-8") as f:
        json.dump(donnees, f, indent=2, ensure_ascii=False)

    # 3. Base de données SQLite
    chemin_db = dossier / "personnes.db"
    if chemin_db.exists():
        chemin_db.unlink()

    with sqlite3.connect(chemin_db) as conn:
        cursor = conn.cursor()
        cursor.execute(
            """
            CREATE TABLE personnes (
                id INTEGER PRIMARY KEY,
                nom TEXT NOT NULL,
                prenom TEXT NOT NULL,
                age INTEGER NOT NULL,
                courriel TEXT NOT NULL
            )
            """
        )
        for item in donnees:
            cursor.execute(
                "INSERT INTO personnes (id, nom, prenom, age, courriel) VALUES (?, ?, ?, ?, ?)",
                (item["id"], item["nom"], item["prenom"], item["age"], item["courriel"]),
            )
        conn.commit()


if __name__ == "__main__":
    dossier_actuel = Path(__file__).parent
    preparer_fichiers_donnees(dossier_actuel)
    print("Fichiers de données (CSV, JSON, SQLite) générés avec succès.")
