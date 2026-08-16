# **OO Python : Concepts de Base**

*Encapsulation, Constructeurs et Méthodes "Dunder"*

---

## **1. Introduction à la Classe `Personne`**

Voici une classe simple représentant une personne :

```python
class Personne:
    def __init__(self, nom, age):
        self.nom = nom
        self.age = age

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
```

### **a) Qu'est-ce que `self` ?**

En Python, `self` est le **premier paramètre des méthodes d'instance** :

- Il représente l'**objet courant**.
- Permet d'accéder aux attributs et méthodes de la classe.

### **b) Comparaison avec `this` en Java**

En Java, `this` est implicite, il ne faut pas le déclarer explicitement dans les signatures de méthodes, tandis que
`self` est obligatoire dans les signatures de méthodes d'instance en Python. Techniquement, on pourrait utiliser
n'importe quel identificateur valide pour désigner
l'objet courant, mais `self` est la convention la plus courante. Si vous utilisez autre chose que `self`, comme `abcd`
par exemple, le code fonctionnera correctement, mais il est plus facile de lire le code si vous utilisez `self`, car
c'est la convention la plus courante. Si vous utilisez autre chose que `self`, votre code aura de grandes chances d'être
rejeté par les développeurs Python.

### **c) Points Clés**

- En Python, `self` est **toujours le premier paramètre** pour les méthodes de classe.
- En Java, `this` peut être omis si le contexte est clair, mais il est souvent utilisé pour éviter les ambiguïtés.
- En Python, `self` est obligatoire pour référer aux attributs de l'objet courant.

!!! not "📌 **Astuce**"
    Pensez à `self` comme un "pointeur vers l'objet courant", similaire à `this` en Java !

---

## **2. Explication des Concepts**

### **a) Constructeur (`__init__`)**

- Méthode spéciale appelée lors de la création d'un objet.
- Initialise les attributs (`nom`, `age`).

```python
p = Personne("Alice", 30)
print(p.nom)  # "Alice"
print(p.age)  # 30
```

---

### **b) Encapsulation**

#### **Attributs Protégés (`_`)**

- Convention pour indiquer que l'attribut est **"interne"** à la classe.
- Accessible depuis l'extérieur, mais **à utiliser avec prudence**.
- Utilisé pour éviter les conflits de noms ou signaler une utilisation interne.

```python
class Personne:
    def __init__(self, nom):
        self._nom = nom  # Attribut protégé (convention)


p = Personne("Alice")
print(p._nom)  # "Alice" → Accessible, mais déconseillé en dehors de la classe
```

**Pourquoi l'utiliser ?**

- Permet aux sous-classes d'accéder à l'attribut.
- Moins strict que privé (`__`).

---

#### **Attributs Privés (`__`)**

- **Vraiment privés** : Python applique un **name mangling** (transformation de nom) pour les rendre difficiles à
  accéder.
- Utilisés pour une encapsulation stricte.

```python
class Personne:
    def __init__(self, nom):
        self.__nom = nom  # Attribut privé


p = Personne("Alice")
# print(p.__nom)  # ❌ AttributeError: 'Personne' object has no attribute '__nom'

# Accès forcé (déconseillé !)
print(p._Personne__nom)  # "Alice" → Name mangling
```

**Pourquoi l'utiliser ?**

- Empêche les modifications accidentelles depuis l'extérieur.
- Utile pour des données sensibles.

---

#### **Comparaison**

| Type        | Préfixe | Accessible depuis l'extérieur ? | Utilisation typique  |
|-------------|---------|---------------------------------|----------------------|
| **Public**  | Aucun   | Oui                             | Attributs principaux |
| **Protégé** | `_`     | Oui (mais déconseillé)          | Internes à la classe |
| **Privé**   | `__`    | Non (_name mangling_)           | Données sensibles    |

---

#### **Exemple Complet**

```python
class CompteBancaire:
    def __init__(self, titulaire, solde):
        self.titulaire = titulaire  # Public
        self._solde = solde  # Protégé (convention)
        self.__mot_de_passe = "1234"  # privé

    def afficher_solde(self):  # Méthode pour accéder au solde protégé
        return self._solde


compte = CompteBancaire("Alice", 1000)

print(compte.titulaire)  # "Alice" → Public
print(compte._solde)  # 1000 → Protégé (accessible, mais déconseillé)
# print(compte.__mot_de_passe)   # ❌ Erreur ! privé

# Accès forcé au privé (déconseillé)
print(compte._CompteBancaire__mot_de_passe)  # "1234" → Name mangling
```

!!! Note "Propriétés"
    Nous verrons plus tard comment mieux encapsuler les données sensibles en utilisant des propriétés et des méthodes
    spéciales. Les propriétés permettent de contrôler l'accès aux attributs privés et de personnaliser leur comportement
    lors de l'accès ou de la modification.

    Les propriétés sont des méthodes spéciales qui permettent de personnaliser l'accès aux attributs d'un objet. Elles sont
    définies en utilisant des décorateurs (`@property`, `@nom.setter`, `@nom.deleter`) et permettent de contrôler la
    lecture, l'écriture et la suppression des attributs.

    Pour l'instant, on se contente de couvrir les concepts de base. Python est un langage très permissif à la base, mais
    il existe des mécanismes pour construire des systèmes plus robustes et sécurisés.

---

#### **Bonnes Pratiques**

- ✅ **Préférez les attributs protégés (`_`)** pour une encapsulation souple.
- ✅ **Utilisez les privés (`__`)** uniquement pour des données critiques.
- ⚠️ **Évitez d'accéder directement aux attributs privés** (utilisez des méthodes).

---

### **c) Méthodes "Dunder" (Double Underscore)**

Ces méthodes sont des **méthodes spéciales** qui permettent de personnaliser le comportement des objets.

| Méthode    | Description                                        | Exemple                                            |
|------------|----------------------------------------------------|----------------------------------------------------|
| `__repr__` | Représentation officielle (pour les développeurs)  | `print(repr(p))` → `Personne(nom='Alice', age=30)` |
| `__str__`  | Représentation lisible (pour les utilisateurs)     | `print(str(p))` → "Bonjour, je m'appelle Alice..." |
| `__eq__`   | Égalité entre objets (`==`)                        | `p1 == p2` compare `nom` et `age`                  |
| `__hash__` | Hachage pour les dictionnaires/ensembles           | Permet d'utiliser `Personne` comme clé             |
| `__lt__`   | Comparaison (`<`). Utilisé par `sort` et `sorted`. | Ordonne par `(nom, age)`                           |
| `__gt__`   | Comparaison (`>`)                                  | Ordonne par `(nom, age)`                           |
| `__le__`   | Comparaison (`<=`)                                 | Ordonne par `(nom, age)`                           |
| `__ge__`   | Comparaison (`>=`)                                 | Ordonne par `(nom, age)`                           |
| `__ne__`   | Inégalité entre objets (`!=`)                      | `p1 != p2` compare `nom` et `age`                  |

---

## **3. Exemples Pratiques**

### **a) Utilisation de `__repr__` et `__str__`**

```python
p = Personne("Alice", 30)

# __str__ est appelé implicitement avec print()
print(p)  # "Bonjour, je m'appelle Alice..."

# __repr__ pour une représentation technique
print(repr(p))  # "Personne(nom='Alice', age=30)"
```

### **b) Comparaison d'objets (`__eq__`) pour l'égalité**

```python
p1 = Personne("Alice", 30)
p2 = Personne("Alice", 30)
p3 = Personne("Bob", 25)

print(p1 == p2)  # True (même nom et âge)
print(p1 == p3)  # False
```

### **c) Comparaison avec `__lt__` pour ordonner les objets**

```python
personnes = [Personne("Bob", 25), Personne("Alice", 30)]
personnes_triees = sorted(personnes)

for p in personnes_triees:
    print(p.nom)  # "Alice" puis "Bob"
```

---

## **4. Exercices**

### **Exercice 1 : Classe `Livre`**

Créez une classe `Livre` avec :

- Un constructeur (`__init__`) pour `titre`, `auteur`, et `annee`.
- Une méthode `afficher()` qui retourne `"Titre: [titre], Auteur: [auteur]"`.
- Implémentez `__repr__` et `__str__`.

**Exemple :**

```python
livre = Livre("1984", "George Orwell", 1949)
print(livre)  # "Titre: 1984, Auteur: George Orwell"
```

---

### **Exercice 2 : Classe `CompteBancaire`**

Créez une classe `CompteBancaire` avec :

- Un constructeur pour `titulaire` et `solde`.
- Une méthode `deposer(montant)`.
- Implémentez `__eq__` pour comparer les soldes.

**Exemple :**

```python
compte1 = CompteBancaire("Alice", 1000)
compte2 = CompteBancaire("Bob", 1000)
print(compte1 == compte2)  # True (même solde)
```

---

### **Exercice 3 : Classe `Etudiant`**

Créez une classe `Etudiant` avec :

- Un constructeur pour `nom`, `age`, et `notes` (liste).
- Une méthode `moyenne()` qui calcule la moyenne des notes.
- Implémentez `__lt__` pour trier par moyenne.

**Exemple :**

```python
etudiants = [Etudiant("Alice", 20, [85, 90]), Etudiant("Bob", 21, [78, 82])]
print(sorted(etudiants)[0].nom)  # "Bob" (moyenne plus basse)
```

---

### **Exercice 4 : Classe `Voiture`**

Créez une classe `Voiture` avec :

- Un attribut public `marque`.
- Un attribut protégé `_vitesse_max`.
- Un attribut privé `__kilométrage`.

```python
class Voiture:
    def __init__(self, marque):
        self.marque = marque
        self._vitesse_max = 200
        self.__kilométrage = 0

    def rouler(self, km):
        self.__kilométrage += km


voiture = Voiture("Toyota")
print(voiture.marque)  # "Toyota" → Public
print(voiture._vitesse_max)  # 200 → Protégé (accessible, mais déconseillé)
# print(voiture.__kilométrage)  # ❌ Erreur ! privé
```

---

## **5. Bonnes Pratiques**

- ✅ **Utilisez `__repr__` et `__str__`** pour une meilleure lisibilité.
- ✅ **Implémentez `__eq__` et `__hash__` ensemble** si vous voulez utiliser des objets comme clés dans un dictionnaire.
- ⚠️ **Évitez les attributs publics** (préférez `_attribut` ou `__attribut` pour indiquer "protégé" ou "privé").

---

### **Conclusion**

Ces concepts de base en POO permettent de :

- Créer des structures de données personnalisées.
- Contrôler l'accès aux attributs (encapsulation).
- Personnaliser le comportement des objets avec les méthodes "dunder".

📌 **Astuce** : Utilisez `dir(objet)` dans le REPL pour voir toutes les méthodes disponibles sur un objet !