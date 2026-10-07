import pytest
from compte_bancaire import CompteBancaire


def test_deposer_montant_valide():
    compte = CompteBancaire("Alice", 100.0)
    compte.deposer(50.0)  # Précondition vérifiée par `deal`
    assert compte.solde == 150.0  # Test du comportement logique


def test_retirer_montant_valide():
    compte = CompteBancaire("Bob", 200.0)
    compte.retirer(75.0)  # Précondition vérifiée par `deal`
    assert compte.solde == 125.0  # Test du comportement logique


def test_retirer_solde_insuffisant():
    compte = CompteBancaire("Charlie", 50.0)
    with pytest.raises(ValueError):  # Test de l'exception
        compte.retirer(60.0)  # Précondition échoue → `deal` lève AssertionError


def test_invariant_solde_negatif():
    compte = CompteBancaire("Dave", 100.0)
    with pytest.raises(AssertionError):  # Test de l'invariant
        compte._solde = -50.0  # `deal` lève AssertionError


def test_solde_propriete_lecture_seule():
    compte = CompteBancaire("Eve", 100.0)
    assert compte.solde == 100.0
    with pytest.raises(AttributeError):
        compte.solde = 200.0