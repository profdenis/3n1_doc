# **`match` avec Héritage**

Python 3.10+ introduit le mot-clé `match`, similaire à `switch` en Java/C++, mais plus puissant car il peut matcher des
**types d'objets** et leurs attributs.

---

## **Exemple avec `match` sur les Classes**

### **a) Matching de Types (Héritage)**

```python
def traiter_personne(personne):
    match personne:
        case Personne(nom, age):  # Match une instance de Personne
            print(f"Personne générale: {nom}, {age} ans")
        case Etudiant(nom, age, matiere):  # Match une instance d'Etudiant
            print(f"Étudiant en {matiere}: {nom}")
        case Professeur(nom, age, departement):  # Match une instance de Professeur
            print(f"Professeur de {departement}: {nom}")
        case _:  # Cas par défaut (comme "default")
            print("Type inconnu")


# Utilisation
p = Personne("Alice", 30)
e = Etudiant("Bob", 20, "Informatique")
prof = Professeur("Charlie", 45, "Mathématiques")

traiter_personne(p)  # "Personne générale: Alice, 30 ans"
traiter_personne(e)  # "Étudiant en Informatique: Bob"
traiter_personne(prof)  # "Professeur de Mathématiques: Charlie"
```

---

### **b) Matching avec Conditions Supplémentaires**

On peut ajouter des conditions après le `case` :

```python
def classifier_par_age(personne):
    match personne:
        case Personne(nom, age) if age < 18:
            print(f"{nom} est mineur")
        case Personne(nom, age) if age >= 65:
            print(f"{nom} est retraité")
        case Etudiant(nom, _, matiere) if "Informatique" in matiere:
            print(f"{nom} est un étudiant en tech!")
        case _:
            print("Cas par défaut")


classifier_par_age(Etudiant("Bob", 17, "Informatique"))  # "Bob est mineur"
classifier_par_age(Professeur("Charlie", 70, "Maths"))  # "Charlie est retraité"
```

---

### **c) Matching avec `isinstance()` (Alternative)**

Si vous préférez éviter le destructuring (`case Personne(nom, age)`), utilisez `isinstance` :

```python
def traiter_personne_alt(personne):
    match personne:
        case p if isinstance(p, Etudiant):
            print(f"Étudiant: {p.nom}, matière: {p.matiere_principale}")
        case p if isinstance(p, Professeur):
            print(f"Professeur: {p.nom}, département: {p.departement}")
        case _:
            print("Autre type")


traiter_personne_alt(e)  # "Étudiant: Bob, matière: Informatique"
```

---

## **Avantages du `match` avec l'Héritage**

- ✅ **Plus lisible** que des `if isinstance()` imbriqués.
- ✅ **Supporte le destructuring** (accès direct aux attributs).
- ✅ **Extensible** : Ajoutez facilement de nouveaux cas.

---

### **Conclusion**

Le `match` est un outil puissant pour gérer le polymorphisme de manière élégante. Il remplace avantageusement les
chaînes d'`if/elif` pour vérifier les types d'objets.

!!! note "📌 **Astuce**"
    Utilisez `case _:` comme "default" pour capturer tous les cas non matchés !