from pathlib import Path

try:
    from .personne import Personne
    from .lecteurs import (
        LecteurCSV,
        LecteurJSON,
        LecteurSQLite,
        LecteurMemoire,
    )
    from .service import GestionnairePersonnes
    from .preparer_donnees import preparer_fichiers_donnees
except (ImportError, ValueError):
    from personne import Personne
    from lecteurs import (
        LecteurCSV,
        LecteurJSON,
        LecteurSQLite,
        LecteurMemoire,
    )
    from service import GestionnairePersonnes
    from preparer_donnees import preparer_fichiers_donnees


def main() -> None:
    dossier_courant = Path(__file__).parent

    # Génère les fichiers d'exemple si besoin
    preparer_fichiers_donnees(dossier_courant)

    chemin_csv = dossier_courant / "personnes.csv"
    chemin_json = dossier_courant / "personnes.json"
    chemin_db = dossier_courant / "personnes.db"

    print("=================================================================")
    print("DÉMONSTRATION DU PATRON INJECTION DE DÉPENDANCES (CONSOLE)")
    print("=================================================================\n")

    # -------------------------------------------------------------------------
    # 1. Utilisation avec la source CSV
    # -------------------------------------------------------------------------
    source_csv = LecteurCSV(chemin_csv)
    # INJECTION : on passe la source concrète au constructeur du gestionnaire
    gestionnaire_csv = GestionnairePersonnes(source=source_csv)
    gestionnaire_csv.afficher_rapport()

    # -------------------------------------------------------------------------
    # 2. Utilisation avec la source JSON
    # -------------------------------------------------------------------------
    source_json = LecteurJSON(chemin_json)
    # INJECTION : même classe GestionnairePersonnes, dépendance différente
    gestionnaire_json = GestionnairePersonnes(source=source_json)
    gestionnaire_json.afficher_rapport()

    # -------------------------------------------------------------------------
    # 3. Utilisation avec la source SQLite
    # -------------------------------------------------------------------------
    source_sqlite = LecteurSQLite(chemin_db)
    # INJECTION : idem avec la base de données relationnelle
    gestionnaire_sqlite = GestionnairePersonnes(source=source_sqlite)
    gestionnaire_sqlite.afficher_rapport()

    # -------------------------------------------------------------------------
    # 4. Utilisation avec un Mock / Source en Mémoire (idéal pour les tests)
    # -------------------------------------------------------------------------
    source_mock = LecteurMemoire([
        Personne(id=101, nom="Labrecque", prenom="Eve", age=30, courriel="eve@test.local"),
        Personne(id=102, nom="Fortin", prenom="Frank", age=50, courriel="frank@test.local"),
    ])
    gestionnaire_mock = GestionnairePersonnes(source=source_mock)
    gestionnaire_mock.afficher_rapport()

    # -------------------------------------------------------------------------
    # 5. Démonstration de logique métier indépendante de la source
    # -------------------------------------------------------------------------
    print("=== Démonstration de filtrage métier (Source SQLite) ===")
    adultes = gestionnaire_sqlite.filtrer_par_age_min(30)
    print("Personnes de 30 ans et plus :")
    for pers in adultes:
        print(f"  * {pers.prenom} {pers.nom} ({pers.age} ans)")

    print("\nRecherche par courriel ('alice.tremblay@exemple.qc.ca') :")
    trouvee = gestionnaire_sqlite.trouver_par_courriel("alice.tremblay@exemple.qc.ca")
    print(f"  Résultat : {trouvee}")


if __name__ == "__main__":
    main()
