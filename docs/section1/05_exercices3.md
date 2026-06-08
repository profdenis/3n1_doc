# Exercices 3

## **Exercices de Base (List Comprehension)**

### **1. Carrés des nombres**

Écrivez une compréhension de liste qui génère les carrés des nombres de 0 à 9.
**Résultat attendu :**

```python
[0, 1, 4, 9, 16, 25, 36, 49, 64, 81]
```

---

### **2. Filtrer les nombres pairs**

Étant donné une liste `[1, 2, 3, 4, 5, 6]`, utilisez une compréhension pour ne garder que les nombres pairs.
**Résultat attendu :**

```python
[2, 4, 6]
```

---

### **3. Transformation de chaînes**

Convertissez chaque caractère d'une chaîne en majuscule.
**Exemple :**

```python
"hello" → ["H", "E", "L", "L", "O"]
```

---

## **Exercices Intermédiaires (List Comprehension)**

### **4. Nombres pairs et impairs**

Créez deux listes séparées pour les nombres pairs et impairs dans `range(10)`.
**Résultat attendu :**

```python
pairs = [0, 2, 4, 6, 8]
impairs = [1, 3, 5, 7, 9]
```

---

### **5. Compréhension imbriquée (Matrice)**

Générez une matrice 3x3 remplie de `1`.
**Résultat attendu :**

```python
[
    [1, 1, 1],
    [1, 1, 1],
    [1, 1, 1]
]
```

---

### **6. Filtrer et transformer**

À partir d'une liste `[10, 25, 30, 45]`, gardez seulement les nombres divisibles par 5 et multipliez-les par 2.
**Résultat attendu :**

```python
[20, 60, 90]
```

---

## **Exercices Avancés (List Comprehension)**

### **7. Liste de dictionnaires**

Étant donné une liste de dictionnaires `[{"nom": "Alice", "âge": 25}, {"nom": "Bob", "âge": 30}]`, extrayez les noms.
**Résultat attendu :**

```python
["Alice", "Bob"]
```

---

### **8. Compréhension avec condition complexe**

Filtrez les nombres de `range(1, 100)` qui sont divisibles par 3 **ou** 5.
**Résultat attendu :**

```python
[3, 5, 6, 9, 10, 12, ...]
```

---

### **9. Générer des mots clés**

À partir d'une phrase `"Python est puissant"`, créez une liste de mots en majuscule.
**Résultat attendu :**

```python
["PYTHON", "EST", "PUISSANT"]
```

---

## **Exercices sur les Dictionnaires (Dict Comprehension)**

### **10. Inversion de dictionnaire**

Inversez un dictionnaire `{"a": 1, "b": 2}` en `{1: "a", 2: "b"}`.
**Résultat attendu :**

```python
{1: "a", 2: "b"}
```

---

### **11. Compteur de lettres**

Comptez le nombre d'occurrences de chaque lettre dans `"hello"`.
**Résultat attendu :**

```python
{"h": 1, "e": 1, "l": 2, "o": 1}
```

---

### **12. Dictionnaire de carrés**

Créez un dictionnaire où les clés sont des nombres de 1 à 5 et les valeurs leurs carrés.
**Résultat attendu :**

```python
{1: 1, 2: 4, 3: 9, 4: 16, 5: 25}
```

---

## **Exercices Combinaisons (List + Dict Comprehension)**

### **13. Statistiques de notes**

Étant donné une liste `[85, 90, 78, 92]`, créez un dictionnaire qui compte le nombre d'étudiants ayant obtenu :

- "A" (≥ 90),
- "B" (80 ≤ note < 90),
- "C" (< 80).
  **Résultat attendu :**

```python
{"A": 2, "B": 1, "C": 1}
```

---

### **14. Dictionnaire de mots et longueurs**

À partir d'une liste `["pomme", "banane"]`, créez un dictionnaire `{mot: longueur}`.
**Résultat attendu :**

```python
{"pomme": 5, "banane": 6}
```

---

## **Exercices Défi (Pour les Étudiants Avancés)**

### **15. Compréhension imbriquée complexe**

Générez une liste de dictionnaires représentant des coordonnées `(x, y)` où `x` et `y` vont de 0 à 2.
**Résultat attendu :**

```python
[
    {"x": 0, "y": 0},
    {"x": 0, "y": 1},
    ...
    {"x": 2, "y": 2}
]
```

---

### **16. Filtrer un dictionnaire avec condition**

Étant donné `{"Alice": 85, "Bob": 90}`, gardez seulement les entrées où la note est ≥ 90.
**Résultat attendu :**

```python
{"Bob": 90}
```

---

## **Corrigés Partiels (Pour Vérification)**

### **Exercice 4 (Nombres pairs et impairs) :**

```python
nombres = range(10)
pairs = [x for x in nombres if x % 2 == 0]
impairs = [x for x in nombres if x % 2 != 0]
```

### **Exercice 11 (Compteur de lettres) :**

```python
phrase = "hello"
compteur = {lettre: phrase.count(lettre) for lettre in set(phrase)}
```

---

## **Conseils pour les Étudiants**

- **Testez dans le REPL** : Utilisez `python` en ligne de commande pour vérifier rapidement vos compréhensions.
- **Comparez avec des boucles** : Écrivez d'abord une solution avec `for`, puis convertissez-la en compréhension.
- **Évitez les compréhensions trop complexes** : Si le code devient illisible, utilisez une boucle classique.

Ces exercices couvrent les cas d'usage courants et permettent de bien maîtriser les compréhensions en Python. Bonne
pratique ! 🚀