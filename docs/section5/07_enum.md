# Les Énumérations (Enums) en Python

En Python, les énumérations (ou **enums**) permettent de regrouper un ensemble de **constantes nommées** sous un type
unique. Elles améliorent la lisibilité du code et la sécurité en remplaçant les valeurs brutes (*magic numbers* ou
chaînes de caractères volantes).

Depuis Python 3.4, elles sont intégrées nativement via le module standard `enum`.

## 1. Syntaxe de base et propriétés

Pour créer une énumération, on définit une classe qui hérite de `Enum`. Par convention, les membres s'écrivent en
majuscules.

```python
from enum import Enum


class StatutCommande(Enum):
    EN_ATTENTE = 1
    EXPEDIEE = 2
    LIVREE = 3
    ANNULEE = 4
```

Chaque membre possède deux propriétés fondamentales : un **nom** (`.name`) et une **valeur** (`.value`).

```python
statut = StatutCommande.EXPEDIEE

print(statut)  # StatutCommande.EXPEDIEE
print(statut.name)  # EXPEDIEE
print(statut.value)  # 2
```

---

## 2. Manipulation des Enums### Recherche et accèsIl existe trois façons d'accéder à un membre :

* **Par attribut (direct) :** `StatutCommande.LIVREE`
* **Par valeur :** `StatutCommande(3)` *(Idéal pour lire une donnée brute depuis une base de données)*
* **Par nom :** `StatutCommande['LIVREE']` *(Idéal pour parser un dictionnaire ou un JSON)*

### Itération et comparaisonLes énumérations se prêtent naturellement aux boucles et aux structures de contrôle :

```python
# Boucler sur tous les membres
for statut in StatutCommande:
    print(statut.name)

# Comparaison d'identité (recommandée)
if statut is StatutCommande.EXPEDIEE:
    print("Le colis est en route !")
```

---

## 3. Utilisation moderne avec `match / case` (Python 3.10+)

La combinaison des Enums avec le filtrage de motifs (*pattern matching*) élimine les longues suites de `if/elif/else` et
centralise la logique métier de manière propre et sécurisée.

```python
def gerer_notification(statut: StatutCommande) -> str:
    match statut:
        case StatutCommande.EN_ATTENTE:
            return "⏳ Votre commande est validée. Préparation en cours."

        case StatutCommande.EXPEDIEE:
            return "🚚 Bonne nouvelle ! Votre colis a été remis au transporteur."

        case StatutCommande.LIVREE:
            return "🎉 Le colis a été déposé dans votre boîte aux lettres."

        case StatutCommande.ANNULEE:
            return "❌ Votre commande a bien été annulée et remboursée."

        case _:
            return "❓ Statut inconnu."


# Exemple d'utilisation :
# Conversion d'une valeur API (ex: 3) en Enum puis traitement
statut_recu = StatutCommande(3)
print(gerer_notification(statut_recu))
# Sortie : 🎉 Le colis a été déposé dans votre boîte aux lettres.
```

### Avantages pédagogiques :* **Sécurité :**

Contrairement à un `match` sur des chaînes de caractères brutes (ex:
`"expediee"`), l'utilisation de l'Enum évite les bugs liés aux fautes de frappe ou de casse.

* **Évolutivité :** Si un nouveau statut est ajouté dans l'Enum, le développeur sait exactement quelles structures
  `match` mettre à jour.

---

## 4. Fonctionnalités avancées

### L'attribution automatique (`auto`)

Si la valeur numérique exacte n'a pas d'importance, utilisez `auto()` pour générer des entiers incrémentiels
automatiquement.

```python
from enum import Enum, auto


class Couleur(Enum):
    ROUGE = auto()  # 1
    VERT = auto()  # 2
    BLEU = auto()  # 3
```

### Garantir l'unicité (`@unique`)

Par défaut, deux membres distincts peuvent partager la même valeur (le second devient un alias). Pour interdire cela et
lever une erreur en cas de doublon, utilisez le décorateur `@unique`.

```python
from enum import Enum, unique


@unique
class CodeErreur(Enum):
    NOT_FOUND = 404
    BAD_REQUEST = 400
    # DUP_FOUND = 404  <-- Lèvera une ValueError au chargement du script
```

### Énumérations typées spécifiques (Python 3.11+)

Python propose des variantes prêtes à l'emploi si vos énumérations doivent interagir directement avec des types de
base :

* **`StrEnum`** : Utile lorsque vos constantes sont des chaînes de caractères. Les membres héritent des méthodes de
  `str`.
* **`IntEnum`** : Permet de comparer directement le membre avec un entier (ex: `StatutCommande.EN_ATTENTE == 1`).

---

## 5. Les Énumérations de type `Flag` (Masques de bits)

Lorsque vos constantes ne sont pas mutuellement exclusives et qu'un élément peut posséder **plusieurs états en même
temps** (comme un système de permissions), on utilise `Flag`.

Derrière le décor, Python utilise des puissances de 2 (`1, 2, 4, 8...`) pour permettre des combinaisons binaires à
l'aide des opérateurs logiques (`|`, `&`).

```python
from enum import Flag, auto


class Permission(Flag):
    LECTURE = auto()  # 1 (0001 en binaire)
    ECRITURE = auto()  # 2 (0010 en binaire)
    EXECUTION = auto()  # 4 (0100 en binaire)
    MODIFICATION = auto()  # 8 (1000 en binaire)
```

### Opérations sur les drapeaux (`Flags`)

Vous pouvez combiner des permissions, vérifier la présence d'un droit ou en retirer grâce aux opérateurs binaires
standard :

```python
# 1. Combiner des permissions (Opérateur OU binaire : |)
droits_editeur = Permission.LECTURE | Permission.ECRITURE
print(droits_editeur)  # Permission.LECTURE|ECRITURE

# 2. Vérifier si une permission est incluse (Mot-clé : in)
a_le_droit_ecriture = Permission.ECRITURE in droits_editeur
print(a_le_droit_ecriture)  # True

# Note : On peut aussi utiliser l'opérateur ET binaire (&)
# ex: (droits_editeur & Permission.ECRITURE) == Permission.ECRITURE

# 3. Ajouter une permission
droits_editeur |= Permission.EXECUTION

# 4. Retirer une permission (Opérateur inversion ~ et ET &)
droits_editeur &= ~Permission.ECRITURE
```

!!! info "Astuce"
        Depuis Python 3.11, il existe aussi `IntFlag`. La différence est que `IntFlag` peut être
        comparé directement à des entiers bruts, et utilisé dans des calculs numériques, tandis que `Flag` reste strictement
        typé pour plus de sécurité.

## 6. Exercices Pratiques : Enums & Dataclasses

Ces exercices permettent de valider la bonne compréhension de la synergie entre les classes de données et les
énumérations.

---

### 📝 Exercice 1 : Gestion d'un inventaire de Véhicules (Niveau Débutant)

**Objectif :** Créer un modèle simple pour un garage automobile.

1. Créez une énumération `TypeVehicule` contenant trois membres : `VOITURE`, `MOTO` et `CAMION` (utilisez l'attribution
   automatique `auto`).
2. Créez une `@dataclass` nommée `Vehicule` avec les attributs suivants :
    * `marque` (chaîne de caractères)
    * `modele` (chaîne de caractères)
    * `categorie` (de type `TypeVehicule`)
    * `prix_journalier` (flottant)
3. Instanciez deux véhicules différents.
4. Écrivez une fonction `afficher_vehicule(v: Vehicule)` qui utilise un bloc `match/case` sur la catégorie du véhicule
   pour afficher un message personnalisé (ex: "🚗 Voiture : Peugeot 208 - 45.0€/jour").

---

### 📝 Exercice 2 : Système de Validation de Commandes (Niveau Intermédiaire)

**Objectif :** Manipuler le cycle de vie d'un objet, les valeurs par défaut et la méthode `__post_init__`.

1. Reprenez ou créez l'énumération `StatutCommande` avec les membres : `EN_ATTENTE`, `PAYEE`, `EXPEDIEE`.
2. Créez une `@dataclass` nommée `Commande` contenant :
    * `id_commande` (entier)
    * `articles` (une liste de chaînes de caractères. *Attention au piège des types mutables !*)
    * `montant_total` (flottant)
    * `statut` (de type `StatutCommande`, avec pour valeur par défaut `StatutCommande.EN_ATTENTE`)
3. Ajoutez une méthode `__post_init__(self)` à la dataclass pour lever une erreur (`ValueError`) si le `montant_total`
   est inférieur ou égal à 0.
4. Créez une méthode dans la classe (ou une fonction externe) permettant de faire passer le statut à `PAYEE`.

---

## 🛠️ Corrigés détaillés

### Corrigé de l'Exercice 1

```python
from enum import Enum, auto
from dataclasses import dataclass


# 1. Définition de l'Enum
class TypeVehicule(Enum):
    VOITURE = auto()
    MOTO = auto()
    CAMION = auto()


# 2. Définition de la Dataclass
@dataclass
class Vehicule:
    marque: str
    modele: str
    categorie: TypeVehicule
    prix_journalier: float


# 4. Fonction d'affichage avec match/case
def afficher_vehicule(v: Vehicule):
    match v.categorie:
        case TypeVehicule.VOITURE:
            print(f"🚗 Voiture : {v.marque} {v.modele} - {v.prix_journalier}€/jour")
        case TypeVehicule.MOTO:
            print(f"🏍️ Moto : {v.marque} {v.modele} - {v.prix_journalier}€/jour")
        case TypeVehicule.CAMION:
            print(f"🚛 Camion : {v.marque} {v.modele} - {v.prix_journalier}€/jour")
        case _:
            print(f"❓ Véhicule inconnu : {v.marque}")


# 3. Instanciation et tests
v1 = Vehicule("Peugeot", "208", TypeVehicule.VOITURE, 45.0)
v2 = Vehicule("Yamaha", "MT-07", TypeVehicule.MOTO, 35.0)

afficher_vehicule(v1)
# Sortie : 🚗 Voiture : Peugeot 208 - 45.0€/jour
afficher_vehicule(v2)
# Sortie : 🏍️ Moto : Yamaha MT-07 - 35.0€/jour
```

---

### Corrigé de l'Exercice 2

```python
from enum import Enum
from dataclasses import dataclass, field


class StatutCommande(Enum):
    EN_ATTENTE = 1
    PAYEE = 2
    EXPEDIEE = 3


@dataclass
class Commande:
    id_commande: int
    montant_total: float
    # Utilisation obligatoire de default_factory pour éviter le partage de la liste entre instances
    articles: list[str] = field(default_factory=list)
    # Le champ avec valeur par défaut doit être placé après les champs sans valeur par défaut
    statut: StatutCommande = StatutCommande.EN_ATTENTE

    def __post_init__(self):
        # Validation des données après la création de l'instance
        if self.montant_total <= 0:
            raise ValueError("Le montant total d'une commande doit être strictement positif.")

    def encaisser(self):
        """Modifie le statut de la commande si elle est en attente."""
        if self.statut is StatutCommande.EN_ATTENTE:
            self.statut = StatutCommande.PAYEE
            print(f"💳 Commande #{self.id_commande} payée avec succès.")
        else:
            print(f"⚠️ Impossible d'encaisser : la commande est au statut {self.statut.name}.")


# --- Tests du système ---

# 1. Test d'une commande valide
cmd1 = Commande(id_commande=101, montant_total=89.99, articles=["Livre Python", "Clé USB"])
print(cmd1)
# Sortie : Commande(id_commande=101, montant_total=89.99, articles=['Livre Python', 'Clé USB'], statut=StatutCommande.EN_ATTENTE)

# 2. Test du changement d'état
cmd1.encaisser()  # Modifie le statut à PAYEE
print(cmd1.statut)  # Sortie : StatutCommande.PAYEE

# 3. Test de la validation (__post_init__)
try:
    cmd_invalide = Commande(id_commande=102, montant_total=-5.0)
except ValueError as e:
    print(f"Erreur interceptée : {e}")
    # Sortie : Erreur interceptée : Le montant total d'une commande doit être strictement positif.
```
