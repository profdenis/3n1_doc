import pytest
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


@pytest.fixture
def donnees_test(tmp_path: Path):
    preparer_fichiers_donnees(tmp_path)
    return tmp_path


def test_service_avec_mock_memoire():
    """Vérifie que la logique métier fonctionne en isolation complète sans toucher au disque/BD."""
    mock_source = LecteurMemoire([
        Personne(1, "TestNom1", "TestPrenom1", 20, "p1@test.com"),
        Personne(2, "TestNom2", "TestPrenom2", 40, "p2@test.com"),
        Personne(3, "TestNom3", "TestPrenom3", 60, "p3@test.com"),
    ])
    service = GestionnairePersonnes(source=mock_source)

    assert len(service.lister_personnes()) == 3
    assert service.calculer_age_moyen() == 40.0
    assert len(service.filtrer_par_age_min(35)) == 2
    assert service.trouver_par_courriel("p2@test.com") is not None
    assert service.trouver_par_courriel("inexistant@test.com") is None


def test_service_avec_csv(donnees_test: Path):
    source = LecteurCSV(donnees_test / "personnes.csv")
    service = GestionnairePersonnes(source=source)
    personnes = service.lister_personnes()

    assert len(personnes) == 4
    assert personnes[0].nom == "Tremblay"
    assert service.calculer_age_moyen() > 0


def test_service_avec_json(donnees_test: Path):
    source = LecteurJSON(donnees_test / "personnes.json")
    service = GestionnairePersonnes(source=source)
    personnes = service.lister_personnes()

    assert len(personnes) == 4
    assert personnes[1].prenom == "Bob"


def test_service_avec_sqlite(donnees_test: Path):
    source = LecteurSQLite(donnees_test / "personnes.db")
    service = GestionnairePersonnes(source=source)
    personnes = service.lister_personnes()

    assert len(personnes) == 4
    assert service.trouver_par_courriel("charlie.roy@exemple.qc.ca") is not None
