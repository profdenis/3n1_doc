# **Extension de `dict` en Python : Pourquoi éviter l'héritage ?**

## **1. Problème avec l'héritage direct de `dict`**

Le dictionnaire Python (`dict`) utilise une **implémentation optimisée en C** (pour les performances). Si tu hérites
directement, tu risques :

- **Des comportements inattendus** : Certaines méthodes peuvent ne pas se comporter comme prévu.
- **Des problèmes de maintenance** : L'API interne de `dict` peut changer entre versions.

### **Exemple problématique**

```python
class MonDict(dict):
    def __setitem__(self, key, value):
        if not isinstance(value, int):  # Exige que les valeurs soient des entiers
            raise ValueError("Les valeurs doivent être des entiers")
        super().__setitem__(key, value)


# Test :
d = MonDict()
d["a"] = 10  # OK
d["b"] = "hello"  # Lève ValueError (comme attendu)
```

**Problème :**

- Certaines opérations internes de `dict` (ex: `update()`) peuvent contourner `__setitem__`.
- Exemple :
  ```python
  d.update({"c": "world"})  # Échappe à la validation ! (pas d'erreur)
  ```

---

## **2. Solution recommandée : Utiliser `collections.UserDict`**

`UserDict` est une **classe wrapper** autour de `dict`, conçue pour être héritée en toute sécurité.

### **Exemple avec `UserDict`**

```python
from collections import UserDict


class MonDict(UserDict):
    def __setitem__(self, key, value):
        if not isinstance(value, int):  # Validation
            raise ValueError("Les valeurs doivent être des entiers")
        super().__setitem__(key, value)


# Test :
d = MonDict()
d["a"] = 10  # OK
d["b"] = "hello"  # Lève ValueError (comme attendu)
d.update({"c": "world"})  # Lève maintenant ValueError ! ✅
```

### **Pourquoi `UserDict` fonctionne mieux ?**

- **Toutes les opérations passent par `__setitem__`** (même `update()`).
- **Comportement prévisible** : Pas de contournement des validations.

---

## **3. Relation avec les ABC (Abstract Base Classes)**

`dict` est une **ABC** (classe abstraite) depuis Python 3.3, définie dans le module `collections.abc`.

### **Exemple d'utilisation avec `Mapping` (ABC pour les dictionnaires)**

```python
from collections.abc import Mapping


class MonDict(Mapping):  # Héritage d'une ABC
    def __init__(self, data):
        self._data = data

    def __getitem__(self, key):
        return self._data[key]

    def __iter__(self):
        return iter(self._data)

    def __len__(self):
        return len(self._data)


# Test :
d = MonDict({"a": 1, "b": 2})
print(d["a"])  # Affiche : 1
```

### **Quand utiliser `Mapping` ?**

- Si tu veux **implémenter un dictionnaire personnalisé** sans dépendre de l'API interne de `dict`.
- Pour des cas avancés où tu as besoin d'un contrôle total sur le comportement.

---

## **4. Bonnes pratiques pour étendre `dict`**

| Approche                      | Quand l'utiliser ?                                 | Exemple                                |
|-------------------------------|----------------------------------------------------|----------------------------------------|
| **Héritage direct de `dict`** | ❌ À éviter (risque de bugs).                       | `class MonDict(dict): ...`.            |
| **`UserDict`**                | ✅ Pour ajouter des validations ou fonctionnalités. | `from collections import UserDict`.    |
| **`Mapping` (ABC)**           | ✅ Pour implémenter un dictionnaire personnalisé.   | `from collections.abc import Mapping`. |

---

## **5. Exemple complet avec `UserDict`**

```python
from collections import UserDict


class CompteBancaire(UserDict):
    def __setitem__(self, key, value):
        if not isinstance(value, (int, float)):  # Validation du type
            raise ValueError("Le solde doit être un nombre")
        super().__setitem__(key, value)

    def deposer(self, compte_id, montant):
        """Ajoute un montant au solde d'un compte."""
        if montant <= 0:
            raise ValueError("Montant doit être positif")
        self[compte_id] += montant


# Test :
comptes = CompteBancaire({"Alice": 100, "Bob": 200})
comptes.deposer("Alice", 50)  # OK
print(comptes["Alice"])  # Affiche : 150
```

---

## **6. Conclusion**

- **Évite d'hériter directement de `dict`** (risque de bugs).
- **Préfère `UserDict`** pour ajouter des fonctionnalités.
- **Utilise `Mapping` (ABC)** si tu veux un contrôle total sur le comportement.

👉 **En résumé :**

- ✅ **`UserDict`** → Pour étendre `dict` en toute sécurité.
- ✅ **`Mapping` (ABC)** → Pour implémenter un dictionnaire personnalisé.
