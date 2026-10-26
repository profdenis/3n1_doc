# Approche hybride : Le Mixin comme injecteur de Stratégie

## Approche 1 : Comparateur de nom

Dans la section précédente, nous avons vu que le patron **Stratégie** (via le `Comparator`) est la solution idéale pour
injecter un comportement de comparaison externe sans polluer la hiérarchie de classes.

Cependant, dans un langage comme Python, on peut choisir une approche hybride : utiliser un **Mixin** pour injecter une
"stratégie de comparaison" directement dans plusieurs classes qui n'ont aucun lien de parenté.

### Le dilemme : Est-ce un "mauvais" héritage ?

On pourrait être tenté de croire que faire hériter `User` et `Product` d'un `NameComparatorMixin` est une erreur, car
cela ressemble à l'héritage de l'exemple "problématique" du chapitre précédent. La nuance réside dans la **nature de la
relation** :

1. **L'erreur (Is-a) :** Faire hériter une classe de `Comparable` est risqué car on tente de définir l' **identité** de
   l'objet (ce qu'il *est*). On force l'objet à entrer dans une hiérarchie de types rigide.
2. **La solution (Can-do) :** Utiliser un Mixin pour ajouter une méthode de comparaison est une extension de
   **capacité**. On ne dit pas que `User` *est* un comparateur, on dit que `User` *possède la capacité* d'être comparé
   par nom.

### Implémentation : Mixin, Protocol et Mypy

Pour rendre cette injection de comportement robuste et compréhensible pour les outils de vérification de type comme
`mypy`, on utilise un **Protocol**. Le Mixin ne se contente pas de "supposer" que la méthode existe ; il exige
contractuellement que la classe hôte respecte une certaine forme.

```python
from typing import Protocol, Any


# 1. Le PROTOCOLE : Il définit ce que le Mixin exige de la classe hôte.
# On ne dit pas que l'objet EST un "HasName", on dit qu'il doit avoir l'attribut "name".
class HasName(Protocol):
    name: str


# 2. LE MIXIN : Il implémente une stratégie de comparaison spécifique.
# Il est petit, a une seule responsabilité et n'est pas instancié seul.
class NameComparatorMixin:
    """Ajoute la capacité de se comparer par nom."""

    def compare_to_name(self, other: HasName) -> int:
        # Le Mixin utilise l'attribut 'name' de l'instance (self) 
        # et de l'autre objet (other), garantis par le Protocol.
        if self.name < other.name:
            return -1
        if self.name > other.name:
            return 1
        return 0


# 3. LES CLASSES MÉTIER : Elles sont totalement indépendantes au départ.
class User:
    def __init__(self, name: str, user_id: int):
        self.name = name
        self.user_id = user_id


class Product:
    def __init__(self, name: str, price: float):
        self.name = name
        self.price = price


# 4. L'APPLICATION : On "injecte" la capacité via l'héritage multiple.
class SortableUser(NameComparatorMixin, User):
    pass


class SortableProduct(NameComparatorMixin, Product):
    pass


# --- Test ---
u = SortableUser("Alice", 1)
p = SortableProduct("Bob", 10.5)

print(u.compare_to_name(p))  # Résultat : -1 (Alice < Bob)
```

### Pourquoi l'héritage multiple est-il approprié ici ?

L'utilisation d'un Mixin pour cette tâche est une application saine du design pour trois raisons :

* **Découplage de l'identité :** `User` et `Product` restent des entités métier pures. L'héritage multiple n'intervient
  que pour ajouter une "option" de comparaison. Si on n'en a pas besoin, on ne l'hérite pas.
* **Évite l'explosion des classes :** Au lieu de créer des sous-classes `UserByName`, `UserByAge`, `ProductByName`,
  etc., on crée des mixins de capacités (`NameComparatorMixin`, `PriceComparatorMixin`) que l'on assemble à la carte.
* **Sûreté contractuelle :** Grâce au `Protocol`, le développeur (et `mypy`) sait exactement pourquoi le Mixin pourrait
  échouer : si la classe hôte ne possède pas l'attribut `name`, le code est considéré comme invalide avant même
  l'exécution.

**En résumé :** On utilise l'héritage multiple non pas pour construire une hiérarchie de types, mais pour assembler des
**comportements interchangeables** sur des objets qui n'ont rien à voir entre eux. C'est le passage de l'héritage de
*nature* à l'héritage de *fonctionnalité*.

Voici la version corrigée de la section. En utilisant une **propriété** (`@property`) dans le `Protocol`, on permet au
Mixin d'accéder à la valeur via `self.key` (comme un attribut), tout en permettant aux classes métier de calculer cette
valeur dynamiquement si nécessaire.

---

## Approche 2 : L'extraction de clé (L'approche générique par propriété)

Dans l'approche précédente, le Mixin était "spécialisé" : il savait qu'il comparait des noms. Mais on peut pousser la
logique encore plus loin en utilisant un concept plus abstrait : l' **extraction de clé**.

Au lieu de dire au Mixin "compare les noms", on lui impose un contrat : "toute classe utilisant ce Mixin doit exposer
une propriété nommée `key`, qui représente sa valeur de comparaison (sa clé primaire)".

### Implémentation : Le Mixin "Key-Based" avec Protocol

En utilisant un `Protocol` qui définit une propriété, on permet au Mixin d'accéder à la valeur via `self.key` de manière
très fluide, tout en restant totalement agnostique sur la nature de cette clé (un entier, une chaîne, une date, etc.).

```python
from typing import Protocol, Any


# 1. Le PROTOCOLE : Définit une "interface de propriété"
# On exige que l'objet possède une propriété 'key'
class KeyProvider(Protocol):
    @property
    def key(self) -> Any:
        """Retourne la valeur servant de critère de comparaison."""
        ...


# 2. LE MIXIN : Un comparateur universel de propriétés
class KeyComparatorMixin:
    """Ajoute la capacité de se comparer via une propriété 'key'."""

    def compare_to_key(self, other: KeyProvider) -> int:
        # On accède à 'key' comme un attribut (grâce au protocole)
        # Le Mixin ne sait pas ce qu'est la clé, il sait juste qu'elle est comparable
        val1 = self.key
        val2 = other.key

        if val1 < val2:
            return -1
        if val1 > val2:
            return 1
        return 0


# 3. LES CLASSES MÉTIER : Elles implémentent la propriété 'key'
class Utilisateur:
    def __init__(self, id_num: int, nom: str):
        self.id_num = id_num
        self.nom = nom

    @property
    def key(self) -> int:
        return self.id_num


class Produit:
    def __init__(self, reference: str, prix: float):
        self.reference = reference
        self.prix = prix

    @property
    def key(self) -> float:
        return self.prix


# 4. L'APPLICATION : L'héritage multiple injecte la capacité de comparaison
class SortableUser(KeyComparatorMixin, Utilisateur):
    pass


class SortableProduct(KeyComparatorMixin, Produit):
    pass


# --- Test ---
u = SortableUser(10, "Alice")
p = SortableProduct("ABC", 49.99)

# La comparaison est possible même entre des types différents si les clés le permettent
print(f"Comparaison (10 vs 49.99) : {u.compare_to_key(p)}") 
```

---

## Discussion : Quelle approche choisir ?

Nous avons maintenant deux manières d'utiliser un Mixin pour injecter un comportement de comparaison. Le choix dépend de
la volonté de spécialiser ou de généraliser la logique.

| Caractéristique                 | **Approche 1 : Spécifique** (ex: `NameMixin`)                          | **Approche 2 : Générique** (via la propriété `key`)         |
|:--------------------------------|:-----------------------------------------------------------------------|:------------------------------------------------------------|
| **Responsabilité du Mixin**     | Elle sait **ce qu'elle** compare (le nom).                             | Elle sait **comment** comparer (comparer deux valeurs).     |
| **Responsabilité de la Classe** | Elle possède une propriété (ex: `self.name`).                          | Elle définit sa propre "clé" via une propriété.             |
| **Flexibilité**                 | **Faible** : Il faut un mixin par attribut (`AgeMixin`, `PriceMixin`). | **Maximale** : Un seul mixin suffit pour tout type d'objet. |
| **Sûreté (Mypy)**               | Très élevée : vérifie la présence de l'attribut.                       | Élevée : vérifie la présence de la propriété `key`.         |
| **Découplage**                  | Le Mixin est couplé à la structure de l'objet.                         | Le Mixin est totalement découplé de la structure.           |

### Laquelle est la meilleure ?

1. **L'approche Spécifique** est préférable lorsque le comportement de comparaison est une **propriété intrinsèque et
   immuable** de l'objet (ex: on veut toujours comparer les noms). Elle est très explicite : lire
   `User.compare_by_name()` est immédiatement compréhensible.

2. **L'approche Générique (via `key`)** est la plus puissante pour la **réutilisabilité**. Elle transforme le Mixin en
   un véritable outil de conception : le Mixin fournit l'algorithme de comparaison, et l'objet fournit la "stratégie" de
   sélection de la donnée à comparer via sa propriété `key`. C'est l'approche la plus proche du **Patron Stratégie**
   pur, car elle sépare la *logique de comparaison* (le Mixin) de la *logique de sélection de la donnée* (la propriété
   de l'objet).

**Conclusion du design :**
Dans les deux cas, l'utilisation du Mixin via l'héritage multiple reste une application saine du principe **"Can-do"**
(Capacité) : on ne redéfinit pas l'identité de l'objet, on lui donne simplement un nouvel outil pour interagir avec le
monde.

---

## L'approche "Pythonique" : Les Comparaisons Riches (Rich Comparisons)

L'approche générique par propriété `key` est puissante, mais elle reste limitée si l'on doit appeler explicitement une
méthode comme `u.compare_to_key(p)`. En Python, la philosophie est de rendre les objets "naturels". Un objet comparable
doit pouvoir répondre aux opérateurs standards : `<`, `==`, `>`, etc.

C'est ce qu'on appelle les **comparaisons riches**.

### Implémentation : Mixin et `total_ordering`

Pour implémenter cela proprement sans une explosion de code, on utilise `functools.total_ordering`. Ce décorateur permet
de ne définir que deux méthodes (`__eq__` et `__lt__`) pour que Python génère automatiquement toutes les autres (`<=`,
`>`, `>=`).

```python
from typing import Protocol, Any, runtime_checkable
from functools import total_ordering


# 1. Le PROTOCOLE : On définit ce qu'est un objet "comparable par clé"
@runtime_checkable
class KeyProvider(Protocol):
    @property
    def key(self) -> Any:
        ...


# 2. LE MIXIN : On utilise @total_ordering pour une implémentation propre
@total_ordering
class KeyComparisonMixin:
    """Ajoute la capacité de comparaison standard via la propriété 'key'."""

    def __eq__(self: KeyProvider, other: Any) -> bool:
        if not isinstance(other, KeyProvider):
            return NotImplemented  # Indique à Python qu'il ne sait pas comparer
        return self.key == other.key

    def __lt__(self: KeyProvider, other: Any) -> bool:
        if not isinstance(other, KeyProvider):
            return NotImplemented
        return self.key < other.key


# 3. LES CLASSES MÉTIER : Elles restent simples et focalisées sur la donnée
class Utilisateur:
    def __init__(self, id_num: int, nom: str):
        self.id_num = id_num
        self.nom = nom

    @property
    def key(self) -> int:
        return self.id_num


class Produit:
    def __init__(self, reference: str, prix: float):
        self.reference = reference
        self.prix = prix

    @property
    def key(self) -> float:
        return self.prix


# 4. L'APPLICATION : L'héritage multiple injecte les dunders standards
class SortableUser(KeyComparisonMixin, Utilisateur):
    pass


class SortableProduct(KeyComparisonMixin, Produit):
    pass


# --- Test de l'élégance Pythonique ---
u1 = SortableUser(10, "Alice")
u2 = SortableUser(20, "Bob")
p1 = SortableProduct("A", 15.0)

print(f"u1 < u2 ? {u1 < u2}")  # True (10 < 20)
print(f"u1 == u2 ? {u1 == u2}")  # False (10 == 20)
print(f"u1 > u2 ? {u1 > u2}")  # False
print(f"u1 <= u2 ? {u1 <= u2}")  # True (généré par total_ordering)
print(f"u1 == p1 ? {u1 == p1}")  # False (10 == 15.0, mais gère le type grâce à l'isinstance)
```

### Pourquoi c'est la version "ultime" ?

1. **Syntaxe naturelle :** On n'écrit plus `u1.compare_to_key(u2)`, on écrit `u1 < u2`. C'est l'essence même du langage
   Python.
2. **Compatibilité avec l'écosystème :** En redéfinissant `__lt__` et `__eq__`, vos objets deviennent compatibles avec
   toutes les fonctions de l'API standard de Python. Ils peuvent être triés par `sorted(ma_liste)`, utilisés comme clés
   dans un dictionnaire, ou comparés dans des expressions complexes.
3. **Efficacité (DRY) :** Grâce à `@total_ordering`, nous n'avons écrit que deux méthodes de comparaison. Le décorateur
   s'occupe de la logique mathématique pour les autres (si `a < b` est faux et `a == b` est faux, alors `a > b` est
   forcément vrai).
4. **Robustesse (NotImplemented) :** En retournant `NotImplemented` au lieu d'une erreur si l'objet n'est pas
   compatible, on permet à Python de demander à l'autre objet s'il sait gérer la comparaison (ce qui est la base du
   polymorphisme de comparaison).

**Résumé :**
L'utilisation de Mixins combinée aux dunders et à `total_ordering` permet de transformer un simple "ajout de
comportement" en une véritable **extension du langage** pour vos propres objets. On passe d'une approche "appel de
méthode" à une approche "intégration au langage".

### Variation : Sécurité et Typage Strict

Pour passer du code "qui marche" au code de production, nous devons résoudre deux problèmes de typage :

1. **Le Typage au runtime :** Les `Protocol` ne sont, par défaut, que des outils pour le vérificateur de type. Pour que
   `isinstance()` fonctionne réellement à l'exécution, il faut utiliser le décorateur `@runtime_checkable`.
2. **Le Typage statique (mypy) :** Un Mixin est une classe qui "s'attend" à ce que l'objet qui l'hérite respecte un
   contrat. Pour que `mypy` accepte que `self.key` existe, nous avons trois solutions :
    * **La solution "Cast" (Performance) :** On force le type avec `cast`. C'est rapide car c'est une opération nulle au
      runtime, mais c'est un "mensonge" au compilateur.
    * **La solution "Self-Hint" :** `self: KeyProvider`. C'est efficace, mais un peu lourd syntaxiquement.
    * **La solution "Type Narrowing" (La plus robuste) :** On utilise `isinstance(self, KeyProvider)` à l'intérieur de
      la méthode. Cela fait double emploi : cela sécurise le runtime **ET** cela informe `mypy` que, dans ce bloc de
      code, `self` possède bien la propriété `key`.

Voici la version optimisée :

```python
from typing import Protocol, Any, runtime_checkable, cast
from functools import total_ordering


# 1. Le PROTOCOLE avec @runtime_checkable
# Indispensable pour que isinstance(obj, KeyProvider) fonctionne à l'exécution
@runtime_checkable
class KeyProvider(Protocol):
    @property
    def key(self) -> Any:
        ...


# 2. Le MIXIN "Expert"
@total_ordering
class KeyComparisonMixin:
    """Ajoute la capacité de comparaison standard via la propriété 'key'."""

    def __eq__(self, other: Any) -> bool:
        # On vérifie que 'other' respecte le contrat
        if not isinstance(other, KeyProvider):
            return NotImplemented

        # On vérifie que 'self' respecte le contrat (Type Narrowing)
        # Cette étape est magique : elle sécurise le runtime ET 
        # elle "rassure" mypy que self.key existe.
        if not isinstance(self, KeyProvider):
            return NotImplemented

        return self.key == other.key

    def __lt__(self, other: Any) -> bool:
        if not isinstance(other, KeyProvider) or not isinstance(self, KeyProvider):
            return NotImplemented
        return self.key < other.key


# 3. LES CLASSES MÉTIER (Inchangées)
class Utilisateur:
    def __init__(self, id_num: int, nom: str):
        self.id_num = id_num
        self.nom = nom

    @property
    def key(self) -> int:
        return self.id_num


class Produit:
    def __init__(self, reference: str, prix: float):
        self.reference = reference
        self.prix = prix

    @property
    def key(self) -> float:
        return self.prix


# 4. L'APPLICATION
class SortableUser(KeyComparisonMixin, Utilisateur):
    pass


class SortableProduct(KeyComparisonMixin, Produit):
    pass


# --- Test ---
u = SortableUser(10, "Alice")
p = SortableProduct("ABC", 49.99)

print(f"u < p ? {u < p}")  # False
print(f"u == p ? {u == p}")  # False
print(f"u < u ? {u < u}")  # False
```

### Variation : La méthode "Scalpel" avec un `type: ignore` ciblé

Il ne faut pas utiliser un simple `# type: ignore` (qui est une "masse" qui ignore toutes les erreurs sur la ligne),
mais un **`type: ignore` ciblé**. Cela permet de dire à `mypy` : *"N'ignore que l'erreur spécifique liée à l'absence de
l'attribut, mais continue de vérifier si j'ai fait une faute ailleurs sur cette même ligne."*

L'erreur que `mypy` lève est généralement `attr-defined`.

```python
from typing import Protocol, Any, runtime_checkable
from functools import total_ordering


@runtime_checkable
class KeyProvider(Protocol):
    @property
    def key(self) -> Any:
        ...


@total_ordering
class KeyComparisonMixin:
    """Ajoute la capacité de comparaison via la propriété 'key'."""

    def __eq__(self, other: Any) -> bool:
        # On ignore l'erreur car mypy ne voit pas 'key' dans KeyComparisonMixin,
        # mais nous savons que l'héritage multiple l'apportera au runtime.
        # On utilise [attr-defined] pour être précis et ne pas masquer d'autres erreurs.
        return self.key == other.key  # type: ignore[attr-defined]

    def __lt__(self, other: Any) -> bool:
        return self.key < other.key  # type: ignore[attr-defined]


# --- Le reste du code reste identique ---
class Utilisateur:
    def __init__(self, id_num: int):
        self.id_num = id_num

    @property
    def key(self) -> int:
        return self.id_num


class SortableUser(KeyComparisonMixin, Utilisateur):
    pass


u = SortableUser(10)
print(u == u)  # True
```

### Pourquoi utiliser `type: ignore[attr-defined]` plutôt qu'un simple `type: ignore` ?

C'est un point crucial pour vos notes :

* **`# type: ignore` (La Masse) :** Si vous écrivez `return self.key + other.key # type: ignore`, et que vous vous
  trompez en écrivant `self.keey` (une faute de frappe), `mypy` ne vous préviendra pas. Il ignorera l'erreur de la faute
  de frappe car vous avez dit d'ignorer *toutes* les erreurs de la ligne.
* **`# type: ignore[attr-defined]` (Le Scalpel) :** Si vous faites la faute de frappe `self.keey`, `mypy` vous dira : *"
  Attention, l'erreur n'est pas 'attribut non défini', c'est 'attribut 'keey' inconnu'"*. Il ne vous ignorera que ce que
  vous lui avez explicitement demandé.

**Conclusion pour l'étudiant :**
En programmation professionnelle, on cherche souvent l'équilibre. On utilise le `type: ignore[attr-defined]` pour dire :
*"Je sais que l'architecture de mon design (Mixin + Héritage multiple) crée une situation que le linter ne peut pas
comprendre, mais je garantis que le code est correct."*

### Comparaison des stratégies de typage pour `mypy`

Si vous travaillez dans un projet avec des règles de typage très strictes, voici comment choisir votre méthode pour le
Mixin :

| Méthode                           | Syntaxe                                        | Avantages                                                 | Rigueur     | Inconvénients                                                                                      |
|:----------------------------------|:-----------------------------------------------|:----------------------------------------------------------|:------------|:---------------------------------------------------------------------------------------------------|
| **Type Hinting**                  | `def __eq__(self: KeyProvider, ...)`           | Très concis, très lisible.                                | Bonne       | Un peu "artificiel" pour `mypy` (on type l'argument `self`).                                       |
| **Type Narrowing** (La plus sûre) | `if isinstance(self, KeyProvider): ...`        | **La plus correcte**. Sécurise le runtime ET le statique. | Maximale    | Un peu plus verbeuse (ajoute un `if` dans le code).                                                |
| **La "Hacker" (Type Ignore)**     | `return self.key # type: ignore[attr-defined]` | **Optimale**                                              | **Moyenne** | On "ment" à `mypy` pour garder un code pur. Risque d' `AttributeError` si l'utilisateur se trompe. |

**Le conseil de l'architecte :**

- Pour des programmes ou des bibliothèques **critiques**, l'approche **Type Narrowing** (vérifier avec
  `isinstance` à l'intérieur de la méthode) est la meilleure pratique. Elle respecte le principe de "Fail Fast" : si
  vous
  essayez de mixer une classe qui ne possède pas de clé, le programme vous le dira explicitement avec une erreur claire,
  plutôt que de se comporter de manière imprévisible.
- Mais pour des projets plus simples ou moins critiques, l'approche **Type Hinting** est appropriée, même si
  l'utilisation d'un type sur `self`, surtout un type différent de la classe
  mixin, peut sembler un peu contradictoire.
- Si on ne veut pas de type sur `self`, et qu'on n'a pas besoin de la rigueur de `isinstance`, la directive à mypy 
  d'ignorer cette erreur d'attribut, qui n'est pas vraiment une erreur si on utilise le mixin correctement, peut être 
  acceptable.
