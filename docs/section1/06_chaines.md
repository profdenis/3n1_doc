# **Manipulation des Chaînes de Caractères**

Les chaînes de caractères (`str`) sont un type fondamental en Python. Elles sont **immuables** (ne peuvent pas être
modifiées après création) et offrent de nombreuses méthodes pour les manipuler.

---

## **1. Création et Accès aux Caractères**

### **a) Déclaration de chaînes**

```python
texte = "Bonjour, monde!"
texte = 'Bonjour, monde!'  # même résultat
multiligne = """Ceci est une chaîne
sur plusieurs lignes."""
```

### **b) Accès aux caractères (indexation)**

```python
print(texte[0])  # "B" (premier caractère)
print(texte[-1])  # "!" (dernier caractère)
print(texte[7:12])  # "monde" (slicing)
```

!!! warning "Avertissement"
    En python, contrairement à d'autres langages, l'usage des `''` est identique à l'usage des `""` : les deux sont 
    interprétés comme des chaînes de caractères. Ils sont interchangeables et peuvent être utilisés selon les 
    préférences personnelles ou les conventions de style du projet. Les `''` ne désignent pas des caractères 
    individuels. `texte[0]` ne donne pas un caractère, mais plutôt une chaîne de caractères contenant un seul
    caractère.

---

## **2. Méthodes Essentielles**

### **a) `len()` – Longueur d'une chaîne**

```python
print(len("Python"))  # 6
```

### **b) `str.lower()` / `str.upper()` – Conversion de casse**

```python
texte = "PyThOn"
print(texte.lower())  # "python"
print(texte.upper())  # "PYTHON"
```

### **c) `str.strip()` – Suppression des espaces (ou caractères spécifiés)**

```python
texte = "   Bonjour   "
print(texte.strip())  # "Bonjour" (supprime les espaces avant/après)
print(texte.lstrip())  # "Bonjour   " (seulement à gauche)
print(texte.rstrip())  # "   Bonjour" (seulement à droite)

# Supprimer d'autres caractères
print("...xabcx...".strip("."))  # "xabcx"
```

### **d) `str.split()` – Découpage en liste**

```python
phrase = "Bonjour, monde!"
mots = phrase.split()  # ["Bonjour,", "monde!"]
mots = phrase.split(",")  # ["Bonjour", " monde!"] (split sur la virgule)
```

### **e) `str.join()` – Concaténation avec un séparateur**

```python
mots = ["Bonjour", "monde"]
phrase = " ".join(mots)  # "Bonjour monde"
phrase = "-".join(mots)  # "Bonjour-monde"
```

---

## **3. Recherche et Remplacement**

### **a) `str.find()` / `str.index()` – Position d'une sous-chaîne**

```python
texte = "Hello, Python!"
print(texte.find("Python"))  # 7 (position de départ)
print(texte.find("Java"))  # -1 (non trouvé)

# index() lève une exception si non trouvé
try:
    print(texte.index("Java"))
except ValueError:
    print("Non trouvé")
```

### **b) `str.replace()` – Remplacement**

```python
texte = "Bonjour, monde!"
print(texte.replace("monde", "Python"))  # "Bonjour, Python!"
```

### **c) `str.count()` – Nombre d'occurrences**

```python
texte = "abababa"
print(texte.count("a"))  # 4
```

---

## **4. Vérification de Contenu**

### **a) Méthodes de test (`str.startswith()`, `str.endswith()`, etc.)**

```python
texte = "Bonjour, monde!"
print(texte.startswith("Bon"))  # True
print(texte.endswith("!"))  # True

# Vérifier si tous les caractères sont des chiffres/lettres
print("123".isdigit())  # True
print("abc".isalpha())  # True
```

### **b) `in` – Opérateur d'inclusion**

```python
texte = "Bonjour"
print("o" in texte)  # True
print("z" in texte)  # False
print("z" not in texte)  # True
```

---

## **5. Formatage de Chaînes (f-strings, `.format()`)**

### **a) f-strings (Python 3.6+)**

```python
nom = "Alice"
âge = 25
print(f"Bonjour {nom}, vous avez {âge} ans.")  # "Bonjour Alice, vous avez 25 ans."
```

### **b) `.format()`**

```python
texte = "Bonjour {}, vous avez {} ans.".format(nom, âge)
```

---

## **6. Exercices Pratiques**

### **1. Nettoyage de texte**

Écrivez une fonction qui :

- Supprime les espaces en début/fin.
- Remplace les tabulations par des espaces.

**Exemple :**

```python
texte = "\t  Bonjour\t!  "
print(nettoyer_texte(texte))  # "Bonjour !"
```

---

### **2. Compteur de mots**

Écrivez une fonction qui compte le nombre de mots dans une phrase.

**Indice :** Utilisez `split()`.

**Exemple :**

```python
phrase = "Bonjour monde!"
print(nombre_mots(phrase))  # 2
```

---

### **3. Censurer un mot**

Remplacez tous les occurrences d'un mot par `***`.
**Exemple :**

```python
texte = "Bonjour monde, bonjour Python"
print(censurer(texte, "bonjour"))  # "*** monde, *** Python"
```

---

## **7. Résumé des Méthodes Clés**

| **Méthode**           | **Description**               | **Exemple**                         |
|-----------------------|-------------------------------|-------------------------------------|
| `len()`               | Longueur de la chaîne         | `len("abc")` → `3`                  |
| `lower()` / `upper()` | Conversion de casse           | `"ABC".lower()` → `"abc"`           |
| `strip()`             | Suppression d'espaces         | `"  abc  ".strip()` → `"abc"`       |
| `split()`             | Découpage en liste            | `"a,b".split(",")` → `["a", "b"]`   |
| `join()`              | Concaténation avec séparateur | `"-".join(["a", "b"])` → `"a-b"`    |
| `find()` / `index()`  | Position d'une sous-chaîne    | `"abc".find("b")` → `1`             |
| `replace()`           | Remplacement                  | `"abc".replace("a", "x")` → `"xbc"` |

---

## **8. Bonnes Pratiques**

✅ **Utilisez `f-strings`** pour le formatage (plus lisible).

✅ **Préférez `str.startswith()`/`endswith()`** aux comparaisons manuelles.

⚠️ **Évitez les boucles sur les chaînes** (utilisez des méthodes intégrées).

---

### **Conclusion**

Les chaînes de caractères en Python sont riches en fonctionnalités. Maîtriser ces méthodes vous permettra d'écrire du
code plus efficace et lisible.

📌 **Astuce :** Utilisez `help(str)` dans le REPL pour voir toutes les méthodes disponibles sur les chaînes !