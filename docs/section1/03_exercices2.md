# Exercices 2

### **Exercices sur les Listes**

#### **1. Manipulation de liste simple**

Écrivez un programme qui :

- Crée une liste `nombres = [5, 2, 8, 1, 9]`.
- Affiche la longueur de la liste.
- Ajoute le nombre `3` à la fin.
- Trie la liste par ordre croissant.

**Exemple :**

```
Longueur : 5
Liste triée : [1, 2, 3, 5, 8, 9]
```

---

#### **2. Recherche dans une liste**

Écrivez une fonction `est_present(liste, valeur)` qui retourne `True` si `valeur` est dans `liste`, sinon `False`.

**Exemple :**

```python
print(est_present([1, 2, 3], 2))  # True
print(est_present([1, 2, 3], 4))  # False
```

---

#### **3. Fusion de listes**

Écrivez une fonction `fusion(liste1, liste2)` qui retourne une nouvelle liste contenant les éléments des deux listes,
sans doublons.

**Exemple :**

```python
print(fusion([1, 2, 3], [3, 4, 5]))  # [1, 2, 3, 4, 5]
```

---

#### **4. Liste de courses**

Écrivez un programme qui :

- Demande à l'utilisateur des articles à ajouter à une liste de courses.
- Affiche la liste finale.
- Utilise `input()` pour les entrées.

**Exemple :**

```
Ajoutez un article (ou 'quit' pour terminer) : pomme
Ajoutez un article : banane
Ajoutez un article : quit
Liste de courses : ['pomme', 'banane']
```

---

### **Exercices sur les Dictionnaires**

#### **5. Compteur de mots**

Écrivez un programme qui compte le nombre d'occurrences de chaque mot dans une phrase donnée.

- Utilisez `split()` pour diviser la phrase en mots.

**Exemple :**

```python
phrase = "bonjour bonjour monde"
print(compter_mots(phrase))
# {'bonjour': 2, 'monde': 1}
```

---

#### **6. Carnet d'adresses**

Créez un dictionnaire `carnet` avec des entrées comme `{"Alice": "alice@example.com", "Bob": "bob@example.com"}`.

- Ajoutez une fonction pour rechercher un email par nom.

**Exemple :**

```python
print(rechercher_email("Alice"))  # "alice@example.com"
```

---

#### **7. Fusion de dictionnaires**

Écrivez une fonction `fusionner(dict1, dict2)` qui fusionne deux dictionnaires en un seul (les clés en double sont
conservées depuis `dict2`).

**Exemple :**

```python
d1 = {"a": 1, "b": 2}
d2 = {"b": 3, "c": 4}
print(fusionner(d1, d2))  # {'a': 1, 'b': 3, 'c': 4}
```

---

#### **8. Inventaire de jeu vidéo**

Simulez un inventaire de jeu avec un dictionnaire où les clés sont des items (`"épée", "potion"`) et les valeurs sont
les quantités.

- Ajoutez une fonction pour ajouter/supprimer des items.

**Exemple :**

```python
inventaire = {"épée": 1, "potion": 3}
ajouter_item("potion")
print(inventaire)  # {'épée': 1, 'potion': 4}
```

---

### **Exercices Combinaisons (Listes + Dictionnaires)**

#### **9. Statistiques de notes**

Étant donné une liste de notes `[85, 90, 78, 92, 88]`, créez un dictionnaire qui compte le nombre d'étudiants ayant
obtenu :

- "A" (notes ≥ 90),
- "B" (80 ≤ notes < 90),
- "C" (notes < 80).

**Résultat attendu :**

```python
{'A': 2, 'B': 3, 'C': 0}
```

---

#### **10. Jeu de devinette avec scores**

Modifiez l'exercice "Devine le nombre" pour :

- Stocker les scores des joueurs dans un dictionnaire `{nom: score}`.
- Utiliser une liste pour enregistrer l'historique des nombres générés.

**Exemple :**

```python
scores = {"Alice": 4, "Bob": 6}
print(scores)
```

