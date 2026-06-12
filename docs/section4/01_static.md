# Attributs et méthodes de classe et méthodes statiques

## Introduction

En Python, il existe plusieurs types d'attributs et de méthodes qui peuvent être associés à une classe. Comprendre ces
différences est crucial pour écrire du code bien structuré et efficace. Ce guide couvre :

1. Les attributs de classe vs. les attributs d'instance
2. Les méthodes statiques vs. les méthodes de classe vs. les méthodes d'instance

## 1. Attributs de classe vs. Attributs d'instance

### Attributs d'instance

Les attributs d'instance sont spécifiques à chaque objet (instance) de la classe.

```python
class Personne:
    def __init__(self, nom):
        self.nom = nom  # Attribut d'instance


p1 = Personne("Alice")
p2 = Personne("Bob")

print(p1.nom)  # "Alice"
print(p2.nom)  # "Bob"

# Chaque instance a son propre attribut
p1.nom = "Alice Smith"  # Ne modifie que p1
print(p1.nom)  # "Alice Smith"
print(p2.nom)  # "Bob" (inchangé)
```

**Caractéristiques :**

- Créés dans `__init__` ou d'autres méthodes avec `self.`
- Uniques à chaque instance
- Modifiés indépendamment pour chaque instance

### Attributs de classe

Les attributs de classe sont partagés par toutes les instances de la classe.

```python
class Personne:
    espece = "Humain"  # Attribut de classe


p1 = Personne()
p2 = Personne()

print(p1.espece)  # "Humain"
print(p2.espece)  # "Humain"

# Modification via la classe affecte toutes les instances
Personne.espece = "Humain moderne"
print(p1.espece)  # "Humain moderne"
print(p2.espece)  # "Humain moderne"

# Accès via l'instance est possible mais déconseillé
p1.espece = "Alien"  # Crée un nouvel attribut d'instance
print(p1.espece)  # "Alien" (seulement pour p1)
print(p2.espece)  # "Humain moderne" (toujours l'attribut de classe)
```

**Caractéristiques :**

- Définis directement dans la classe
- Partagés par toutes les instances
- Modifiés via `Classe.attribut`
- Peut être accédé via `instance.attribut` mais cela peut créer des attributs d'instance

### Quand utiliser chacun ?

| Type                | Utilisation recommandée                                  |
|---------------------|----------------------------------------------------------|
| Attribut d'instance | Données spécifiques à chaque objet (nom, âge, etc.)      |
| Attribut de classe  | Constantes ou données partagées par toutes les instances |

## 2. Méthodes statiques vs. méthodes de classe vs. méthodes d'instance

### Méthodes d'instance (les plus courantes)

Les méthodes d'instance sont liées à une instance spécifique et reçoivent `self` comme premier argument.

```python
class Personne:
    def __init__(self, nom):
        self.nom = nom

    def saluer(self):  # Méthode d'instance
        return f"Bonjour, je m'appelle {self.nom}"


p = Personne("Alice")
print(p.saluer())  # "Bonjour, je m'appelle Alice"
```

**Caractéristiques :**

- Reçoivent `self` comme premier argument
- Peuvent accéder et modifier les attributs d'instance
- Doivent être appelées sur une instance

### Méthodes de classe (`@classmethod`)

Les méthodes de classe sont liées à la classe plutôt qu'à une instance. Elles reçoivent `cls` (la classe) comme premier
argument.

```python
class Personne:
    espece = "Humain"

    @classmethod
    def de_classe(cls):  # Méthode de classe
        return f"Je suis une méthode de {cls.__name__}"

    @classmethod
    def creer_depuis_chaine(cls, chaine: str):
        """Crée une instance à partir d'une chaîne."""
        nom = chaine.split()[0]
        return cls(nom)


print(Personne.de_classe())  # "Je suis une méthode de Personne"
p = Personne.creer_depuis_chaine("Alice Smith")
print(p.nom)  # "Alice"
```

**Caractéristiques :**

- Reçoivent `cls` comme premier argument
- Peuvent accéder aux attributs et méthodes de classe
- Peut créer des instances (`cls()`)
- Doivent être appelées sur la classe ou l'instance

### Méthodes statiques (`@staticmethod`)

Les méthodes statiques ne sont pas liées à la classe ou à l'instance. Elles ne reçoivent aucun argument spécial.

```python
class MathUtils:
    @staticmethod
    def additionner(a, b):  # Méthode statique
        return a + b

    @staticmethod
    def est_pair(nombre):
        return nombre % 2 == 0


print(MathUtils.additionner(5, 3))  # 8
print(MathUtils.est_pair(4))  # True
```

**Caractéristiques :**

- Ne reçoivent pas `self` ou `cls`
- Ne peuvent pas accéder aux attributs/méthodes de classe ou d'instance
- Doivent être appelées sur la classe (mais peuvent aussi être appelées sur une instance)
- Utiles pour les fonctions utilitaires liées à la classe

### Quand utiliser chaque type ?

| Type               | Utilisation recommandée                                                                   |
|--------------------|-------------------------------------------------------------------------------------------|
| Méthode d'instance | Opérations qui dépendent de l'état spécifique d'une instance                              |
| Méthode de classe  | Factories, méthodes qui opèrent sur la classe plutôt que les instances                    |
| Méthode statique   | Fonctions utilitaires liées à la classe mais n'ayant pas besoin d'accéder à ses attributs |

## Exemple complet illustrant toutes les différences

```python
class CompteBancaire:
    # Attribut de classe
    taux_interet = 0.01

    def __init__(self, titulaire, solde=0):
        # Attributs d'instance
        self.titulaire = titulaire
        self.solde = solde
        self._historique = []  # Attribut privé d'instance

    # Méthode d'instance
    def deposer(self, montant):
        """Ajoute au solde."""
        if montant > 0:
            self.solde += montant
            self._historique.append(f"Déposit de {montant}")
            return True
        return False

    # Méthode d'instance
    def retirer(self, montant):
        """Retire du solde si disponible."""
        if 0 < montant <= self.solde:
            self.solde -= montant
            self._historique.append(f"Retrait de {montant}")
            return True
        return False

    # Méthode d'instance
    def afficher_historique(self):
        """Affiche l'historique des transactions."""
        print("Historique pour", self.titulaire)
        for transaction in self._historique:
            print(f"- {transaction}")

    @classmethod
    def taux_interet_annuel(cls):
        """Retourne le taux d'intérêt annuel."""
        return cls.taux_interet * 100

    @classmethod
    def creer_compte_vide(cls, titulaire):
        """Crée un compte avec solde initial de 0."""
        return cls(titulaire)

    @staticmethod
    def valider_iban(iban):
        """Valide un numéro IBAN (simplifié)."""
        if not isinstance(iban, str) or len(iban) < 15:
            return False
        # Logique de validation simplifiée
        return True


# Utilisation des différentes méthodes et attributs
print("Taux d'intérêt annuel:", CompteBancaire.taux_interet_annuel(), "%")

compte1 = CompteBancaire("Alice", 1000)
compte2 = CompteBancaire.creer_compte_vide("Bob")  # Utilisation de la méthode de classe

compte1.deposer(500)  # Méthode d'instance
compte1.retirer(200)

print(f"Solde d'Alice: {compte1.solde}")  # Solde d'Alice: 1300

# Modification de l'attribut de classe affecte tous les comptes
CompteBancaire.taux_interet = 0.02
print("Nouveau taux:", CompteBancaire.taux_interet_annuel(), "%")  # Nouveau taux: 2.0 %

compte1.afficher_historique()
# Historique pour Alice
# - Déposit de 500
# - Retrait de 200

print("IBAN valide?", CompteBancaire.valider_iban("FR7630001007941234567890185"))  # True
```

## Bonnes pratiques et pièges à éviter

### 1. Modification des attributs de classe via les instances

```python
class MaClasse:
    compteur = 0


# Mauvais : crée un nouvel attribut d'instance
instance = MaClasse()
instance.compteur = 5
print(MaClasse.compteur)  # 0 (inchangé)

# Bon : modification via la classe
MaClasse.compteur += 1
print(MaClasse.compteur)  # 1
```

### 2. Utilisation appropriée des méthodes statiques

```python
class Calculatrice:
    @staticmethod
    def additionner(a, b):
        return a + b


# Correct : appel sur la classe
resultat = Calculatrice.additionner(5, 3)

# Également correct mais déconseillé : appel sur une instance
calc = Calculatrice()
resultat = calc.additionner(5, 3)  # Fonctionne mais peut prêter à confusion
```

### 3. Méthodes de classe pour les factories

```python
class Date:
    def __init__(self, jour, mois, annee):
        self.jour = jour
        self.mois = mois
        self.annee = annee

    @classmethod
    def depuis_chaine(cls, chaine):
        """Crée une instance à partir d'une chaîne au format JJ/MM/AAAA."""
        jour, mois, annee = map(int, chaine.split('/'))
        return cls(jour, mois, annee)


# Utilisation
date1 = Date(15, 6, 2023)
date2 = Date.depuis_chaine("15/06/2023")  # Plus lisible que Date("15/06/2023")
```

### 4. Accès aux attributs de classe dans les méthodes d'instance

```python
class MaClasse:
    constante = "Valeur"

    def __init__(self):
        self.instance_attr = "Autre valeur"

    def afficher(self):
        # Accès à l'attribut de classe
        print("Constante:", self.constante)  # Correct

        # Accès à l'attribut d'instance
        print("Instance:", self.instance_attr)  # Correct

        # Modification de l'attribut de classe (affecte toutes les instances)
        MaClasse.constante = "Nouvelle valeur"


# Utilisation
obj1 = MaClasse()
obj1.afficher()

obj2 = MaClasse()
print(obj2.constante)  # "Nouvelle valeur" (modifié par obj1)
```

## Exercices pratiques

### Exercice 1 : Gestionnaire de configuration

Créez une classe `Configuration` avec :

- Un attribut de classe `default_timeout` initialisé à 30
- Une méthode d'instance pour définir un timeout personnalisé
- Une méthode de classe pour réinitialiser tous les timeouts à la valeur par défaut
- Une méthode statique pour valider un timeout

### Exercice 2 : Système de forme géométrique

Créez une hiérarchie de classes pour représenter des formes géométriques :

- Classe de base `Forme` avec une méthode de classe pour créer une forme à partir d'une chaîne
- Sous-classes `Cercle`, `Rectangle` et `Triangle`
- Chaque sous-classe doit avoir :
    - Des attributs d'instance appropriés (rayon, côtés, etc.)
    - Une méthode d'instance pour calculer l'aire
    - Une méthode statique pour valider les dimensions

### Exercice 3 : Système de logging

Créez une classe `Logger` avec :

- Un attribut de classe `log_level` (DEBUG, INFO, WARNING, ERROR)
- Une méthode d'instance pour ajouter un message au log
- Une méthode de classe pour définir le niveau de log global
- Une méthode statique pour formater les messages

## Conclusion

Comprendre la différence entre :

- Attributs de classe et attributs d'instance
- Méthodes statiques, méthodes de classe et méthodes d'instance

est essentiel pour écrire du code Python bien structuré. Ces concepts permettent de :

1. **Partager des données** entre instances avec les attributs de classe
2. **Créer des factories** avec les méthodes de classe
3. **Organiser des fonctions utilitaires** avec les méthodes statiques
4. **Maintenir un état propre** pour chaque instance

En maîtrisant ces concepts, vous serez capable d'écrire des classes Python plus robustes et mieux organisées, ce qui
facilitera la maintenance et l'évolution de votre code.