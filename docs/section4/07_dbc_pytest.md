# **Guide : Combinaison de pytest et Design by Contract (DbC) avec `deal`**

*Pour les étudiants en programmation orientée objet*

---

## **1. Introduction**

Le **Design by Contract (DbC)** et les **tests unitaires** sont deux approches complémentaires pour assurer la qualité
du code :

- **DbC (`deal`)** : Vérifie les préconditions, postconditions et invariants *pendant l'exécution*.
- **Tests unitaires (`pytest`)** : Vérifient le comportement attendu *de manière indépendante*.

### **Quand utiliser quoi ?**

| Approche            | Utilisation                                                                      | Exemple                                            |
|---------------------|----------------------------------------------------------------------------------|----------------------------------------------------|
| **DbC**             | Vérifications *runtime* (ex: solde ≥ 0 dans un compte bancaire).                 | `@inv(lambda self: self.solde >= 0)`               |
| **Tests unitaires** | Vérifications *logiques* (ex: "Un retrait de 50€ doit réduire le solde de 50€"). | `assert compte.solde == 150 après un dépôt de 50€` |

---

## **2. Ce que les tests doivent vérifier**

### **Ce qui est déjà couvert par DbC (à ne pas retester)**

❌ **Ne testez pas** :

- Les préconditions (`@pre`) → `deal` s'en charge.
- Les invariants (`@inv`) → `deal` s'en charge.
- Les postconditions (`@post`) → Si elles échouent, c'est une erreur de programmation.

### **Ce que les tests doivent vérifier**

✅ **Testez** :

1. **Le comportement logique** (ex: "Un dépôt augmente le solde").
2. **Les cas limites** (ex: "Un retrait avec un solde insuffisant lève une exception").
3. **L'intégration entre méthodes** (ex: "Après un dépôt, un retrait fonctionne correctement").

---

## **3. Exemple complet : CompteBancaire avec DbC + pytest**

### **Code source (avec `deal`)**

```python
from deal import pre, post, inv


@inv(lambda self: self._solde >= 0)  # Invariant : solde toujours ≥ 0
class CompteBancaire:
    def __init__(self, titulaire: str, solde_initial: float = 0.0):
        self.titulaire = titulaire
        self._solde = solde_initial

    @pre(lambda montant: montant > 0)  # Précondition : montant positif
    def deposer(self, montant: float):
        """Dépose un montant sur le compte."""
        self._solde += montant

    @pre(lambda montant: montant > 0 and montant <= self._solde)  # Précondition
    def retirer(self, montant: float):
        """Retire un montant du compte. Lève ValueError si solde insuffisant."""
        if montant > self._solde:
            raise ValueError("Solde insuffisant")
        self._solde -= montant

    @post(lambda result: isinstance(result, (int, float)) and result >= 0)  # Postcondition
    def get_solde(self) -> float:
        """Retourne le solde actuel."""
        return self._solde
```

### **Tests pytest associés**

```python
import pytest
from votre_module import CompteBancaire


def test_deposer_montant_valide():
    compte = CompteBancaire("Alice", 100.0)
    compte.deposer(50.0)  # Précondition vérifiée par `deal`
    assert compte.get_solde() == 150.0  # Test du comportement logique


def test_retirer_montant_valide():
    compte = CompteBancaire("Bob", 200.0)
    compte.retirer(75.0)  # Précondition vérifiée par `deal`
    assert compte.get_solde() == 125.0  # Test du comportement logique


def test_retirer_solde_insuffisant():
    compte = CompteBancaire("Charlie", 50.0)
    with pytest.raises(ValueError):  # Test de l'exception
        compte.retirer(60.0)  # Précondition échoue → `deal` lève AssertionError


def test_invariant_solde_negatif():
    compte = CompteBancaire("Dave", 100.0)
    with pytest.raises(AssertionError):  # Test de l'invariant
        compte._solde = -50.0  # `deal` lève AssertionError
```

---

## **4. Stratégie de test avec DbC**

### **Étape 1 : Tester les cas valides (comportement logique)**

```python
def test_deposer_et_retirer():
    compte = CompteBancaire("Alice", 100.0)
    compte.deposer(50.0)  # OK (précondition vérifiée par `deal`)
    compte.retirer(30.0)  # OK (précondition vérifiée par `deal`)
    assert compte.get_solde() == 120.0  # Test du résultat final
```

### **Étape 2 : Tester les cas invalides (exceptions)**

```python
def test_deposer_montant_negatif():
    compte = CompteBancaire("Bob", 100.0)
    with pytest.raises(AssertionError):  # `deal` lève AssertionError
        compte.deposer(-50.0)  # Précondition échoue


def test_retirer_solde_insuffisant():
    compte = CompteBancaire("Charlie", 50.0)
    with pytest.raises(ValueError):  # Exception levée par la méthode
        compte.retirer(60.0)  # Précondition échoue → `deal` lève AssertionError
```

### **Étape 3 : Tester les invariants (modifications directes)**

```python
def test_invariant_violé():
    compte = CompteBancaire("Dave", 100.0)
    with pytest.raises(AssertionError):  # `deal` lève AssertionError
        compte._solde = -50.0  # Accès direct à l'attribut (interdit par `@inv`)
```

---

## **5. Bonnes pratiques**

### **✅ Ce que les tests doivent faire**

1. **Vérifier le comportement attendu** (ex: "Un dépôt augmente le solde").
2. **Tester les exceptions** (ex: "Un retrait avec solde insuffisant lève une erreur").
3. **Valider l'intégration entre méthodes** (ex: "Après un dépôt, un retrait fonctionne").

### **❌ Ce que les tests ne doivent pas faire**

1. **Retester les préconditions/postconditions** → C'est le rôle de `deal`.
2. **Tester les invariants manuellement** → `deal` s'en charge.
3. **Répéter les vérifications de type** → Utilisez des annotations (`: float`) + `mypy`.

---

## **6. Exercice pour les étudiants**

### **Consigne**

Écrivez des tests pytest pour la classe `Rectangle` suivante (avec DbC) :

```python
from deal import pre, post, inv


@inv(lambda self: self.largeur > 0 and self.hauteur > 0)
class Rectangle:
    def __init__(self, largeur: float, hauteur: float):
        self.largeur = largeur
        self.hauteur = hauteur

    @pre(lambda valeur: valeur > 0)
    def set_largeur(self, valeur: float):
        self.largeur = valeur

    @pre(lambda valeur: valeur > 0)
    def set_hauteur(self, valeur: float):
        self.hauteur = valeur

    @post(lambda aire: aire > 0)
    def calculer_aire(self) -> float:
        return self.largeur * self.hauteur
```

### **Tests attendus**

1. Test de la création d'un rectangle valide.
2. Test de l'échec d'une largeur/hauteur négative (précondition).
3. Test du calcul de l'aire.
4. Test de l'invariant (modification directe des attributs).

---

## **7. Ressources supplémentaires**

- [Documentation pytest](https://docs.pytest.org/)
- [Documentation deal](https://github.com/python-deal/deal)

---

### **Résumé final**

| Approche                       | Rôle                                                   | Exemple                      |
|--------------------------------|--------------------------------------------------------|------------------------------|
| **DbC (`deal`)**               | Vérifie les contrats (pré/postconditions, invariants). | `@pre(lambda x: x > 0)`      |
| **Tests unitaires (`pytest`)** | Vérifie le comportement logique et les cas d'usage.    | `assert compte.solde == 150` |

**Stratégie :**

- Laissez `deal` gérer les vérifications de contrat.
- Utilisez `pytest` pour tester la logique métier et les interactions entre méthodes.
