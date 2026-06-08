# Définir des propriétés avec `@property`

## Introduction

Le décorateur `@property` est un outil puissant de Python qui permet de contrôler l'accès aux attributs d'une classe
comme s'ils étaient des attributs publics, tout en permettant une validation ou un traitement personnalisé. Il est
particulièrement utile pour :

1. **Encapsulation** : Protéger les données internes
2. **Validation** : Vérifier les valeurs avant affectation
3. **Calcul dynamique** : Calculer des valeurs à la demande
4. **Interface propre** : Offrir une API simple tout en gardant le contrôle

## Structure de base d'une propriété

Une propriété est composée de trois parties :

```python
class MaClasse:
    def __init__(self):
        self._mon_attribut = None  # Attribut privé (convention)

    @property
    def mon_attribut(self):  # Getter
        """Docstring pour le getter"""
        return self._mon_attribut

    @mon_attribut.setter
    def mon_attribut(self, valeur):  # Setter
        """Docstring pour le setter"""
        if not self._valider_valeur(valeur):
            raise ValueError("Valeur invalide")
        self._mon_attribut = valeur

    def _valider_valeur(self, valeur):
        """Méthode de validation interne"""
        return True  # À surcharger
```

## Exemple 1 : Classe Personne avec validation

Voici la classe `Personne` modifiée pour utiliser des propriétés :

```python
class Personne:
    def __init__(self, nom, age):
        self._nom = None
        self._age = None
        self.nom = nom  # Utilise le setter pour valider
        self.age = age

    @property
    def nom(self):
        """Retourne le nom de la personne."""
        return self._nom

    @nom.setter
    def nom(self, valeur):
        """Définie le nom avec validation."""
        if not isinstance(valeur, str):
            raise TypeError("Le nom doit être une chaîne de caractères")
        valeur = valeur.strip()
        if len(valeur) == 0:
            raise ValueError("Le nom ne peut pas être vide après suppression des espaces")
        self._nom = valeur

    @property
    def age(self):
        """Retourne l'âge de la personne."""
        return self._age

    @age.setter
    def age(self, valeur):
        """Définie l'âge avec validation."""
        if not isinstance(valeur, int) or valeur < 0:
            raise ValueError("L'âge doit être un entier positif")
        self._age = valeur

    def saluer(self):
        return f"Bonjour, je m'appelle {self.nom} et j'ai {self.age} ans."

    def __repr__(self):
        return f"Personne(nom='{self.nom}', age={self.age})"

    def __str__(self):
        return self.saluer()

    def __eq__(self, autre):
        if isinstance(autre, Personne):
            return self.nom == autre.nom and self.age == autre.age
        return False

    def __hash__(self):
        return hash((self.nom, self.age))

    def __lt__(self, autre):
        if isinstance(autre, Personne):
            return (self.nom, self.age) < (autre.nom, autre.age)
        return False


# Exemples d'utilisation
try:
    p1 = Personne("Alice", 30)
    print(p1.saluer())  # Bonjour, je m'appelle Alice et j'ai 30 ans.

    p2 = Personne("", -5)  # Va lever une exception pour le nom vide
except (ValueError, TypeError) as e:
    print(f"Erreur lors de la création: {e}")

try:
    p1.nom = "Bob"  # Modification valide
    p1.age = -10  # Va lever une exception
except ValueError as e:
    print(f"Erreur lors de la modification: {e}")  # L'âge doit être un entier positif

p1.age = 35  # Modification valide
print(p1)  # Bonjour, je m'appelle Bob et j'ai 35 ans.
```

### Points clés pour cet exemple :

1. **Validation du nom** :
    - Vérifie que c'est une chaîne de caractères
    - Supprime les espaces avec `strip()`
    - Vérifie que la longueur est > 0 après nettoyage

2. **Validation de l'âge** :
    - Doit être un entier (`int`)
    - Doit être positif (>= 0)

3. **Comportement lors des erreurs** :
    - Les exceptions sont levées immédiatement
    - L'objet reste dans un état cohérent (pas d'attributs partiellement définis)

## Exemple 2 : Classe Point avec validation

Voici l'exemple complet de la classe `Point` avec propriétés :

```python
class Point:
    def __init__(self, x=0, y=0):
        self._x = None
        self._y = None
        self.x = x  # Utilise le setter pour valider
        self.y = y

    @property
    def x(self):
        """Retourne la coordonnée x du point."""
        return self._x

    @x.setter
    def x(self, valeur):
        """Définie la coordonnée x avec validation."""
        if not isinstance(valeur, (int, float)):
            raise TypeError("La coordonnée x doit être un nombre")
        if valeur < 0:
            raise ValueError("La coordonnée x doit être positive ou nulle")
        self._x = float(valeur)  # On stocke toujours en float pour la cohérence

    @property
    def y(self):
        """Retourne la coordonnée y du point."""
        return self._y

    @y.setter
    def y(self, valeur):
        """Définie la coordonnée y avec validation."""
        if not isinstance(valeur, (int, float)):
            raise TypeError("La coordonnée y doit être un nombre")
        if valeur < 0:
            raise ValueError("La coordonnée y doit être positive ou nulle")
        self._y = float(valeur)

    def distance(self, autre_point):
        """Calcule la distance euclidienne entre deux points."""
        if not isinstance(autre_point, Point):
            raise TypeError("L'argument doit être un objet Point")
        return ((self.x - autre_point.x) ** 2 + (self.y - autre_point.y) ** 2) ** 0.5

    def __repr__(self):
        return f"Point(x={self.x}, y={self.y})"

    def __str__(self):
        return f"({self.x}, {self.y})"

    def __eq__(self, autre):
        if isinstance(autre, Point):
            return self.x == autre.x and self.y == autre.y
        return False


# Exemples d'utilisation
try:
    p1 = Point(3, 4)
    print(p1)  # (3.0, 4.0)

    p2 = Point(-1, 5)  # Va lever une exception pour x négatif
except ValueError as e:
    print(f"Erreur: {e}")  # La coordonnée x doit être positive ou nulle

p3 = Point(0, 0)
print(p3.distance(p1))  # 5.0 (distance entre (0,0) et (3,4))

# Modification des valeurs
try:
    p1.x = "cinq"  # Va lever une exception pour type incorrect
except TypeError as e:
    print(f"Erreur: {e}")  # La coordonnée x doit être un nombre

p1.y = 7.5  # Modification valide
print(p1)  # (3.0, 7.5)
```

### Points clés pour cet exemple :

1. **Validation des types** :
    - Accepte à la fois `int` et `float`
    - Convertit toujours en `float` pour la cohérence interne

2. **Validation des valeurs** :
    - Les coordonnées doivent être >= 0
    - Messages d'erreur descriptifs

3. **Méthodes supplémentaires** :
    - La méthode `distance()` montre comment utiliser les propriétés dans d'autres méthodes
    - Implémentation de `__repr__` et `__str__` pour une meilleure représentation

## Cas particuliers et bonnes pratiques

### 1. Propriétés en lecture seule

Pour créer une propriété accessible uniquement en lecture :

```python
class Rectangle:
    def __init__(self, largeur, hauteur):
        self._largeur = largeur
        self._hauteur = hauteur

    @property
    def aire(self):
        """Calcule l'aire du rectangle."""
        return self._largeur * self._hauteur


# Utilisation
r = Rectangle(5, 10)
print(r.aire)  # 50
# r.aire = 20  # Va lever une AttributeError
```

### 2. Propriétés calculées

Les propriétés peuvent calculer des valeurs dynamiquement :

```python
class Cercle:
    def __init__(self, rayon):
        self._rayon = rayon

    @property
    def rayon(self):
        return self._rayon

    @rayon.setter
    def rayon(self, valeur):
        if valeur < 0:
            raise ValueError("Le rayon doit être positif")
        self._rayon = valeur

    @property
    def diametre(self):
        """Retourne le diamètre (calculé à partir du rayon)."""
        return 2 * self._rayon

    @property
    def circonference(self):
        """Retourne la circonférence."""
        return 2 * 3.14159 * self._rayon


# Utilisation
c = Cercle(5)
print(c.diametre)  # 10 (calculé dynamiquement)
```

### 3. Gestion des exceptions personnalisées

Pour une meilleure gestion des erreurs :

```python
class InvalidAgeError(ValueError):
    """Exception levée lorsque l'âge est invalide."""
    pass


class InvalidNameError(ValueError):
    """Exception levée lorsque le nom est invalide."""
    pass


class Personne:
    # ... (même structure que précédemment) ...

    @nom.setter
    def nom(self, valeur):
        if not isinstance(valeur, str):
            raise TypeError("Le nom doit être une chaîne de caractères")
        valeur = valeur.strip()
        if len(valeur) == 0:
            raise InvalidNameError("Le nom ne peut pas être vide après suppression des espaces")
        self._nom = valeur

    @age.setter
    def age(self, valeur):
        if not isinstance(valeur, int) or valeur < 0:
            raise InvalidAgeError(f"L'âge doit être un entier positif (reçu: {valeur})")
        self._age = valeur


# Utilisation avec gestion d'exceptions spécifiques
try:
    p = Personne("", -5)
except InvalidNameError as e:
    print(f"Erreur de nom: {e}")
except InvalidAgeError as e:
    print(f"Erreur d'âge: {e}")
```

### 4. Propriétés avec valeurs par défaut

```python
class Configuration:
    def __init__(self):
        self._debug = False
        self._timeout = 30

    @property
    def debug(self):
        """Mode débogage."""
        return self._debug

    @debug.setter
    def debug(self, valeur):
        if not isinstance(valeur, bool):
            raise TypeError("Le mode debug doit être un booléen")
        self._debug = valeur

    @property
    def timeout(self):
        """Timeout en secondes."""
        return self._timeout

    @timeout.setter
    def timeout(self, valeur):
        if not isinstance(valeur, (int, float)) or valeur <= 0:
            raise ValueError("Le timeout doit être un nombre positif")
        self._timeout = float(valeur)


# Utilisation avec valeurs par défaut
config = Configuration()
print(config.debug)  # False (valeur par défaut)
print(config.timeout)  # 30.0 (valeur par défaut)
```

## Avantages des propriétés

1. **Encapsulation** : Protège les données internes contre les modifications incorrectes
2. **Flexibilité** : Permet de changer l'implémentation interne sans affecter le code client
3. **Validation** : Garantit que les objets restent dans un état valide
4. **Interface propre** : Offre une API simple et intuitive
5. **Documentation** : Les docstrings des propriétés apparaissent dans `help()` et les outils IDE

## Pièges à éviter

1. **Modification directe de l'attribut privé** :
   ```python
   p = Personne("Alice", 30)
   p._age = -5  # Contourne la validation ! (à éviter)
   ```

2. **Oublier le setter** :
   Si vous définissez un getter mais pas de setter, l'attribut devient en lecture seule.

3. **Performance** :
   Les propriétés calculées sont recalculées à chaque accès - évitez pour des calculs coûteux.

4. **Cohérence entre getter et setter** :
   Assurez-vous que le setter met toujours l'objet dans un état valide.

## Exercice pratique

1. Créez une classe `CompteBancaire` avec :
    - Un solde (doit être >= 0)
    - Un titulaire (ne peut pas être vide après strip())
    - Une méthode `deposer()` qui ajoute au solde
    - Une méthode `retirer()` qui soustrait du solde (ne peut pas dépasser le solde)

2. Créez une classe `Etudiant` avec :
    - Un nom (comme dans Personne)
    - Une liste de notes (doit être une liste d'entiers entre 0 et 20)
    - Une propriété calculée `moyenne` qui retourne la moyenne des notes

3. Modifiez la classe `Point` pour ajouter :
    - Une méthode `deplacer()` qui prend un autre Point comme argument
    - Une validation qui empêche le déplacement vers des coordonnées négatives

## Conclusion

Les propriétés sont un outil essentiel en Python pour créer des classes robustes et bien encapsulées. Elles permettent
de :

- Valider les données entrantes
- Calculer des valeurs dynamiquement
- Maintenir une interface propre tout en gardant le contrôle
- Documenter clairement l'API de la classe

En maîtrisant les propriétés, vous serez capable de créer des classes Python plus professionnelles et sûres.