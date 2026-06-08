# **Introduction à Python**

Python est un langage de programmation polyvalent, apprécié pour sa simplicité et sa lisibilité. Contrairement à Java ou
C, qui sont des langages compilés, Python est **interprété**, ce qui signifie que le code est exécuté ligne par ligne.
Cela le rend idéal pour le prototypage rapide, les scripts et l'enseignement.

Dans ce cours, nous aborderons les bases de Python, en mettant l'accent sur sa syntaxe intuitive et ses fonctionnalités
pratiques. Vous utiliserez des outils comme la **ligne de commande**, un **IDE** (PyCharm recommandé) ou un éditeur
léger (VS Code), et découvrirez comment Python peut servir de calculatrice avancée tout en introduisant des concepts
clés comme les structures de contrôle, les fonctions et la gestion des fichiers.

---

## **1. Exécution de Python : Interpréteur, REPL et IDE**

Python peut être exécuté de plusieurs manières :

### **a) Ligne de commande (Terminal/Console)**

- Ouvrez un terminal (Windows: `cmd`/`PowerShell`, macOS/Linux: `Terminal`).
- Tapez `python` ou `python3` pour lancer l'interpréteur.
  ```bash
  python
  ```
- Vous entrez alors dans le **REPL** (*Read-Eval-Print Loop*), un environnement interactif où chaque commande est
  exécutée immédiatement.

### **b) Fichiers Python (`.py`)**

- Créez un fichier avec l'extension `.py` (ex: `script.py`) et écrivez votre code.
- Exécutez-le depuis le terminal :
  ```bash
  python script.py
  ```

### **c) IDE/Éditeurs recommandés**

- **PyCharm** (recommandé pour son support complet).
- **VS Code** (léger, avec extensions Python comme *Python* et *Pylance*).
- **IDLE** (simple, fourni avec Python).

---

## **2. Python comme calculatrice**

L'interpréteur Python peut servir de calculatrice avancée :

### **a) Opérations de base**

```python
>> > 2 + 3  # Addition
5
>> > 10 / 3  # Division réelle (float)
3.333...
>> > 10 // 3  # Division entière (floor division)
3
>> > 10 % 3  # Modulo (reste de la division)
1
```

### **b) Entiers de précision infinie**

Contrairement à certains langages, Python gère les grands entiers sans perte de précision :

```text
>>> 123456789012345678901234567890
123456789012345678901234567890
```

---

## **3. Indentation et blocs de code**

Python utilise l'**indentation** (espaces ou tabulations) pour définir les blocs de code, contrairement aux accolades
`{}` en Java/C/JS.
Exemple :

```python
if x > 0:
    print("Positif")  # Indentation obligatoire !
else:
    print("Négatif")
```

---

## **4. Structures de contrôle**

### **a) Conditionnelles (`if`, `elif`, `else`)**

```python
x = -5
if x > 0:
    print("Positif")
elif x == 0:
    print("Zéro")
else:
    print("Négatif")  # Résultat : "Négatif"
```

### **b) Boucles (`for`, `while`)**

```python
# Boucle for (itère sur une liste)
for i in [1, 2, 3]:
    print(i)

# Boucle while
count = 0
while count < 5:
    print(count)
    count += 1
```

### **c) `match` (nouveauté Python 3.10)**

Alternative à `switch` en Java/C :

```python
def jour_semaine(n):
    match n:
        case 1:
            return "Lundi"
        case 2:
            return "Mardi"
        case _:
            return "Inconnu"  # Cas par défaut
```

---

## **5. Fonctions**

Définissez des fonctions avec `def` :

```python
def saluer(nom):
    """Fonction qui retourne un message de salut."""
    return f"Bonjour, {nom}!"


print(saluer("Alice"))  # Résultat : "Bonjour, Alice!"
```

---

## **6. Modules et importation**

Python organise le code en **modules** (fichiers `.py`) :

```python
# Importer un module entier
import math

print(math.sqrt(16))  # 4.0

# Importer une fonction spécifique
from random import randint

print(randint(1, 10))  # Nombre aléatoire entre 1 et 10
```

---

## **7. Listes**

Les listes sont des collections mutables (modifiables) :

```python
nombres = [1, 2, 3]
nombres.append(4)  # Ajoute 4 à la fin
print(nombres[0])  # Accès à l'élément 0 : 1

# Slicing (extraction de sous-listes)
print(nombres[1:3])  # [2, 3]
```

---

## **8. Compréhensions de liste**

Syntaxe concise pour créer des listes :

```python
carrés = [x ** 2 for x in range(5)]  # [0, 1, 4, 9, 16]
pairs = [x for x in carrés if x % 2 == 0]  # [0, 4, 16]
```

---

## **9. Dictionnaires**

Structures clé-valeur (similaires aux objets JS) :

```python
personne = {"nom": "Alice", "âge": 25}
print(personne["nom"])  # "Alice"
personne["ville"] = "Montréal"  # Ajout d'une nouvelle clé
```

---

## **10. Exceptions**

Gestion des erreurs avec `try`/`except` :

```python
try:
    result = 10 / 0
except ZeroDivisionError:
    print("Erreur : division par zéro !")
```

---

## **11. Lecture/Écriture de fichiers texte**

### **a) Écrire dans un fichier**

```python
with open("fichier.txt", "w") as f:  # "w" = écriture
    f.write("Bonjour, monde!")
```

### **b) Lire un fichier**

```python
with open("fichier.txt", "r") as f:  # "r" = lecture
    contenu = f.read()
    print(contenu)
```

---

## **12. Autres concepts utiles**

- **Commentaires** : `#` pour une ligne, `'''` ou `"""` pour des blocs.
- **Docstrings** : Chaînes de documentation dans les fonctions (ex: `"""Fonction qui..."""`).
- **Types dynamiques** : Pas besoin de déclarer les types (contrairement à Java/C).

---

## **13. À éviter pour l'instant**

Certains concepts seront vus plus tard :

- Programmation orientée objet (`class`, héritage).
- *Type hints* (`def f(x: int) -> str:`).
- Décorateurs (`@decorator`).
- Gestion avancée des modules (`__init__.py`).

---

## **Exercice pratique**

1. Créez un script Python qui :
    - Demande à l'utilisateur son âge.
    - Affiche "Majeur" si ≥ 18, sinon "Mineur".
    - Utilise une boucle pour afficher les nombres de 1 à 10.
2. Lisez le contenu d'un fichier texte et comptez le nombre de lignes.
