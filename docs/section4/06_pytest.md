# **Tests unitaires avec `pytest`**

## **1. Pourquoi utiliser pytest ?**

- **Framework de test unitaire** très populaire en Python.
- **Syntaxe simple et expressive**.
- **Intégration facile** avec des outils comme `deal` pour le Design by Contract.

---

## **2. Installation et configuration**

### **Installation**

```bash
pip install pytest
```

*(Aucune configuration supplémentaire nécessaire pour commencer !)*

---

## **3. Structure de base d'un test avec pytest**

### **Exemple : Test d'une fonction simple**

```python
# Dans un fichier `test_exemple.py`
def additionner(a, b):
    return a + b


# Test associé (nom du fichier doit commencer par `test_`)
def test_additionner():
    assert additionner(2, 3) == 5  # Si l'assertion échoue, pytest signale une erreur
```

### **Exécution des tests**

```bash
pytest test_exemple.py -v  # Le `-v` affiche les détails (verbose)
```

**Sortie attendue :**

```
test_exemple.py::test_additionner PASSED
```

---

## **4. Écrire des tests plus avancés**

### **Test avec plusieurs cas**

```python
def test_additionner_plusieurs_cas():
    assert additionner(0, 0) == 0  # Cas limite : zéro
    assert additionner(-1, 1) == 0  # Nombres négatifs
    assert additionner(1.5, 2.5) == 4  # Nombres flottants
```

### **Test avec messages personnalisés**

```python
def test_additionner_avec_message():
    result = additionner(2, 3)
    assert result == 5, f"Attendu 5, obtenu {result}"  # Message d'erreur clair
```

---

## **5. Fixtures (pour éviter la duplication de code)**

### **Exemple : Initialisation commune**

```python
import pytest

class CompteBancaire:
    def __init__(self, solde):
        self.solde = solde

    def deposer(self, montant):
        self.solde += montant

@pytest.fixture
def compte_bancaire():
    return CompteBancaire(100)  # Solde initial pour tous les tests


def test_deposer(compte_bancaire):  # `compte_bancaire` est fourni par la fixture
    compte_bancaire.deposer(50)
    assert compte_bancaire.solde == 150


def test_retirer(compte_bancaire):
    compte_bancaire.solde -= 30
    assert compte_bancaire.solde == 70
```

---

## **6. Bonnes pratiques pour pytest**

### **Nommage des tests**

- Utilise `test_nom_fonction` pour les tests unitaires.
- Utilise `test_nom_fonction_cas_particulier` pour les sous-cas.

### **Isolation des tests**

- Chaque test doit être indépendant (pas d'effets de bord entre tests).
- Utilise des fixtures pour partager des ressources.

### **Tests paramétrés (pour éviter la duplication)**

```python
import pytest


@pytest.mark.parametrize("a, b, expected", [
    (2, 3, 5),
    (0, 0, 0),
    (-1, 1, 0)
])
def test_additionner_parametre(a, b, expected):
    assert additionner(a, b) == expected
```

---

## **7. Exercice pour les étudiants**

### **Consigne**

Écrivez des tests pytest pour la classe `CompteBancaire` suivante :

```python
class CompteBancaire:
    def __init__(self, solde_initial):
        self.solde = solde_initial

    def deposer(self, montant):
        if montant > 0:
            self.solde += montant
        else:
            raise ValueError("Montant doit être positif")

    def retirer(self, montant):
        if montant <= self.solde and montant > 0:
            self.solde -= montant
        else:
            raise ValueError("Montant invalide")
```

### **Tests attendus**

1. Test du dépôt d'un montant valide.
2. Test de l'échec d'un dépôt avec un montant négatif.
3. Test du retrait d'un montant valide.
4. Test de l'échec d'un retrait avec un solde insuffisant.

---

## **8. Ressources supplémentaires**

- [Documentation officielle pytest](https://docs.pytest.org/)
- [Tutoriel pytest pour débutants](https://realpython.com/pytest-python-testing/)

---

### **Résumé final**

- `pytest` est simple et puissant pour les tests unitaires.
- Utilisez `assert` pour vérifier les résultats attendus.
- Les fixtures évitent la duplication de code.
- Les tests paramétrés permettent de tester plusieurs cas en un seul test.
