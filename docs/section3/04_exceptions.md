# Gestion des erreurs : Exceptions et Assertions

## Introduction

En Python, nous avons deux mécanismes principaux pour gérer les situations anormales :

1. **Les exceptions** : Pour gérer les erreurs prévisibles qui peuvent survenir pendant l'exécution
2. **Les assertions** (`assert`) : Pour vérifier des conditions qui ne devraient jamais échouer dans un code correct

Avec l'introduction des *Type Hints* (indices de type), nous pouvons réduire la duplication de code en laissant les
vérifications de type à l'analyseur statique (comme mypy) tout en utilisant `assert` et `raise` pour des vérifications
plus spécifiques.

## 1. Gestion des exceptions

### Concepts de base

Les *Type Hints* documentent les types attendus, tandis que les exceptions gèrent les cas d'erreur à l'exécution.

```python
def lire_fichier(nom_fichier: str) -> str:
    try:
        with open(nom_fichier, 'r') as f:
            contenu = f.read()
        return contenu
    except FileNotFoundError:
        print(f"Erreur: Le fichier {nom_fichier} n'existe pas")
        raise  # Ré-élève l'exception après traitement
    except PermissionError:
        print(f"Erreur: Permission insuffisante pour lire {nom_fichier}")
        raise
    except Exception as e:
        print(f"Une erreur inattendue s'est produite: {e}")
        raise


# Utilisation avec vérification statique
try:
    contenu = lire_fichier("fichier.txt")
except FileNotFoundError:
    print("Gérer l'absence de fichier...")
```

### Exceptions personnalisées

```python
class AgeInvalideError(ValueError):
    """Exception levée lorsque l'âge est invalide."""

    def __init__(self, age: int | float, message: str = "L'âge doit être un entier positif"):
        self.age = age
        super().__init__(message)


class Personne:
    def __init__(self, nom: str, age: int):
        # Les vérifications de type sont faites par mypy
        self.nom = nom  # Utilise le setter pour valider
        self.age = age

    @property
    def nom(self) -> str:
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
        return self._age

    @age.setter
    def age(self, valeur: int) -> None:
        """Définie l'âge avec validation."""
        if valeur < 0:
            raise AgeInvalideError(valeur)
        self._age = valeur


# Utilisation avec vérification statique et à l'exécution
try:
    p = Personne("Alice", -5)  # mypy détectera que -5 n'est pas un int positif
except AgeInvalideError as e:
    print(f"Erreur: {e} (âge: {e.age})")
```

## 2. Assertions (`assert`)

### Concepts de base

Les assertions sont utilisées pour vérifier des conditions qui ne devraient jamais échouer dans un code correct, en
complément des vérifications de type.

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
    # mypy vérifie que notes est bien une list[float]
    assert len(notes) > 0, "La liste ne peut pas être vide"

    for note in notes:
        if not (0 <= note <= 20):
            raise ValueError(f"Note {note} en dehors de l'intervalle [0, 20]")

    return sum(notes) / len(notes)


# Utilisation
print(calculer_moyenne([15.0, 18.0, 20.0]))  # Affiche 17.666...
try:
    calculer_moyenne([])  # Lève AssertionError (détecté à l'exécution)
except AssertionError as e:
    print(f"Erreur: {e}")
```

### Validation des invariants avec assertions

```python
class CompteBancaire:
    def __init__(self, titulaire: str, solde: float = 0.0):
        self.titulaire = titulaire
        self.solde = solde

    @property
    def solde(self) -> float:
        return self._solde

    @solde.setter
    def solde(self, valeur: float) -> None:
        assert valeur >= 0,"Le solde ne peut pas être négatif"
        self._solde = float(valeur)

    def retirer(self, montant: float) -> float:
        """Retire un montant du compte.

        Args:
            montant: Montant à retirer (doit être positif)

        Returns:
            Nouveau solde

        Raises:
            AssertionError: Si le montant est invalide ou si le solde est insuffisant
        """
        assert montant > 0, "Le montant doit être positif"
        assert self.solde >= montant, "Solde insuffisant"

        self.solde -= montant
        return self.solde


# Utilisation
compte = CompteBancaire("Alice", 1000.0)
print(compte.retirer(500.0))  # Affiche 500.0

try:
    compte.retirer(-100.0)  # Lève AssertionError (montant invalide)
except AssertionError as e:
    print(f"Erreur: {e}")
```

## 3. Comparaison : `assert` vs `if` avec `raise`

### Quand utiliser `assert`?

Les assertions sont appropriées pour :

1. **Vérifier les invariants** (conditions qui doivent toujours être vraies dans un code correct)
   ```python
    @solde.setter
    def solde(self, valeur: float) -> None:
        assert valeur >= 0,"Le solde ne peut pas être négatif"
        self._solde = float(valeur)
   ```

2. **Documenter les hypothèses** du code pour les autres développeurs

3. **Détecter les erreurs logiques** pendant le développement (les assertions peuvent être désactivées en production)

### Quand utiliser `if` avec `raise`?

Les vérifications avec `if` et `raise` sont appropriées pour :

1. **Gérer les erreurs prévisibles** qui peuvent survenir dans un code correct
   ```python
   def lire_fichier(nom: str) -> str:
       """Lit le contenu d'un fichier."""
       if not os.path.exists(nom):
           raise FileNotFoundError(f"Fichier {nom} introuvable")
       # ... traitement ...
   ```

2. **Valider les entrées utilisateur** ou les données externes

3. **Gérer les cas d'erreur qui doivent être traités en production**

### Exemple comparatif

```python
class Personne:
    def __init__(self, nom: str, age: int):
        # Les vérifications de type sont faites par mypy
        self.nom = nom  # Utilise le setter pour valider
        self.age = age

    @property
    def nom(self) -> str:
        """Retourne le nom de la personne."""
        return self._nom

    @nom.setter
    def nom(self, valeur: str) -> None:
        """Définie le nom avec validation."""
        # mypy vérifie que valeur est une str
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
        # mypy vérifie que valeur est un int
        if valeur < 0:
            raise ValueError("L'âge doit être positif")
        self._age = valeur

    def saluer(self) -> str:
        """Retourne un message de salutation.

        Raises:
            RuntimeError: Si l'objet n'est pas correctement initialisé
        """
        # Assertion pour vérifier l'état interne (ne devrait jamais échouer)
        assert hasattr(self, '_nom') and hasattr(self, '_age'), "Objet mal initialisé"

        return f"Bonjour, je m'appelle {self.nom} et j'ai {self.age} ans."


# Utilisation
try:
    p = Personne("Alice", 30)
    print(p.saluer())

    # Ces lignes lèveront des exceptions différentes
    Personne("", -5)  # mypy détectera que -5 n'est pas un int positif
except Exception as e:
    print(f"Erreur: {e}")

try:
    Personne("Bob", "trente")  # mypy détectera que "trente" n'est pas un int
except Exception as e:
    print(f"Erreur: {e}")
```

### Points clés à retenir

1. **Les assertions** :
    - Sont désactivables avec l'option `-O` de Python (`python -O script.py`)
    - Ne doivent pas être utilisées pour gérer les erreurs d'entrée utilisateur
    - Doivent documenter des conditions qui ne devraient jamais échouer dans un code correct

2. **Les vérifications avec `if/raise`** :
    - Doivent toujours être activées en production
    - Sont appropriées pour gérer les erreurs prévisibles
    - Doivent être utilisées pour valider les entrées externes

3. **Complémentarité avec les Type Hints** :
    - Les *Type Hints* documentent les types attendus (vérifiés par mypy)
    - Les assertions vérifient des conditions logiques à l'exécution
    - Les exceptions gèrent les cas d'erreur prévisibles

## 4. Bonnes pratiques

### a) Combinaison des trois approches

```python
from typing import Sequence


def calculer_statistiques(donnees: Sequence[float]) -> tuple[float, float]:
    """Calcule la moyenne et l'écart-type d'une séquence de nombres.

    Args:
        donnees: Séquence de nombres (doivent être entre 0 et 100)

    Returns:
        Tuple contenant (moyenne, écart-type)

    Raises:
        ValueError: Si les données sont invalides
    """
    # mypy vérifie que donnees est une Sequence[float]
    assert len(donnees) > 1, "Il faut au moins deux valeurs pour calculer l'écart-type"

    for valeur in donnees:
        if not (0 <= valeur <= 100):
            raise ValueError(f"Valeur {valeur} en dehors de l'intervalle [0, 100]")

    moyenne = sum(donnees) / len(donnees)

    # Assertion pour vérifier le résultat
    assert 0 <= moyenne <= 100, "La moyenne est en dehors des limites attendues"

    variance = sum((x - moyenne) ** 2 for x in donnees) / len(donnees)
    ecart_type = variance ** 0.5

    return moyenne, ecart_type


# Utilisation
print(calculer_statistiques([85.0, 90.0, 78.0]))  # Affiche (84.33..., 6.21...)
```

### b) Messages d'erreur descriptifs

```python
def convertir_temperature(valeur: float, unite: str) -> float:
    """Convertit une température entre Celsius et Fahrenheit.

    Args:
        valeur: Valeur numérique de la température
        unite: Unité ('C' pour Celsius, 'F' pour Fahrenheit)

    Returns:
        Température convertie

    Raises:
        ValueError: Si l'unité est invalide
    """
    assert unite in ('C', 'F'), f"Unité invalide: {unite}. Doit être 'C' ou 'F'"

    if unite == 'C':
        return (valeur * 9 / 5) + 32
    else:
        return (valeur - 32) * 5 / 9


# Utilisation
print(convertir_temperature(100.0, 'C'))  # Affiche 212.0
```

### c) Désactiver les assertions en production

```bash
# En développement (assertions activées)
python mon_script.py

# En production (assertions désactivées)
python -O mon_script.py
```

## 5. Exercices pratiques

### Exercice 1 : Gestionnaire de fichiers

Créez une classe `FichierManager` qui :

- Utilise des assertions pour vérifier l'état interne
- Utilise des vérifications avec `if/raise` pour gérer les erreurs d'entrée
- Implémente des méthodes pour lire et écrire des fichiers

```python
class FichierManager:
    def __init__(self, chemin: str):
        self.chemin = chemin
        self._est_ouvert = False

    @property
    def chemin(self) -> str:
        return self._chemin

    @chemin.setter
    def chemin(self, valeur: str) -> None:
        if not isinstance(valeur, str) or len(valeur.strip()) == 0:
            raise ValueError("Le chemin doit être une chaîne non vide")
        self._chemin = valeur.strip()

    def ouvrir(self) -> None:
        """Ouvre le fichier."""
        assert not self._est_ouvert, "Le fichier est déjà ouvert"
        # ... implémentation ...
        self._est_ouvert = True

    def fermer(self) -> None:
        """Fermer le fichier."""
        assert self._est_ouvert, "Le fichier n'est pas ouvert"
        # ... implémentation ...
        self._est_ouvert = False
```

### Exercice 2 : Calculatrice scientifique

Créez une classe `Calculatrice` qui :

- Utilise des assertions pour vérifier les invariants mathématiques
- Utilise des vérifications avec `if/raise` pour gérer les erreurs d'entrée utilisateur
- Implémente des méthodes pour calculer des fonctions trigonométriques, logarithmes, etc.

```python
import math


class Calculatrice:
    @staticmethod
    def sinus(valeur: float) -> float:
        """Calcule le sinus d'une valeur en radians."""
        assert isinstance(valeur, (int, float)), "La valeur doit être numérique"
        return math.sin(valeur)

    @staticmethod
    def logarithme(valeur: float, base: float = math.e) -> float:
        """Calcule le logarithme d'une valeur.

        Args:
            valeur: Valeur positive
            base: Base du logarithme (doit être > 0 et ≠ 1)

        Returns:
            Logarithme de la valeur

        Raises:
            ValueError: Si les arguments sont invalides
        """
        if valeur <= 0:
            raise ValueError("La valeur doit être positive")
        if base <= 0 or base == 1:
            raise ValueError("La base doit être > 0 et ≠ 1")

        return math.log(valeur, base)
```

### Exercice 3 : Système de réservation

Créez un système de réservation simple qui :

- Utilise des assertions pour vérifier l'état interne du système
- Utilise des vérifications avec `if/raise` pour gérer les erreurs d'entrée utilisateur
- Implémente des méthodes pour réserver, annuler et lister les réservations

```python
from datetime import datetime
from typing import Dict, List


class SystemeReservation:
    def __init__(self):
        self._reservations: Dict[str, List[datetime]] = {}

    def reserver(self, client_id: str, date: datetime) -> None:
        """Réserve une place pour un client à une date donnée.

        Args:
            client_id: Identifiant du client
            date: Date de la réservation

        Raises:
            ValueError: Si la date est dans le passé ou déjà réservée
        """
        assert isinstance(client_id, str), "L'identifiant doit être une chaîne"
        assert isinstance(date, datetime), "La date doit être un objet datetime"

        if date < datetime.now():
            raise ValueError("Ne peut pas réserver une date dans le passé")
        if client_id in self._reservations and date in self._reservations[client_id]:
            raise ValueError("Cette réservation existe déjà")

        if client_id not in self._reservations:
            self._reservations[client_id] = []
        self._reservations[client_id].append(date)

    def annuler(self, client_id: str, date: datetime) -> None:
        """Annule une réservation.

        Args:
            client_id: Identifiant du client
            date: Date de la réservation à annuler

        Raises:
            ValueError: Si la réservation n'existe pas
        """
        assert isinstance(client_id, str), "L'identifiant doit être une chaîne"
        assert isinstance(date, datetime), "La date doit être un objet datetime"

        if client_id not in self._reservations or date not in self._reservations[client_id]:
            raise ValueError("Cette réservation n'existe pas")

        self._reservations[client_id].remove(date)
```

## Conclusion

Avec l'introduction des *Type Hints*, nous pouvons optimiser notre gestion des erreurs en :

1. **Documentant les types attendus** avec les *Type Hints* (vérifiés par mypy)
2. **Utilisant des assertions** pour vérifier les invariants logiques
3. **Gérant les cas d'erreur prévisibles** avec `if/raise`

Cette approche réduit la duplication de code tout en maintenant un haut niveau de robustesse et de lisibilité.

**Règles mémo-techniques :**

- Les *Type Hints* documentent les types (vérifiés par mypy)
- Les assertions vérifient les invariants logiques (à l'exécution)
- Les exceptions gèrent les cas d'erreur prévisibles
- Ne dupliquez pas les vérifications de type avec `isinstance`