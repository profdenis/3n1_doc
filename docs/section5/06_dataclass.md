# Les Classes de Données (`@dataclass`)

En programmation orientée objet, on crée souvent des classes dont le seul but est de **stocker des données** (comme le
profil d'un utilisateur, un produit de e-commerce ou un point géographique).

Avant Python 3.7, l'écriture de ces classes exigeait beaucoup de code répétitif (*boilerplate*) pour définir le
constructeur (`__init__`), la représentation textuelle (`__repr__`) ou les comparaisons (`__eq__`).

Le décorateur `@dataclass` du module standard `dataclasses` génère automatiquement toutes ces méthodes spéciales à
partir des annotations de types.

---

## 1. Syntaxe de base : Avant vs Après

### Approche traditionnelle (Sans dataclass)

```python
class LivreTraditionnel:
    def __init__(self, titre: str, auteur: str, pages: int):
        self.titre = titre
        self.auteur = auteur
        self.pages = pages

    def __repr__(self):
        return f"LivreTraditionnel(titre={self.titre!r}, auteur={self.auteur!r}, pages={self.pages})"

    def __eq__(self, other):
        if not isinstance(other, LivreTraditionnel):
            return NotImplemented
        return (self.titre, self.auteur, self.pages) == (other.titre, other.auteur, other.pages)
```

### Approche moderne (Avec `@dataclass`)

Le code suivant est **strictement équivalent** au bloc ci-dessus. Python écrit les méthodes `__init__`, `__repr__` et
`__eq__` à votre place en arrière-plan :

```python
from dataclasses import dataclass


@dataclass
class Livre:
    titre: str
    auteur: str
    pages: int
```

---

## 2. Fonctionnalités générées automatiquement

Grâce au décorateur, les objets créés profitent immédiatement de comportements essentiels :

```python
# 1. Le constructeur __init__ est prêt
livre1 = Livre("Dune", "Frank Herbert", 832)
livre2 = Livre("Dune", "Frank Herbert", 832)
livre3 = Livre("Le Hobbit", "J.R.R. Tolkien", 310)

# 2. Une représentation textuelle propre (__repr__)
print(livre1)
# Sortie : Livre(titre='Dune', auteur='Frank Herbert', pages=832)

# 3. La comparaison par valeur (__eq__)
print(livre1 == livre2)  # True (Les valeurs sont identiques)
print(livre1 == livre3)  # False
```

---

## 3. Valeurs par défaut et Typage

Il est possible d'attribuer des valeurs par défaut aux champs. Comme pour les fonctions classiques, **les champs avec
une valeur par défaut doivent impérativement être placés en dernier**.

```python
@dataclass
class Etudiant:
    nom: str
    filiere: str = "Informatique"  # Valeur par défaut
    actif: bool = True  # Valeur par défaut
```

> ⚠️ **Avertissement pédagogique (Le piège des types mutables) :**
> On ne peut pas mettre une liste vide `[]` ou un dictionnaire `{}` directement comme valeur par défaut (ex:
> `notes: list = []` lèvera une erreur). Il faut utiliser la fonction `field` avec `default_factory` :
> ```python
> from dataclasses import dataclass, field
> 
> @dataclass
> class Classe:
>     eleves: list = field(default_factory=list) # Crée une nouvelle liste pour chaque instance
> ```

---

## 4. Rendre un objet immuable (`frozen`)

Si vous souhaitez que les données ne puissent pas être modifiées après la création de l'objet (équivalent à un tuple
nommé), activez l'option `frozen=True`.

```python
@dataclass(frozen=True)
class Position:
    x: float
    y: float


p = Position(10.5, 20.0)
# p.x = 15.0  <-- Lèvera une FrozenInstanceError
```

L'avantage majeur de `frozen=True` est que l'objet devient **hachable** (`__hash__`). Vos étudiants peuvent ainsi
utiliser ces instances comme **clés dans un dictionnaire** ou dans un **ensemble (`set`)**.

---

## 5. Personnalisation avec `post_init`

Parfois, on a besoin de valider des données ou de calculer un champ dérivé juste après la création de l'objet. La
méthode `__post_init__` sert précisément à cela :

```python
@dataclass
class Produit:
    nom: str
    prix_ht: float
    taux_tva: float = 0.20
    prix_ttc: float = field(init=False)  # init=False signifie qu'on ne le passe pas au constructeur

    def __post_init__(self):
        # Validation simple
        if self.prix_ht < 0:
            raise ValueError("Le prix HT ne peut pas être négatif.")

        # Calcul automatique du champ dérivé
        self.prix_ttc = self.prix_ht * (1 + self.taux_tva)


# Utilisation
p = Produit("Clavier", 50.0)
print(p.prix_ttc)  # Sortie : 60.0
```

---

## Résumé des bonnes pratiques

1. Utilisez les `@dataclass` dès qu'une classe sert principalement à **contenir de l'état (des données)** plutôt qu'à
   définir des comportements complexes.
2. N'oubliez pas les **annotations de types** (`str`, `int`, etc.), elles sont obligatoires pour que le décorateur
   détecte les champs.
3. Préférez `frozen=True` si les données lues ne doivent plus bouger au cours de l'exécution, cela sécurise le code.
