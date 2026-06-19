# **Les Protocoles**

*L'équivalent des interfaces Java pour la programmation orientée objet*

---

## **1. Qu’est-ce qu’un Protocole ?**

Un **`Protocol`** est une façon de définir une **interface** (un contrat) en Python, similaire aux `interface` en Java.
Il permet de spécifier les méthodes qu’une classe doit implémenter, sans héritage forcé.

### **Comparaison avec Java**

| Concept        | Java (`interface`)                     | Python (`Protocol`)                                                        |
|----------------|----------------------------------------|----------------------------------------------------------------------------|
| Définition     | `interface Animal { void manger(); }`  | `@runtime_checkable class Animal(Protocol): def manger(self) -> None: ...` |
| Implémentation | `class Chat implements Animal { ... }` | Pas besoin de déclarer l’héritage (`class Chat: ...`).                     |

---

## **2. Pourquoi utiliser les Protocols ?**

- **Flexibilité** : Une classe peut implémenter un `Protocol` sans en hériter.
- **Duck Typing** : "Si ça marche comme un canard, c’est un canard."
- **Vérification statique** (avec `mypy`) pour une meilleure sécurité des types.

!!! note "Duck Typing"
    En programmation informatique, le typage canard (_duck typing_) est une application du test du canard 
    _« Si ça marche comme un canard et que ça cancan comme un canard, alors c'est un canard »_,
    ou en anglais _« If it walks like a duck and it quacks like a duck, then it must be a duck »_, 
    pour déterminer si un objet peut être utilisé à un but particulier.

    Avec le **typage nominatif**, un objet est d'un type donné s'il est déclaré comme tel (ou si
    l'association d'un type avec l'objet est déduite par des mécanismes tels que l'héritage d'objets). Avec le typage
    canard, un objet est d'un type donné s'il possède toutes les méthodes et propriétés requises par ce type. Le
    typage canard peut être considéré comme une équivalence structurelle basée sur l'utilisation entre un objet donné 
    et les exigences d'un type. [src](https://en.wikipedia.org/wiki/Duck_typing)

---

## **3. Exemple de Protocol simple**

### **Définition d’un Protocol**

```python
from typing import Protocol


class Forme(Protocol):
    def aire(self) -> float: ...

    def perimetre(self) -> float: ...


# Une classe qui implémente Forme (sans héritage)
class Cercle:
    def __init__(self, rayon: float):
        self.rayon = rayon

    def aire(self) -> float:
        return 3.14 * self.rayon ** 2

    def perimetre(self) -> float:
        return 2 * 3.14 * self.rayon


# Une autre classe qui implémente Forme
class Carre:
    def __init__(self, cote: float):
        self.cote = cote

    def aire(self) -> float:
        return self.cote ** 2

    def perimetre(self) -> float:
        return 4 * self.cote
```

### **Utilisation avec une fonction générique**

```python
def calculer_aire(forme: Forme) -> float:
    return forme.aire()


# Test :
cercle = Cercle(5)
carre = Carre(4)

print(calculer_aire(cercle))  # Affiche : 78.5 (3.14 * 5²)
print(calculer_aire(carre))  # Affiche : 16 (4²)
```

---

## **4. Protocols avec `runtime_checkable`**

Pour vérifier dynamiquement si une classe implémente un `Protocol`, utilise `@runtime_checkable`.

### **Exemple**

```python
from typing import Protocol, runtime_checkable


@runtime_checkable
class Forme(Protocol):
    def aire(self) -> float: ...


class Cercle:
    def aire(self) -> float:
        return 3.14 * 5 ** 2


# Vérification dynamique
print(isinstance(Cercle(), Forme))  # Affiche : True (Cercle implémente Forme)
```

---

## **5. Protocols avec des attributs**

Un `Protocol` peut aussi définir des **attributs** (pas seulement des méthodes).

### **Exemple**

```python
from typing import Protocol


class Animal(Protocol):
    nom: str  # Attribut requis

    def manger(self) -> None: ...


class Chat:
    def __init__(self, nom: str):
        self.nom = nom  # Implémente l'attribut `nom`

    def manger(self) -> None:
        print(f"{self.nom} mange.")


# Test :
chat = Chat("Milo")
print(chat.nom)  # Affiche : "Milo"
chat.manger()  # Affiche : "Milo mange."
```

---

## **6. Protocols avec des types génériques**

Un `Protocol` peut être combiné avec des **types génériques**.

### **Exemple**

```python
from typing import Protocol, TypeVar

T = TypeVar('T')


class Comparable(Protocol[T]):
    def comparer(self, autre: T) -> int: ...


class Personne:
    def __init__(self, age: int):
        self.age = age

    def comparer(self, autre: 'Personne') -> int:
        return self.age - autre.age  # Retourne un nombre positif si plus âgé


# Test :
p1 = Personne(25)
p2 = Personne(30)
print(p1.comparer(p2))  # Affiche : -5 (p1 est plus jeune que p2)
```

---

## **7. Bonnes pratiques avec les Protocols**

✅ **Utilise `Protocol` pour définir des interfaces flexibles.**
✅ **Préfère `@runtime_checkable` pour les vérifications dynamiques.**
✅ **Combine avec des types génériques pour plus de polyvalence.**

---

## **8. Exercice pour les étudiants**

### **Consigne**

1. Créez un `Protocol` `Dessinable` avec une méthode `dessiner()`.
2. Implémentez deux classes (`Cercle` et `Ligne`) qui respectent ce `Protocol`.
3. Écrivez une fonction `afficher_dessin(dessin: Dessinable)` qui appelle `dessiner()`.

??? info "Solution"

        ```python
        from typing import Protocol
        
        
        class Dessinable(Protocol):
            def dessiner(self) -> None: ...
        
        
        class Cercle:
            def dessiner(self) -> None:
                print("Dessine un cercle.")
        
        
        class Ligne:
            def dessiner(self) -> None:
                print("Dessine une ligne.")
        
        
        def afficher_dessin(dessin: Dessinable) -> None:
            dessin.dessiner()
        
        
        # Test :
        cercle = Cercle()
        ligne = Ligne()
        
        afficher_dessin(cercle)  # Affiche : "Dessine un cercle."
        afficher_dessin(ligne)  # Affiche : "Dessine une ligne."
        ```

---

## **9. Ressources supplémentaires**

- [Documentation Python sur `typing.Protocol`](https://docs.python.org/3/library/typing.html#typing.Protocol)
- [Article sur les Protocols et le Duck Typing](https://realpython.com/python-protocols/)

---

### **Résumé final**

| Concept        | Java (`interface`)                     | Python (`Protocol`)                                                        |
|----------------|----------------------------------------|----------------------------------------------------------------------------|
| Définition     | `interface Animal { void manger(); }`  | `@runtime_checkable class Animal(Protocol): def manger(self) -> None: ...` |
| Implémentation | `class Chat implements Animal { ... }` | Pas besoin de déclarer l’héritage (`class Chat: ...`).                     |

**Points clés :**

- Les `Protocols` permettent de définir des **interfaces flexibles**.
- Ils sont utiles pour le **Duck Typing** et la vérification statique (`mypy`).
- Combinaison possible avec les **types génériques**.
