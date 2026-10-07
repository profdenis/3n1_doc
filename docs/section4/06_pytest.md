# **Tests unitaires avec `pytest`**

## **1. Pourquoi utiliser pytest ?**

- **Framework de test unitaire** très populaire en Python.
- **Syntaxe simple et expressive**.
- **Intégration facile** avec des outils comme `deal` pour le Design by Contract.

---

## **2. Installation et configuration**

### **Installation**

```bash
uv add pytest
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

    def retirer(self, montant):
        self.solde -= montant


@pytest.fixture
def compte_bancaire():
    return CompteBancaire(100)  # Solde initial pour tous les tests


def test_deposer(compte_bancaire):  # `compte_bancaire` est fourni par la fixture
    compte_bancaire.deposer(50)
    assert compte_bancaire.solde == 150


def test_retirer(compte_bancaire):
    compte_bancaire.retirer(30)
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

## **7. Tester les exceptions**

Pour tester qu'une fonction lève une exception spécifique avec `pytest`, on utilise le gestionnaire de contexte
**`pytest.raises`**.

Voici comment procéder, du cas le plus simple au cas le plus professionnel (utilisant le paramétrage).

### 1. La syntaxe de base : `pytest.raises`

Si vous voulez simplement vérifier que l'exception de type `ValueError` est levée, on utilise un bloc `with`. Si la
fonction ne lève pas l'exception (ou lève une autre exception que celle attendue), le test échouera.

```python
import pytest


# La fonction à tester
def diviser(a, b):
    if b == 0:
        raise ValueError("Le diviseur ne peut pas être nul.")
    if a < 0:
        raise ValueError("Le dividende doit être positif.")
    return a / b


# Le test
def test_division_par_zero():
    # On s'attend à ce que ce bloc lève une ValueError
    with pytest.raises(ValueError):
        diviser(10, 0)
```

---

### 2. Vérifier le message d'erreur (Recommandé)

Il est souvent risqué de vérifier seulement le type d'exception (car une fonction peut lever un `ValueError` pour une
raison totalement différente de celle que vous testez). Il est préférable de vérifier que le **message d'erreur**
contient bien le texte attendu en utilisant l'argument `match`.

L'argument `match` accepte une **expression régulière (regex)**.

```python
def test_division_message_specifique():
    # On vérifie le type ET le contenu du message
    with pytest.raises(ValueError, match="Le diviseur ne peut pas être nul"):
        diviser(10, 0)
```

---

### 3. La méthode "Pro" : `@pytest.mark.parametrize`

Puisque vous avez mentionné vouloir tester "certains paramètres" (sous-entendu : plusieurs cas de figure), la manière la
plus propre et la plus efficace en programmation de tests est d'utiliser le **paramétrage**.

Cela permet de tester une liste de jeux de données (inputs / expected_exception / expected_message) avec une seule
fonction de test.

```python
import pytest


# --- Code source ---
def verifier_age(age):
    if age < 0:
        raise ValueError("L'âge ne peut pas être négatif.")
    if age > 150:
        raise ValueError("L'âge est trop élevé.")
    return True


# --- Tests ---

@pytest.mark.parametrize("age_erreur, exception_attendue, message_attendu", [
    (-1, ValueError, "L'âge ne peut pas être négatif."),  # Cas 1
    (151, ValueError, "L'âge est trop élevé."),  # Cas 2
    (-50, ValueError, "ne peut pas être négatif"),  # Cas 3 (vérifie que regex fonctionne aussi)
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
```

### À retenir :

1. **`with pytest.raises(ExceptionType):`** est la syntaxe standard pour capturer une exception.
2. **L'importance du `match`** : Toujours essayer de matcher le message d'erreur pour s'assurer que l'exception levée
   est bien celle que l'on attendait (et pas une autre erreur de type `ValueError` causée par un autre bug).
3. **`@pytest.mark.parametrize`** : C'est l'outil indispensable pour éviter la duplication de code lorsque vous avez
   plusieurs cas de tests d'erreurs (cas limites, valeurs négatives, valeurs trop grandes, etc.).
4. **Échec du test** :
    * Si aucune exception n'est levée $\rightarrow$ **Échec**.
    * Si une exception d'un *autre type* est levée $\rightarrow$ **Échec**.
    * Si l'exception est la bonne mais le message ne correspond pas au `match` $\rightarrow$ **Échec**.

---

## **8. Exercice**

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

## **9. Ressources supplémentaires**

- [Documentation officielle pytest](https://docs.pytest.org/)
- [Tutoriel pytest pour débutants](https://realpython.com/pytest-python-testing/)

---

## **Résumé final**

- `pytest` est simple et puissant pour les tests unitaires.
- Utilisez `assert` pour vérifier les résultats attendus.
- Les fixtures évitent la duplication de code.
- Les tests paramétrés permettent de tester plusieurs cas en un seul test.
