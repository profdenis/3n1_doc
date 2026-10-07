import pytest
from fonctions import additionner, diviser, verifier_age


@pytest.mark.parametrize("a, b, expected", [
    (2, 3, 5),
    (0, 0, 0),
    (-1, 1, 0)
])
def test_additionner_parametre(a, b, expected):
    assert additionner(a, b) == expected


def test_additionner_avec_message():
    result = additionner(2, 3)
    assert result == 5, f"Attendu 5, obtenu {result}"  # Message d'erreur clair


def test_division_par_zero():
    # On s'attend à ce que ce bloc lève une ValueError
    with pytest.raises(ValueError):
        diviser(10, 0)


def test_division_message_specifique():
    # On vérifie le type ET le contenu du message
    with pytest.raises(ValueError, match="Le diviseur ne peut pas être nul"):
        diviser(10, 0)


@pytest.mark.parametrize("age_erreur, exception_attendue, message_attendu", [
    (-1, ValueError, "L'âge ne peut pas être négatif."),  # Cas 1
    (151, ValueError, "L'âge est trop élevé."),  # Cas 2
    (-50, ValueError, r"ne peut pas être négatif"),  # Cas 3 (vérifie que regex fonctionne aussi)
])
def test_verifier_age_exceptions(age_erreur, exception_attendue, message_attendu):
    """
    Teste que la fonction lève les bonnes exceptions
    pour les mauvaises valeurs d'âge.
    """
    with pytest.raises(exception_attendue, match=message_attendu):
        verifier_age(age_erreur)


def test_verifier_age_valide():
    """Test que la fonction fonctionne normalement pour des valeurs valides."""
    assert verifier_age(25) is True
