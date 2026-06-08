# **Héritage et Polymorphisme**

*Exemple avec la classe `Personne`, et ses sous-classes `Etudiant` et `Professeur`*

---

## **1. Définition des Sous-Classes**

### **a) Classe `Etudiant` (héritage de `Personne`)**

```python
class Etudiant(Personne):
    def __init__(self, nom, age, matiere_principale):
        super().__init__(nom, age)  # Appel au constructeur parent
        self.matiere_principale = matriere_principale

    def saluer(self):  # Redéfinition (polymorphisme)
        return f"Bonjour, je suis {self.nom}, étudiant en {self.matiere_principale}!"

    def __str__(self):
        return self.saluer()  # Utilise la méthode redéfinie
```

### **b) Classe `Professeur` (héritage de `Personne`)**

```python
class Professeur(Personne):
    def __init__(self, nom, age, departement):
        super().__init__(nom, age)
        self.departement = departement

    def saluer(self):  # Redéfinition (polymorphisme)
        return f"Bonjour, je suis {self.nom}, professeur en {self.departement}!"

    def enseigner(self, matiere):
        return f"{self.nom} enseigne {matiere}."
```

---

## **2. Explication de l'Héritage**

- `Etudiant` et `Professeur` **héritent** de `Personne`.
- `super().__init__()` appelle le constructeur parent pour initialiser les attributs hérités (`nom`, `age`).

!!! Note "`super()`"
    N'oubliez pas les parenthèses lors de l'appel à `super()`, contrairement à Java, où `super` est un mot-clé. En python,
    `super()` est une fonction qui renvoie une instance de la classe parente, permettant d'appeler ses méthodes ou accéder à
    ses attributs.

```python
p = Personne("Alice", 30)
e = Etudiant("Bob", 20, "Informatique")
prof = Professeur("Charlie", 45, "Mathématiques")

print(p.saluer())  # "Bonjour, je m'appelle Alice et j'ai 30 ans."
print(e.saluer())  # "Bonjour, je suis Bob, étudiant en Informatique!"
print(prof.saluer())  # "Bonjour, je suis Charlie, professeur en Mathématiques!"
```

---

## **3. Polymorphisme : Redéfinition de Méthodes**

Le polymorphisme permet à une méthode d'avoir un **comportement différent selon la classe** :

- `saluer()` est redéfini dans `Etudiant` et `Professeur`.
- `__str__()` utilise la version redéfinie de `saluer()`.

```python
personnes = [p, e, prof]

for personne in personnes:
    print(personne)  # Appelle __str__, qui utilise saluer()
# Affiche :
# Bonjour, je m'appelle Alice et j'ai 30 ans.
# Bonjour, je suis Bob, étudiant en Informatique!
# Bonjour, je suis Charlie, professeur en Mathématiques!
```

---

## **4. Méthodes Spécifiques aux Sous-Classes**

Chaque sous-classe peut ajouter des méthodes propres :

```python
print(e.matiere_principale)  # "Informatique" (attribut d'Etudiant)
print(prof.enseigner("Python"))  # "Charlie enseigne Python." (méthode de Professeur)
```

---

## **5. Vérification du Type avec `isinstance()`**

Pour vérifier si un objet est une instance d'une classe :

```python
print(isinstance(e, Etudiant))  # True
print(isinstance(prof, Personne))  # True (héritage)
print(isinstance(p, Professeur))  # False
```

---

## **6. Résumé des Concepts**

| Concept                     | Explication                                                     |
|-----------------------------|-----------------------------------------------------------------|
| **Héritage**                | `Etudiant` et `Professeur` héritent de `Personne`.              |
| **Redéfinition (Override)** | `saluer()` est réimplémenté dans les sous-classes.              |
| **Polymorphisme**           | Une méthode peut avoir plusieurs comportements selon la classe. |
| **Méthodes spécifiques**    | Chaque sous-classe ajoute ses propres attributs/méthodes.       |

---

### **Conclusion**

L'héritage et le polymorphisme permettent de :

- **Réutiliser** du code (éviter la duplication).
- **Étendre** des classes existantes.
- **Personnaliser** le comportement selon les besoins.

!!! note "📌 **Astuce**"
    Utilisez `super()` pour appeler les méthodes du parent, surtout dans `__init__` !