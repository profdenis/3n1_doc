# **Compréhensions de Liste et Dictionnaire**

Les **compréhensions** sont une caractéristique puissante de Python qui permet d'écrire des boucles et des conditions de
manière concise. Elles remplacent souvent les boucles `for` classiques pour créer des listes, des dictionnaires ou des
ensembles.

---

## **1. Compréhension de Liste (List Comprehension)**

### **Syntaxe de Base**

```python
[nouvelle_valeur for item in iterable if condition]
```

- `item` : Élément courant dans l'iterable.
- `nouvelle_valeur` : Expression appliquée à chaque élément.
- `condition` (optionnelle) : Filtre les éléments.

---

### **Exemples Pratiques**

#### **a) Transformation Simple**

```python
# Carrés des nombres de 0 à 9
carrés = [x ** 2 for x in range(10)]
print(carrés)  # [0, 1, 4, 9, 16, 25, 36, 49, 64, 81]
```

#### **b) Avec Condition (Filtre)**

```python
# Nombres pairs entre 0 et 9
pairs = [x for x in range(10) if x % 2 == 0]
print(pairs)  # [0, 2, 4, 6, 8]
```

#### **c) Transformation + Filtre**

```python
# Carrés des nombres pairs entre 0 et 9
carrés_pairs = [x ** 2 for x in range(10) if x % 2 == 0]
print(carrés_pairs)  # [0, 4, 16, 36, 64]
```

#### **d) Itération sur des Chaînes**

```python
# Liste des lettres d'un mot
lettres = [c for c in "Python"]
print(lettres)  # ['P', 'y', 't', 'h', 'o', 'n']
```

#### **e) Nested List Comprehension (Listes Imbriquées)**

```python
# Matrice 3x3 remplie de zéros
matrice = [[0 for _ in range(3)] for _ in range(3)]
print(matrice)
# [[0, 0, 0], [0, 0, 0], [0, 0, 0]]
```

⚠️ **Attention** : Évitez `[[0]*3]*3` (créerait des références identiques).

---

### **Avantages vs Boucles Classiques**

| **Compréhension de Liste**                            | **Boucle `for`** |
|-------------------------------------------------------|------------------|
| Plus concise et lisible.                              | Plus verbeuse.   |
| Exécution souvent plus rapide (optimisée par Python). | Moins optimisée. |

---

## **2. Compréhension de Dictionnaire (Dict Comprehension)**

### **Syntaxe de Base**

```python
{clé: valeur for item in iterable if condition}
```

- `clé` et `valeur` : Expressions définissant les paires clé-valeur.
- `item` : Élément courant dans l'iterable.

---

### **Exemples Pratiques**

#### **a) Inversion de Clés et Valeurs**

```python
# Dictionnaire original
notes = {"Alice": 85, "Bob": 90}
# Inversé (valeur → clé)
inverse = {v: k for k, v in notes.items()}
print(inverse)  # {85: 'Alice', 90: 'Bob'}
```

#### **b) Filtrer un Dictionnaire**

```python
# Garder seulement les notes ≥ 90
bons_élèves = {k: v for k, v in notes.items() if v >= 90}
print(bons_élèves)  # {'Bob': 90}
```

#### **c) Transformation des Valeurs**

```python
# Ajouter 10% à chaque note
notes_augmentées = {k: v * 1.1 for k, v in notes.items()}
print(notes_augmentées)  # {'Alice': 93.5, 'Bob': 99.0}
```

#### **d) Générer un Dictionnaire à partir d'une Liste**

```python
# Liste de mots → dictionnaire (mot: longueur)
mots = ["pomme", "banane"]
longueurs = {mot: len(mot) for mot in mots}
print(longueurs)  # {'pomme': 5, 'banane': 6}
```

#### **e) Nested Dict Comprehension**

```python
# Dictionnaire de matrices (3x3)
matrices = {
    "A": [[i + j for j in range(3)] for i in range(3)],
    "B": [[0 for _ in range(3)] for _ in range(3)]
}
print(matrices["A"])
# [[0, 1, 2], [1, 2, 3], [2, 3, 4]]
```

---

### **Cas d'Usage Avancés**

#### **a) Compter les Occurrences (Alternative à `collections.Counter`)**

```python
texte = "bonjour bonjour monde"
compteur = {mot: texte.split().count(mot) for mot in set(texte.split())}
print(compteur)  # {'bonjour': 2, 'monde': 1}
```

#### **b) Dictionnaire de Carrés avec Indices**

```python
# {0: 0, 1: 1, 2: 4, ..., 9: 81}
carrés = {i: i ** 2 for i in range(10)}
print(carrés)
```

---

## **3. Comparaison avec `map()` et `filter()`**

| **Méthode**                | **Exemple**                                | **Avantages**                       |
|----------------------------|--------------------------------------------|-------------------------------------|
| **Compréhension de Liste** | `[x*2 for x in range(5)]`                  | Lisible, Pythonique.                |
| **`map()`**                | `list(map(lambda x: x*2, range(5)))`       | Utile pour les fonctions complexes. |
| **`filter()`**             | `list(filter(lambda x: x%2==0, range(5)))` | Pour des filtres simples.           |

✅ **Préférez les compréhensions** pour la clarté, sauf si vous utilisez des fonctions existantes.

---

## **4. Bonnes Pratiques**

1. **Évitez les compréhensions trop complexes** (privilégiez la lisibilité).
2. **Utilisez `_` pour les variables inutilisées** :
   ```python
   [x for x in range(5)]  # Correct
   [_ for _ in range(5)]  # Si la valeur n'est pas utilisée
   ```
3. **Testez avec des petits exemples** avant de généraliser.

---

## **5. Exercices pour S'entraîner**

### **List Comprehension**

1. Créez une liste des cubes des nombres impairs entre 1 et 20.
2. Filtrez les mots de plus de 4 lettres dans `["pomme", "kiwi", "banane"]`.

### **Dict Comprehension**

3. Convertissez une liste `[("a", 1), ("b", 2)]` en dictionnaire.
4. Comptez le nombre de voyelles dans `"Hello World"`.

---

## **6. Résumé des Syntaxes Clés**

| **Type**        | **Syntaxe**                        | **Exemple**                                     |
|-----------------|------------------------------------|-------------------------------------------------|
| Liste           | `[expr for x in iterable]`         | `[x*2 for x in [1,2,3]]` → `[2,4,6]`            |
| Liste (filtrée) | `[expr for x in iterable if cond]` | `[x for x in range(5) if x%2==0]` → `[0,2,4]`   |
| Dictionnaire    | `{key: val for x in iterable}`     | `{x:x**2 for x in [1,2,3]}` → `{1:1, 2:4, 3:9}` |

---

### **Conclusion**

Les compréhensions de liste et dictionnaire sont des outils puissants pour écrire du code Python plus **concise** et *
*lisible**. Maîtrisez-les pour gagner en efficacité !

📌 **Astuce** : Utilisez le REPL (`python` dans le terminal) pour tester rapidement vos compréhensions.