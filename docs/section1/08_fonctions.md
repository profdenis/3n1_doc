# **Les Fonctions**

## **1. Définition de Fonctions**

### **Syntaxe de base**

```python
def nom_fonction(param1, param2):
    """Docstring : description de la fonction"""
    # Corps de la fonction
    return valeur_de_retour  # Optionnel
```

### **Exemple simple**

```python
def saluer(nom):
    """Retourne un message de salut."""
    return f"Bonjour, {nom}!"


print(saluer("Alice"))  # "Bonjour, Alice!"
```

---

## **2. Fonctions Lambda (Anonymes)**

### **Syntaxe**

```python
lambda arguments: expression
```

- Utilisées pour des fonctions courtes.
- Ne peuvent pas contenir de `return` ou de docstrings.

### **Exemples**

#### **a) Lambda simple**

```python
carré = lambda x: x ** 2
print(carré(5))  # 25
```

#### **b) Avec `map()` et `filter()`**

```python
nombres = [1, 2, 3, 4]
# Doubler chaque nombre
doublés = list(map(lambda x: x * 2, nombres))
print(doublés)  # [2, 4, 6, 8]

# Garder les nombres pairs
pairs = list(filter(lambda x: x % 2 == 0, nombres))
print(pairs)  # [2, 4]
```

!!! note "Compréhension vs. `map()` et `filter()`"
    Python utilise les compréhensions pour créer des listes, des dictionnaires et des ensembles à partir de séquences 
    existantes, mais `map()` et `filter()` sont plus flexibles et peuvent être utilisés avec des fonctions plus 
    complexes. Pour des cas simples, on devrait privilégier les compréhensions, mais pour des cas plus compliqués, 
    `map()` et `filter()` peuvent être plus appropriés.

    **Exercice :** Réécrire les exemples de `map()` et `filter()` avec des compréhensions de liste.

#### **c) Dans `sorted()`**

```python
étudiants = [("Alice", 25), ("Bob", 20)]
# Trier par âge (deuxième élément du tuple)
triés = sorted(étudiants, key=lambda x: x[1])
print(triés)  # [('Bob', 20), ('Alice', 25)]
print(sorted(triés))  # [('Alice', 25), ('Bob', 20)]
```

---

## **3. Références à des Fonctions**

En Python, **tout est objet**, y compris les fonctions.
Cela signifie qu'une fonction peut être :

- Passée en argument.
- Stockée dans une variable.
- Ajoutée à une liste/dictionnaire.

### **Exemples**

#### **a) Fonction comme argument**

```python
def appliquer_operation(x, y, operation):
    return operation(x, y)


# Définition des opérations
def addition(a, b):
    return a + b


def multiplication(a, b):
    return a * b


print(appliquer_operation(5, 3, addition))  # 8
print(appliquer_operation(5, 3, multiplication))  # 15
```

#### **b) Fonction dans une variable**

```python
opération = addition  # Référence à la fonction `addition`
print(opération(2, 3))  # 5 (équivalent à `addition(2, 3)`)
```

---

## **4. "Tout est Objet" en Python**

### **Explication**

En Python :

- Les fonctions sont des **objets de première classe**.
- Elles peuvent être :
    - Assignées à des variables.
    - Passées comme arguments.
    - Retournées par d'autres fonctions.

### **Exemple : Liste de Fonctions**

```python
# Définition de plusieurs fonctions
def dire_bonjour():
    return "Bonjour"


def dire_au_revoir():
    return "Au revoir"


# Liste de références à ces fonctions
fonctions = [dire_bonjour, dire_au_revoir]

# Appel des fonctions via la liste
for fonction in fonctions:
    print(fonction())  # "Bonjour" puis "Au revoir"
```

---

## **5. Dictionnaire d'Opérations (Table de Symboles)**

### **Exemple : Calculatrice avec `+` et `-`**

```python
# Définition des opérations
def addition(a, b):
    return a + b


def soustraction(a, b):
    return a - b


# Dictionnaire associant un symbole à une fonction
opérations = {
    "+": addition,
    "-": soustraction,
}

# Utilisation
resultat = opérations["+"](5, 3)  # Appelle `addition(5, 3)`
print(resultat)  # 8

# Avec input()
symbole = input("Choisissez une opération (+/-) : ")
a = int(input("Premier nombre : "))
b = int(input("Deuxième nombre : "))
print(opérations[symbole](a, b))
```

---

## **6. Combinaisons Avancées**

### **a) Liste de Fonctions + `map()`**

```python
nombres = [1, 2, 3]

# Liste de fonctions à appliquer
fonctions = [
    lambda x: x * 2,  # Doubler
    lambda x: x + 1,  # Incrémenter
]

# Appliquer chaque fonction à la liste
for fonction in fonctions:
    résultats = list(map(fonction, nombres))
    print(résultats)
# [2, 4, 6] puis [2, 3, 4]
```

### **b) Dictionnaire + Compréhension de Liste**

```python
# Dictionnaire de transformations
transformations = {
    "majuscules": lambda s: s.upper(),
    "minuscules": lambda s: s.lower(),
}

texte = "Bonjour"

# Appliquer chaque transformation
for nom, fonction in transformations.items():
    print(f"{nom}: {fonction(texte)}")
# "majuscules: BONJOUR"
# "minuscules: bonjour"
```

### **c) `join()` avec des Fonctions**

```python
nombres = [1, 2, 3]

# Convertir chaque nombre en chaîne et les joindre
resultat = "-".join(map(str, nombres))
print(resultat)  # "1-2-3"


# Avec une fonction personnalisée
def formater(x):
    return f"[{x}]"


resultat = ", ".join(map(formater, nombres))
print(resultat)  # "[1], [2], [3]"
```

---

## **7. Paramètres Nommés en Python**

### **1. Syntaxe de Base**

En Python, vous pouvez :

- Appeler une fonction en spécifiant **explicitement le nom des paramètres** (`nom=valeur`).
- Inverser l'ordre des arguments si vous utilisez les noms.

```python
def addition(x, y):
    return x + y


# Appel classique (positionnel)
print(addition(5, 3))  # 8

# Appel avec paramètres nommés
print(addition(y=3, x=5))  # 8 (ordre inversé !)
```

---

### **2. Avantages des Paramètres Nommés**

✅ **Lisibilité améliorée** :

```python
def configurer_couleur(rouge, vert, bleu):
    return f"RGB({rouge}, {vert}, {bleu})"


# Plus clair que configurer_couleur(255, 0, 128)
print(configurer_couleur(rouge=255, vert=0, bleu=128))  # "RGB(255, 0, 128)"
```

✅ **Ordre flexible** :

```python
def afficher_coordonnées(x, y):
    return f"({x}, {y})"


print(afficher_coordonnées(y=10, x=5))  # "(5, 10)" (ordre inversé)
```

---

### **3. Mélange de Paramètres Positionnels et Nommés**

Vous pouvez combiner les deux styles, mais :

- Les arguments positionnels doivent venir **avant** les nommés.
- Un paramètre ne peut pas être spécifié deux fois.

```python
def fonction(a, b, c=10):
    return a + b + c


print(fonction(1, 2))  # 13 (c=10 par défaut)
print(fonction(1, 2, 3))  # 6 (tous positionnels)
print(fonction(1, b=2, c=3))  # 6 (mélange)
# print(fonction(a=1, 2, 3))   ❌ Erreur ! Positionnel après nommé
```

---

### **4. Cas Particuliers**

#### **a) Valeurs par défaut + paramètres nommés**

```python
def dessiner_rectangle(largeur, hauteur=10, couleur="bleu"):
    return f"{largeur}x{hauteur} en {couleur}"


print(dessiner_rectangle(5))  # "5x10 en bleu"
print(dessiner_rectangle(hauteur=20, largeur=3))  # "3x20 en bleu"
```

#### **b) `**kwargs` pour arguments nommés variables**

```python
def afficher_infos(**kwargs):
    for clé, valeur in kwargs.items():
        print(f"{clé}: {valeur}")


afficher_infos(nom="Alice", âge=25, ville="Montréal")
# nom: Alice
# âge: 25
# ville: Montréal
```

---

### **Bonnes Pratiques**

✅ **Utilisez les paramètres nommés** pour :

- Les fonctions avec beaucoup de paramètres.
- Les cas où l'ordre n'est pas intuitif.

⚠️ **Évitez de mélanger positionnel et nommé** si cela rend le code illisible.

---

Les paramètres nommés permettent :

- Une **meilleure lisibilité** du code.
- Une **flexibilité dans l'ordre des arguments**.
- Des **appels de fonction plus explicites**.

📌 **Astuce** : Dans les IDE comme PyCharm ou VS Code, le surlignage des paramètres nommés aide à éviter les erreurs !

---

## **8. Nombre de paramètres variable**

Il est possible d'utiliser `**kwargs` pour **des paramètres nommés variables** (comme mentionné plus haut), et
`*args` pour **des paramètres positionnels variables**.

```python
def formatter_noms(*args):
    temp = ", ".join(map(str.lower, args))
    return f"[{temp}]"


print(formatter_noms("Alice", "Bob", "Charlie"))
```

---

## **9. Exemple : Fonction de Logging**

```python
from datetime import datetime

def logger(message, niveau="INFO", fichier=None):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    log_entry = f"[{timestamp}] [{niveau}] {message}"

    if fichier:
        with open(fichier, "a") as f:
            f.write(log_entry + "\n")
    else:
        print(log_entry)

# Utilisation
logger("Début du programme")         # INFO par défaut
logger("Erreur critique", "ERROR")   # Niveau personnalisé
logger("Debug", "DEBUG", "log.txt")  # Avec fichier
```

---

## **10. Conclusion**

Les fonctions en Python sont puissantes et flexibles. En comprenant leur nature d'objet, vous pouvez créer des designs
élégants comme :

- Des listes de fonctions pour des pipelines de traitement.
- Des dictionnaires pour des tables d'opérations dynamiques.

📌 **Astuce :** Utilisez `help(fonction)` dans le REPL pour explorer les attributs d'une fonction (comme `__doc__` ou
`__name__`).