# Les indices de type (Type Hints)

## Introduction : Pourquoi les Type Hints ?

Dans nos exemples précédents avec `@property`, nous avons utilisé beaucoup de vérifications `isinstance()` pour valider
les types. Par exemple :

```python
@nom.setter
def nom(self, valeur):
    if not isinstance(valeur, str):  # Vérification manuelle du type
        raise TypeError("Le nom doit être une chaîne de caractères")
    # ...
```

Ce code a plusieurs problèmes :

1. **Redondance** : Nous devons écrire la même vérification à plusieurs endroits
2. **Maintenabilité** : Si nous changeons le type attendu, nous devons mettre à jour toutes les vérifications
3. **Documentation** : La signature de la méthode ne montre pas clairement quels types sont attendus
4. **Outils** : Les IDE et outils d'analyse statique (comme mypy) ne peuvent pas aider

Les *Type Hints* (indices de type) résolvent ces problèmes en :

- Documentant les types attendus
- Permettant une vérification automatique
- Améliorant l'expérience développeur avec l'autocomplétion et la détection d'erreurs

## Principes de base des Type Hints

### 1. Syntaxe de base

Les type hints sont ajoutés après le deux-points dans les définitions de fonctions/méthodes :

```python
def ma_fonction(param: type) -> retour:
# implémentation
```

Pour les attributs de classe, on utilise des commentaires ou des annotations :

```python
class MaClasse:
    attribut: type  # Annotation pour les attributs

    def __init__(self):
        self.attribut = valeur  # Pas de vérification automatique ici
```

### 2. Types de base

Python propose plusieurs types intégrés pour les hints :

```python
def exemple(
        entier: int,
        flottant: float,
        chaine: str,
        booleen: bool,
        liste: list[int],  # Liste d'entiers
        tuple: tuple[str, int],  # Tuple avec une chaîne et un entier
        ensemble: set[float],
        dictionnaire: dict[str, int]  # Clés chaînes, valeurs entiers
) -> None:
    pass
```

### 3. Types personnalisés

Pour les classes que vous définissez :

```python
class Personne:
    def __init__(self, nom: str, age: int):
        self.nom = nom
        self.age = age


def saluer(personne: Personne) -> str:
    return f"Bonjour {personne.nom}"
```

### 4. Types optionnels et unions

Pour indiquer qu'une valeur peut être de plusieurs types :

```python
from typing import Optional, Union


def exemple(
        valeur: Optional[int] = None,  # Peut être int ou None
        union: Union[str, float]  # Peut être str ou float
) -> None:
    pass
```

En Python 3.10+, on peut utiliser `|` à la place de `Union` :

```python
def exemple(
        valeur: int | None = None,
        union: str | float
) -> None:
    pass
```

## Exemple motivant : Classe Personne avec Type Hints

Reprenons notre classe `Personne` et voyons comment les type hints améliorent la situation :

### Version sans type hints (avec isinstance)

```python
class Personne:
    def __init__(self, nom: str, age: int):
        if not isinstance(nom, str):
            raise TypeError("Le nom doit être une chaîne de caractères")
        if not isinstance(age, int) or age < 0:
            raise ValueError("L'âge doit être un entier positif")

        self._nom = nom.strip()
        self._age = age

    @property
    def nom(self) -> str:
        return self._nom

    @nom.setter
    def nom(self, valeur: str) -> None:
        if not isinstance(valeur, str):
            raise TypeError("Le nom doit être une chaîne de caractères")
        valeur = valeur.strip()
        if len(valeur) == 0:
            raise ValueError("Le nom ne peut pas être vide après suppression des espaces")
        self._nom = valeur

    @property
    def age(self) -> int:
        return self._age

    @age.setter
    def age(self, valeur: int) -> None:
        if not isinstance(valeur, int) or valeur < 0:
            raise ValueError("L'âge doit être un entier positif")
        self._age = valeur
```

### Version avec type hints (et vérification automatique)

```python
from typing import final


class Personne:
    def __init__(self, nom: str, age: int):
        # Les vérifications de type sont maintenant implicites grâce aux hints
        self.nom = nom  # Utilise le setter pour valider
        self.age = age

    @property
    def nom(self) -> str:
        """Retourne le nom de la personne."""
        return self._nom

    @nom.setter
    def nom(self, valeur: str) -> None:
        """Définie le nom avec validation."""
        valeur = valeur.strip()
        if len(valeur) == 0:
            raise ValueError("Le nom ne peut pas être vide après suppression des espaces")
        self._nom = valeur

    @property
    def age(self) -> int:
        """Retourne l'âge de la personne."""
        return self._age

    @age.setter
    def age(self, valeur: int) -> None:
        """Définie l'âge avec validation."""
        if valeur < 0:
            raise ValueError("L'âge doit être positif")
        self._age = valeur


# Utilisation avec vérification statique
p = Personne(nom="Alice", age=30)
print(p.nom)  # Alice

# Ces lignes seraient détectées par mypy comme des erreurs de type
# p = Personne(nom=123, age="trente")  # Erreur: argument 1 doit être str, reçu int
# p.age = "quarante"  # Erreur: ne peut pas assigner str à int
```

### Avantages de cette approche :

1. **Documentation claire** : La signature montre immédiatement quels types sont attendus
2. **Vérification automatique** : mypy peut détecter les erreurs avant l'exécution
3. **Moins de code dupliqué** : Plus besoin de vérifier `isinstance` pour chaque paramètre
4. **Meilleure expérience développeur** :
    - Autocomplétion dans les IDE
    - Détection des erreurs en temps réel
    - Meilleure compréhension du code

## Exemple complet avec Type Hints et vérification

Pour une solution complète, nous pouvons combiner type hints avec une vérification réelle à l'exécution :

```python
from typing import Any, get_type_hints


class Personne:
    def __init__(self, nom: str, age: int):
        self._valider_types(nom=nom, age=age)
        self.nom = nom
        self.age = age

    @property
    def nom(self) -> str:
        return self._nom

    @nom.setter
    def nom(self, valeur: str) -> None:
        self._valider_type("nom", valeur)
        valeur = valeur.strip()
        if len(valeur) == 0:
            raise ValueError("Le nom ne peut pas être vide après suppression des espaces")
        self._nom = valeur

    @property
    def age(self) -> int:
        return self._age

    @age.setter
    def age(self, valeur: int) -> None:
        self._valider_type("age", valeur)
        if valeur < 0:
            raise ValueError("L'âge doit être positif")
        self._age = valeur

    def _valider_types(self, **kwargs: Any) -> None:
        """Valide les types des arguments en utilisant les type hints."""
        hints = get_type_hints(self.__init__)
        for param, value in kwargs.items():
            if param in hints:
                expected_type = hints[param]
                if not isinstance(value, expected_type):
                    raise TypeError(
                        f"Argument '{param}' doit être {expected_type}, "
                        f"reçu {type(value)}"
                    )

    def _valider_type(self, attr: str, value: Any) -> None:
        """Valide le type d'un attribut en utilisant les type hints."""
        hints = get_type_hints(self)
        if attr in hints:
            expected_type = hints[attr]
            if not isinstance(value, expected_type):
                raise TypeError(
                    f"Attribut '{attr}' doit être {expected_type}, "
                    f"reçu {type(value)}"
                )


# Utilisation
try:
    p = Personne(nom="Bob", age=25)
    print(p.nom)  # Bob

    # Ces lignes lèveront des exceptions à l'exécution
    p.age = "trente"  # TypeError: Attribut 'age' doit être <class 'int'>
except (TypeError, ValueError) as e:
    print(f"Erreur: {e}")
```

## Exemple avec la classe Point

Voici comment nous pourrions réécrire la classe `Point` avec des type hints :

```python
from typing import Union


class Point:
    def __init__(self, x: float = 0.0, y: float = 0.0):
        self.x = x
        self.y = y

    @property
    def x(self) -> float:
        """Retourne la coordonnée x du point."""
        return self._x

    @x.setter
    def x(self, valeur: float) -> None:
        """Définie la coordonnée x avec validation."""
        if valeur < 0:
            raise ValueError("La coordonnée x doit être positive ou nulle")
        self._x = float(valeur)

    @property
    def y(self) -> float:
        """Retourne la coordonnée y du point."""
        return self._y

    @y.setter
    def y(self, valeur: float) -> None:
        """Définie la coordonnée y avec validation."""
        if valeur < 0:
            raise ValueError("La coordonnée y doit être positive ou nulle")
        self._y = float(valeur)

    def distance(self, autre_point: 'Point') -> float:
        """Calcule la distance euclidienne entre deux points.

        Args:
            autre_point: Un autre objet Point

        Returns:
            La distance entre les deux points
        """
        return ((self.x - autre_point.x) ** 2 + (self.y - autre_point.y) ** 2) ** 0.5

    def deplacer(self, dx: float, dy: float) -> None:
        """Déplace le point des coordonnées (dx, dy)."""
        nouvelle_x = self.x + dx
        nouvelle_y = self.y + dy

        if nouvelle_x < 0 or nouvelle_y < 0:
            raise ValueError("Le déplacement résultant en des coordonnées négatives")

        self.x = nouvelle_x
        self.y = nouvelle_y


# Utilisation avec vérification statique
p1: Point = Point(3.0, 4.0)
p2: Point = Point()

print(p1.distance(p2))  # 5.0

# Ces lignes seraient détectées par mypy comme des erreurs de type
# p3: Point = Point("trois", "quatre")  # Erreur: argument doit être float
# p1.deplacer("cinq", 6)  # Erreur: arguments doivent être float
```

## Bonnes pratiques avec les Type Hints

### 1. Utilisez des docstrings complètes

Les type hints ne remplacent pas les docstrings :

```python
def calculer_moyenne(notes: list[float]) -> float:
    """Calcule la moyenne d'une liste de notes.

    Args:
        notes: Liste de notes numériques (doivent être entre 0 et 20)

    Returns:
        La moyenne des notes

    Raises:
        ValueError: Si une note est en dehors de l'intervalle [0, 20]
    """
    if any(n < 0 or n > 20 for n in notes):
        raise ValueError("Toutes les notes doivent être entre 0 et 20")
    return sum(notes) / len(notes)
```

### 2. Utilisez des types spécifiques plutôt que `Any`

Évitez d'utiliser `typing.Any` sauf lorsque vraiment nécessaire :

```python
# Mauvais : trop vague
def traiter_donnees(donnees: Any) -> None:
    pass


# Bon : plus précis
def traiter_donnees(donnees: list[dict[str, Union[int, str]]]) -> None:
    pass
```

### 3. Utilisez des alias de type pour les structures complexes

Pour améliorer la lisibilité :

```python
from typing import TypeAlias

Note: TypeAlias = float  # Une note est un nombre à virgule flottante
EtudiantID: TypeAlias = str  # Un identifiant d'étudiant est une chaîne


class Etudiant:
    def __init__(self, id: EtudiantID, notes: list[Note]):
        self.id = id
        self.notes = notes
```

### 4. Utilisez des protocoles pour le duck typing

Pour les objets qui doivent avoir certains attributs/méthodes :

```python
from typing import Protocol


class Drawable(Protocol):
    def draw(self) -> None: ...


def afficher(obj: Drawable) -> None:
    obj.draw()


# Peut être utilisé avec n'importe quel objet ayant une méthode draw()
class Cercle:
    def draw(self) -> None:
        print("Dessin d'un cercle")


afficher(Cercle())  # Fonctionne
```

### 5. Utilisez des annotations pour les attributs de classe

Pour documenter les attributs de classe :

```python
class Configuration:
    debug: bool = False
    timeout: float = 30.0
    max_connexions: int = 100

    def __init__(self):
        self.debug = True  # Surcharge la valeur par défaut
```

## Outils pour les Type Hints

### 1. mypy - Vérificateur de type statique

Installez avec :

```bash
pip install mypy
```

Utilisation :

```bash
mypy mon_fichier.py
```

Exemple de sortie :

```
mon_fichier.py:5: error: Argument 1 to "Personne" has incompatible type "int"; expected "str"
Found 1 error in 1 file (checked 2 source files)
```

### 2. pyright - Alternative à mypy

Installez avec :

```bash
npm install -g pyright
```

Utilisation :

```bash
pyright mon_fichier.py
```

### 3. IDE Support

La plupart des IDE modernes supportent les type hints :

- **VS Code** : Avec l'extension Python
- **PyCharm** : Support intégré
- **Sublime Text** : Avec des plugins comme LSP-python

### 4. pytype - Vérificateur de Google

Installez avec :

```bash
pip install pytype
```

Utilisation :

```bash
pytype mon_fichier.py
```

## Exercice pratique avec Type Hints

1. **Classe CompteBancaire** :
   ```python
   class CompteBancaire:
       def __init__(self, titulaire: str, solde: float = 0.0):
           # Implémentez avec type hints et validation
           pass

       @property
       def solde(self) -> float:
           pass

       def deposer(self, montant: float) -> None:
           pass

       def retirer(self, montant: float) -> None:
           pass
   ```

2. **Classe Etudiant** :
   ```python
   class Etudiant:
       def __init__(self, nom: str, notes: list[int]):
           # Implémentez avec type hints et validation
           pass

       @property
       def moyenne(self) -> float:
           """Retourne la moyenne des notes."""
           pass
   ```

3. **Fonction de tri personnalisée** :
   ```python
   from typing import Callable, TypeVar

   T = TypeVar('T')

   def tri_personnalise(
       liste: list[T],
       cle: Callable[[T], float]
   ) -> list[T]:
       """Trie une liste en utilisant une clé de comparaison."""
       pass
   ```

## Conclusion

Les type hints sont un outil puissant qui améliore :

1. **La lisibilité** : La signature des fonctions est plus claire
2. **La maintenabilité** : Moins de vérifications manuelles de types
3. **La sécurité** : Détection d'erreurs avant l'exécution
4. **L'expérience développeur** : Meilleure intégration avec les IDE

En combinant type hints et propriétés, vous obtenez un code :

- Bien documenté
- Facile à maintenir
- Sûr grâce aux validations
- Agréable à utiliser grâce à une API propre

Les type hints ne remplacent pas complètement les vérifications à l'exécution (qui restent nécessaires pour la
sécurité), mais ils forment un excellent complément qui améliore significativement la qualité du code.