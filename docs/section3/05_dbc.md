# **Le Design par Contrat (DbC)**

## **1. Qu’est-ce que le Design par Contrat (DbC) ?**

Le **Design par Contrat** est un paradigme de programmation qui formalise les interactions entre composants logiciels en
définissant :

- **Préconditions** : Conditions qui doivent être vraies *avant* l’exécution d’une méthode.
- **Postconditions** : Conditions qui doivent être vraies *après* l’exécution d’une méthode.
- **Invariants** : Propriétés qui doivent toujours être vraies pour un objet.

**Objectif** :

- Clarifier les attentes entre le code appelant et le code appelé.
- Détecter tôt les erreurs (pendant le développement).
- Améliorer la maintenabilité du code.

---

## **2. Exemples simples avec `assert`**

Python ne supporte pas nativement le DbC, mais on peut utiliser `assert` pour des vérifications basiques.

### **Exemple : Fonction de division**

```python
def diviser(a: float, b: float) -> float:
    assert b != 0, "Le dénominateur ne doit pas être nul"  # Précondition
    result = a / b
    assert isinstance(result, float), "Le résultat doit être un float"  # Postcondition
    return result


# Test
print(diviser(10, 2))  # OK → 5.0
print(diviser(10, 0))  # Lève AssertionError: "Le dénominateur ne doit pas être nul"
```

### **Exemple : Classe `CompteBancaire`**

```python
class CompteBancaire:
    def __init__(self, solde_initial: float):
        assert solde_initial >= 0, "Le solde initial doit être positif"  # Précondition
        self.solde = solde_initial

    def deposer(self, montant: float):
        assert montant > 0, "Le montant doit être positif"  # Précondition
        self.solde += montant


# Test
compte = CompteBancaire(100)
compte.deposer(50)  # OK
compte.deposer(-10)  # Lève AssertionError: "Le montant doit être positif"
```

**Limites de `assert`** :

- Désactivable avec `-O` en ligne de commande.
- Peu flexible pour les postconditions complexes.

---

## **3. Le module `deal` (version 4.24.6)**

`deal` est une bibliothèque Python qui implémente le DbC de manière propre et puissante.

### **Installation**

```bash
pip install deal
```

Note : la version actuelle de `deal`, utilisée dans ce document, est `4.24.6`.

### **Décorateurs disponibles**

| Décorateur | Description                                                                                       | Exemple                                                                               |
|------------|---------------------------------------------------------------------------------------------------|---------------------------------------------------------------------------------------|
| `@pre`     | Vérifie une condition *avant* l’exécution de la méthode.                                          | `@pre(lambda x: x > 0)`                                                               |
| `@post`    | Vérifie une condition *après* l’exécution de la méthode. Limitée aux résultats de la fonction.    | `@post(lambda result: result >= 0)`                                                   |
| `@ensure`  | Vérifie une condition *après* l’exécution de la méthode. Avec accès aux paramètres de la fonction | `@ensure(lambda self, montant, result: self.solde == self.solde + montant - montant)` |
| `@inv`     | Vérifie une propriété *toujours vraie* pour un objet.                                             | `@inv(lambda self: self.solde >= 0)`                                                  |

---

## **4. Exemple avec `deal`**

### **Classe `CompteBancaire` améliorée**

```python
from deal import pre, post, inv, ensure


@inv(lambda self: self.solde >= 0)
class CompteBancaire:
    def __init__(self, solde_initial: float):
        self.solde = solde_initial

    @pre(lambda self, montant: montant > 0)  # Le montant doit être positif
    @pre(lambda self, montant: self.solde >= montant)  # Solde suffisant
    @ensure(lambda self, montant, result: self.solde == self.solde + montant - montant)  # Exemple simplifié
    def retirer(self, montant: float) -> float:
        print(f"Retrait de {montant}€ effectué.")
        self.solde -= montant
        return self.solde

    @pre(lambda self, montant: montant > 0)
    def deposer(self, montant: float):
        self.solde += montant
        print(f"Dépôt de {montant}€ effectué.")


# --- Tests ---

compte = CompteBancaire(100)

# 1. Test succès
compte.retirer(50)  # OK

# 2. Violation de précondition (montant négatif)
try:
    compte.retirer(-10)
except Exception as e:
    print(f"Erreur : {e}")  # PreconditionViolation

# 3. Violation de précondition (solde insuffisant)
try:
    compte.retirer(1000)
except Exception as e:
    print(f"Erreur : {e}")  # PreconditionViolation

try:
    compte.solde = -50
except Exception as e:
    print(f"Erreur : {e}")
```

---

## **5. Bonnes pratiques avec `deal`**

✅ **Préfère les `lambda` aux chaînes de caractères** :

- Plus lisible et vérifié par le compilateur.
- Exemple :
  ```python
  @pre(lambda x: x > 0)  # ✅ Bon
  @pre("x > 0")          # ❌ Moins recommandé
  ```

✅ **Place `@inv` au niveau de la classe** :

- Protège tous les attributs, même en cas d’accès direct.

✅ **Utilise `@post` pour valider les retours** :

- Exemple : Vérifier qu’une méthode retourne un nombre positif.

❌ **Évite les conditions trop complexes dans les décorateurs** :

- Si une condition est difficile à lire, extrais-la dans une méthode séparée.

### Est-ce que les pré- et post-conditions sur les types, avec `isinstance`, sont nécessaires si on utilise les indices de type ?

#### **Réponse courte :**

Non, les vérifications de type avec `isinstance` dans les pré/postconditions ne sont **pas strictement nécessaires** si
tu utilises des **annotations de type (type hints)** en Python, mais elles peuvent rester utiles dans certains cas.

---

#### **1. Pourquoi les annotations de type suffisent souvent ?**

Python 3.5+ supporte les **annotations de type** (PEP 484), qui permettent de documenter les types attendus sans
vérification runtime.

##### **Exemple avec `mypy` (vérification statique)**

```python
def diviser(a: float, b: float) -> float:
    return a / b


# mypy détectera une erreur si on appelle :
diviser("10", 2)  # Erreur : Argument 1 doit être un float, pas str
```

- **Avantage** : La vérification se fait à la compilation (ou via `mypy`), pas au runtime.
- **Inconvénient** : Ne fonctionne que si le code est analysé par `mypy` ou un autre outil statique.

---

#### **2. Quand garder `isinstance` dans les pré/postconditions ?**

Même avec des annotations de type, tu peux vouloir garder des vérifications lors de l'exécution (_runtime_) pour :

1. Le **code qui n’est pas analysé par `mypy`** (ex: scripts exécutés directement).
2. Le **cas où le type est dynamique** (ex: arguments passés via `**kwargs`).
3. La **robustesse supplémentaire** (ex: vérifier qu’un argument est bien un nombre, même s’il est annoté comme `float`).

##### **Exemple avec `deal` + annotations de type**

```python
from deal import pre


@pre(lambda x: isinstance(x, float))  # Vérification runtime
def diviser(a: float, b: float) -> float:
    return a / b


# mypy détectera une erreur si on appelle :
diviser("10", 2)  # Erreur statique (mypy)
diviser(10.5, "2")  # Erreur runtime (deal)
```

---

#### **3. Bonnes pratiques**

| Situation                           | Utilisation recommandée                                                         |
|-------------------------------------|---------------------------------------------------------------------------------|
| **Code analysé par `mypy`**         | Annotations de type (`: float`) + éventuellement `@pre` pour des cas critiques. |
| **Code sans vérification statique** | Garde `@pre(lambda x: isinstance(x, ...))` pour éviter les erreurs runtime.     |
| **Types dynamiques (ex: `Any`)**    | Utilise `isinstance` dans les préconditions pour plus de sécurité.              |

---

#### **4. Exemple complet avec `deal` + annotations**

```python
from deal import pre, post


@pre(lambda a, b: isinstance(a, float) and isinstance(b, float))
@post(lambda result: isinstance(result, float))
def diviser(a: float, b: float) -> float:
    return a / b


# Test
print(diviser(10.5, 2))  # OK (10.5 / 2 = 5.25)
print(diviser("10", 2))  # Erreur runtime : "isinstance(a, float)" échoue
```

---

#### **Conclusion**

- **Annotations de type (`: float`)** → Pour la documentation et la vérification statique (via `mypy`).
- **`@pre(lambda x: isinstance(x, ...))`** → Pour une vérification runtime supplémentaire si nécessaire.
- **Choix dépend du contexte** :
    - Si tu utilises `mypy`, les annotations suffisent souvent.
    - Si le code est exécuté sans analyse statique, garde `@pre` pour plus de sécurité.

👉 **En résumé :**

- ✅ **Annotations de type** → Pour la clarté et l’analyse statique.
- ✅ **`@pre`/`isinstance`** → Pour une vérification runtime si besoin.



---

## **6. Comparaison `assert` vs `deal`**

| Critère            | `assert`                        | `deal`               |
|--------------------|---------------------------------|----------------------|
| **Lisibilité**     | Faible                          | Élevée (`lambda`)    |
| **Flexibilité**    | Limitée                         | Très flexible        |
| **Maintenabilité** | Difficile à debuguer            | Clairs et documentés |
| **Performance**    | Légère (désactivable avec `-O`) | Un peu plus lourde   |

---

## **7. Quand utiliser le DbC ?**

- **Projets critiques** (systèmes bancaires, calculs scientifiques).
- **Code collaboratif** pour clarifier les interfaces.
- **Tests automatisés** : Les contrats peuvent servir d’assertions.

---

## **8. Exercice pour les étudiants**

1. **Implémente une classe `Rectangle` avec DbC** :
    - Précondition : La largeur et la hauteur doivent être positives.
    - Postcondition : L'aire doit être positive.
    - Invariant : Le périmètre doit toujours être ≥ 0.

2. **Utilise `deal` pour vérifier les conditions** :
    - `@pre`, `@post`, `@inv`.

3. **Teste avec des cas valides et invalides**.

---

## **9. Ressources supplémentaires**

- [Documentation officielle de `deal`](https://github.com/python-deal/deal)
- [Article sur le DbC en Python](https://realpython.com/python-design-by-contract/)

---

### **Résumé final**

- Le **DbC** améliore la robustesse et la clarté du code.
- En Python, on peut l’implémenter avec :
    - `assert` (simple mais limité),
    - `deal` (recommandé pour des projets sérieux).
- **Préfère `@pre`, `@post`, `@inv` avec `lambda`** pour un code propre et maintenable.
