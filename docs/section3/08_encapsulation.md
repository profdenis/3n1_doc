# **8. Encapsulation et Intégrité**

Est-ce que la définition d'_encapsulation_ inclut également la _validation_ et le maintien de l'_intégrité_ de
l'état des objets, ou est-ce que l'_encapsulation_ et l'_intégrité_ sont habituellement définies séparément ?

### **Réponse courte :**

L'**encapsulation** en programmation orientée objet (POO) se concentre principalement sur **la restriction de l'accès
aux données internes d'une classe**, mais elle est souvent associée à la **validation et au maintien de l'intégrité des
objets**. Cependant, ces deux concepts sont parfois distingués :

- **Encapsulation stricte** = Masquage des détails internes (ex: attributs privés).
- **Intégrité des objets** = Validation des modifications d'état (ex: vérifications avec `@inv` ou méthodes setters).

---

## **1. Définition classique de l'encapsulation**

L'encapsulation est définie comme :
> *"Le mécanisme qui cache les détails internes d'un objet et ne permet l'accès qu'à travers des méthodes publiques."*

**Exemple en Python :**

```python
class CompteBancaire:
    def __init__(self, solde):
        self.__solde = solde  # Attribut privé (encapsulation)

    def deposer(self, montant):  # Méthode publique pour modifier le solde
        if montant > 0:
            self.__solde += montant


# Accès direct interdit :
compte = CompteBancaire(100)
compte.deposer(50)  # OK (méthode publique)
compte.__solde = -100  # Échoue (attribut privé)
```

---

## **2. Validation et intégrité : Une extension de l'encapsulation ?**

La validation des modifications d'état est souvent **considérée comme une partie de l'encapsulation**, car elle garantit
que :

- Les objets restent dans un état valide.
- Les règles métier sont respectées.

**Exemple avec validation :**

```python
class CompteBancaire:
    def __init__(self, solde):
        self.__solde = solde

    def deposer(self, montant):
        if montant <= 0:  # Validation
            raise ValueError("Montant doit être positif")
        self.__solde += montant


# Test :
compte.deposer(-50)  # Lève ValueError (validation échoue)
```

---

## **3. Différence entre encapsulation et intégrité**

| Concept                    | Description                           | Exemple                                    |
|----------------------------|---------------------------------------|--------------------------------------------|
| **Encapsulation**          | Masquage des détails internes.        | Attributs privés (`__solde`).              |
| **Intégrité (Validation)** | Vérification que l'état reste valide. | `if montant > 0: self.__solde += montant`. |

**Cas où ils sont séparés :**

- Une classe peut être bien encapsulée (attributs privés) mais sans validation.
- Exemple :
  ```python
  class CompteBancaire:
      def __init__(self, solde):
          self.__solde = solde  # Encapsulation OK

      def set_solde(self, nouveau_solde):  # Pas de validation !
          self.__solde = nouveau_solde  # Risque : solde négatif !

  compte.set_solde(-100)  # Problème d'intégrité !
  ```

---

## **4. Combinaison avec le Design by Contract (DbC)**

Le DbC (avec `deal`) renforce l'encapsulation en :

- Vérifiant les préconditions (`@pre`).
- Garantissant les invariants (`@inv`).

**Exemple :**

```python
from deal import inv


@inv(lambda self: self.__solde >= 0)  # Invariant : solde toujours ≥ 0
class CompteBancaire:
    def __init__(self, solde):
        self.__solde = solde

    def deposer(self, montant):
        if montant > 0:
            self.__solde += montant


# Test :
compte = CompteBancaire(100)
compte.deposer(50)  # OK
compte.__solde = -50  # Lève AssertionError (invariant violé)
```

---

## **5. Conclusion**

- **Encapsulation** = Masquage des détails internes.
- **Intégrité** = Validation des modifications d'état (souvent associée à l'encapsulation).
- **DbC (`deal`)** = Outils pour formaliser ces vérifications.

**Bonnes pratiques :**

- ✅ Utilisez l'encapsulation pour cacher les attributs.
- ✅ Ajoutez des validations pour maintenir l'intégrité.
- ✅ Utilisez `@inv` (DbC) pour des règles globales.

---

### **Résumé final**

| Concept           | Rôle                              | Outils                                       |
|-------------------|-----------------------------------|----------------------------------------------|
| **Encapsulation** | Cacher les détails internes.      | Attributs privés (`__`), méthodes publiques. |
| **Intégrité**     | Valider les modifications d'état. | Vérifications dans les setters, `@inv`.      |

L'encapsulation et l'intégrité sont souvent combinées, mais elles peuvent être distinguées selon le contexte.