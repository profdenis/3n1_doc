# Exercices 5

## **Exercices de Base**

### **1. Fonction de salutation**

Écrivez une fonction `saluer(nom)` qui retourne `"Bonjour, [nom]!"`.

**Exemple :**

```python
print(saluer("Alice"))  # "Bonjour, Alice!"
```

---

### **2. Calcul d'aire**

Écrivez une fonction `aire_rectangle(longueur, largeur)` qui calcule l'aire d'un rectangle.

**Exemple :**

```python
print(aire_rectangle(5, 3))  # 15
```

---

### **3. Fonction avec valeur par défaut**

Modifiez la fonction précédente pour que `largeur` ait une valeur par défaut de `1`.

**Exemple :**

```python
print(aire_rectangle(5))  # 5 (équivalent à aire_rectangle(5, 1))
```

---

## **Exercices Intermédiaires**

### **4. Fonction récursive (Factorielle)**

Écrivez une fonction `factorielle(n)` qui calcule `n!` de manière récursive.

**Exemple :**

```python
print(factorielle(5))  # 120
```

---

### **5. Fonction avec nombre variable d'arguments**

Écrivez une fonction `somme(*args)` qui retourne la somme de tous les arguments passés.

**Exemple :**

```python
print(somme(1, 2, 3))  # 6
print(somme(10, 20))  # 30
```

---

### **6. Fonction avec arguments nommés**

Écrivez une fonction `personne(nom, âge=0)` qui retourne `"[nom] a [âge] ans"`.

**Exemple :**

```python
print(personne("Alice", 25))  # "Alice a 25 ans"
print(personne("Bob"))  # "Bob a 0 ans"
```

---

## **Exercices sur les Lambdas**

### **7. Lambda pour doubler un nombre**

Écrivez une lambda `doubler` qui retourne le double de son argument.

**Exemple :**

```python
doubler = lambda x: x * 2
print(doubler(5))  # 10
```

---

### **8. Utilisation avec `map()`**

Utilisez `map()` et une lambda pour doubler chaque élément de `[1, 2, 3]`.

**Résultat attendu :**

```python
[2, 4, 6]
```

---

### **9. Tri personnalisé**

Triez la liste `[("Alice", 25), ("Bob", 20)]` par âge en utilisant une lambda avec `sorted()`.

**Résultat attendu :**

```python
[('Bob', 20), ('Alice', 25)]
```

---

## **Exercices sur les Références à des Fonctions**

### **10. Fonction qui appelle une autre fonction**

Écrivez une fonction `appliquer(fonction, x)` qui applique `fonction` à `x`.

**Exemple :**

```python
def carré(x):
    return x * x


print(appliquer(carré, 5))  # 25
```

---

### **11. Liste de fonctions**

Créez une liste `[carré, doubler]` et utilisez-la pour appliquer ces opérations à `3`.

**Résultat attendu :**

```python
[9, 6]  # carré(3)=9, doubler(3)=6
```

---

## **Exercices Avancés**

### **12. Dictionnaire d'opérations**

Créez un dictionnaire `opérations` qui associe `+` et `-` à des fonctions correspondantes.

**Exemple :**

```python
print(opérations["+"](5, 3))  # 8
print(opérations["-"](5, 3))  # 2
```

---

### **13. Calculatrice avec input()**

Utilisez le dictionnaire précédent pour créer une calculatrice interactive.

**Exemple :**

```
Choisissez une opération : +
Premier nombre : 5
Deuxième nombre : 3
Résultat : 8
```

---

### **14. Liste de fonctions pour filtrer des nombres**

Écrivez une fonction `filtrer(nombres, conditions)` qui retourne les nombres satisfaisant toutes les conditions (listes
de lambdas).

**Exemple :**

```python
nombres = [1, -2, 3, -4]
conditions = [
    lambda x: x > 0,
    lambda x: x % 2 == 1,
]

print(filtrer(nombres, conditions))  # [1, 3]
```

---

## **Exercices Défi**

### **15. Dictionnaire de formattage**

Créez un dictionnaire `formats` où :

- Les clés sont des noms (`"HTML"`, `"JSON"`).
- Les valeurs sont des fonctions qui formatent une chaîne.

**Exemple :**

```python
textes = ["Bonjour", "Monde"]

for texte in textes:
    for nom, fonction in formats.items():
        print(f"{nom}: {fonction(texte)}")
```

---

### **16. Pipeline de transformations**

Écrivez une fonction `pipeline(valeur, fonctions)` qui applique une liste de fonctions à une valeur.

**Exemple :**

```python
transformations = [
    lambda x: x * 2,
    lambda x: x + 1,
]

print(pipeline(5, transformations))  # ((5*2)+1) = 11
```

---

## **Corrigés Partiels**

### **Exercice 4 (Factorielle) :**

```python
def factorielle(n):
    if n == 0:
        return 1
    return n * factorielle(n - 1)
```

### **Exercice 12 (Dictionnaire d'opérations) :**

```python
opérations = {
    "+": lambda a, b: a + b,
    "-": lambda a, b: a - b,
}
```

---

## **7. Exercices Pratiques**

### **1. Calculatrice avec Dictionnaire d'Opérations**

Écrivez un programme qui :

- Utilise un dictionnaire pour associer `+`, `-`, `*`, `/` à des fonctions.
- Demande à l'utilisateur une opération et deux nombres.
- Affiche le résultat.

**Exemple :**

```
Choisissez une opération : +
Premier nombre : 5
Deuxième nombre : 3
Résultat : 8
```

---

### **2. Liste de Fonctions pour Filtrer des Nombres**

Écrivez une fonction `filtrer(nombres, conditions)` qui :

- Prend une liste de nombres et une liste de fonctions (ex: `lambda x: x > 0`).
- Retourne les nombres qui satisfont **toutes** les conditions.

**Exemple :**

```python
nombres = [1, -2, 3, -4]
conditions = [
    lambda x: x > 0,
    lambda x: x % 2 == 1,
]

print(filtrer(nombres, conditions))  # [1, 3]
```

---

### **3. Dictionnaire de Formattage**

Créez un dictionnaire `formats` où :

- Les clés sont des noms (`"HTML"`, `"JSON"`).
- Les valeurs sont des fonctions qui formatent une chaîne.

**Exemple :**

```python
textes = ["Bonjour", "Monde"]

# Appliquer chaque format à la liste
for texte in textes:
    for nom, fonction in formats.items():
        print(f"{nom}: {fonction(texte)}")
```

---

## **8. Solutions aux Exercices**

### **Exercice 1 (Calculatrice) :**

```python
opérations = {
    "+": lambda a, b: a + b,
    "-": lambda a, b: a - b,
    "*": lambda a, b: a * b,
    "/": lambda a, b: a / b if b != 0 else "Erreur",
}

symbole = input("Opération : ")
a = float(input("Premier nombre : "))
b = float(input("Deuxième nombre : "))
print(opérations[symbole](a, b))
```

### **Exercice 2 (Filtrer des Nombres) :**

```python
def filtrer(nombres, conditions):
    for condition in conditions:
        nombres = list(filter(condition, nombres))
    return nombres


nombres = [1, -2, 3, -4]
conditions = [
    lambda x: x > 0,
    lambda x: x % 2 == 1,
]
print(filtrer(nombres, conditions))  # [1, 3]
```

---

## **9. Bonnes Pratiques**

✅ **Préférez les noms de fonctions explicites** plutôt que des lambdas complexes.

✅ **Documentez vos fonctions** avec des docstrings.

⚠️ **Évitez les effets de bord** dans les fonctions (modifications externes).
 
---


### **4. Exercices sur les Paramètres par Défaut**

#### **Exercice 1 : Fonction de formatage**
Écrivez une fonction `formater_texte(texte, majuscules=False, alignement="gauche")` qui :
- Met le texte en majuscules si `majuscules=True`.
- Aligne le texte à gauche/droite/centre selon `alignement`.

**Exemple :**
```python
print(formater_texte("bonjour"))          # "bonjour"
print(formater_texte("bonjour", True))    # "BONJOUR"
print(formater_texte("bonjour", False, "droite"))  # "bonjour" (aligné à droite)
```

---

#### **Exercice 2 : Fonction de dessin**
Écrivez une fonction `dessiner_ligne(caractère="*", longueur=10)` qui retourne une chaîne comme `"**********"`.

**Exemple :**
```python
print(dessiner_ligne())          # "**********"
print(dessiner_ligne("#", 5))    # "#####"
```

---

#### **Exercice 3 : Fonction de calcul avancé**
Écrivez une fonction `calculer_statistiques(nombres, moyenne=True, médiane=False)` qui :
- Calcule la moyenne si `moyenne=True`.
- Calcule la médiane si `médiane=True`.

**Exemple :**
```python
print(calculer_statistiques([1, 2, 3]))          # {"moyenne": 2.0}
print(calculer_statistiques([1, 2, 3], True, True))  # {"moyenne": 2.0, "médiane": 2}
```

---

#### **Exercice 4 : Fonction de connexion (simulée)**
Écrivez une fonction `se_connecter(utilisateur, mot_de_passe=None)` qui :
- Retourne `"Connecté"` si le mot de passe est correct.
- Si aucun mot de passe n'est fourni, retourne `"Connexion anonyme"`.

**Exemple :**
```python
print(se_connecter("Alice"))          # "Connexion anonyme"
print(se_connecter("Bob", "1234"))    # "Connecté"
```

---

### **5. Solutions aux Exercices**

#### **Solution Exercice 1 :**
```python
def formater_texte(texte, majuscules=False, alignement="gauche"):
    if majuscules:
        texte = texte.upper()
    if alignement == "droite":
        return texte.rjust(len(texte))
    elif alignement == "centre":
        return texte.center(len(texte))
    else:  # gauche
        return texte
```

#### **Solution Exercice 2 :**
```python
def dessiner_ligne(caractère="*", longueur=10):
    return caractère * longueur
```

#### **Solution Exercice 3 :**
```python
def calculer_statistiques(nombres, moyenne=True, médiane=False):
    résultats = {}
    if moyenne:
        résultats["moyenne"] = sum(nombres) / len(nombres)
    if médiane:
        nombres_tris = sorted(nombres)
        n = len(nombres_tris)
        if n % 2 == 1:
            résultats["médiane"] = nombres_tris[n//2]
        else:
            résultats["médiane"] = (nombres_tris[n//2-1] + nombres_tris[n//2]) / 2
    return résultats
```

---

### **6. Bonnes Pratiques**
✅ **Placez toujours les paramètres obligatoires en premier**, suivis des optionnels.
✅ **Utilisez `None` comme valeur par défaut** pour les paramètres mutables.
⚠️ **Évitez les valeurs mutables par défaut** (listes, dictionnaires) sauf si c'est intentionnel.

---

### **7. Cas Réel : Fonction de Logging**
```python
def logger(message, niveau="INFO", fichier=None):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    log_entry = f"[{timestamp}] [{niveau}] {message}"

    if fichier:
        with open(fichier, "a") as f:
            f.write(log_entry + "\n")
    else:
        print(log_entry)

# Utilisation
logger("Début du programme")          # INFO par défaut
logger("Erreur critique", "ERROR")   # Niveau personnalisé
logger("Debug", "DEBUG", "log.txt")  # Avec fichier
```

---

### **5. Exercices sur les Paramètres Nommés**

#### **Exercice 1 : Fonction de formatage**
Écrivez une fonction `formater_texte(texte, majuscules=False, alignement="gauche")` et appelez-la avec des paramètres nommés pour :
- Mettre le texte en majuscules.
- Aligner à droite.

**Exemple :**
```python
print(formater_texte("bonjour", alignement="droite"))  # "bonjour" (aligné à droite)
```

---

#### **Exercice 2 : Fonction de calcul**
Écrivez une fonction `calculer(a, b, opération="+")` qui effectue l'opération demandée. Appelez-la avec :
- L'ordre des arguments inversé.
- Un paramètre nommé pour l'opération.

**Exemple :**
```python
print(calculer(b=10, a=5, opération="-"))  # 5
```

---

#### **Exercice 3 : Fonction de dessin**
Écrivez une fonction `dessiner_ligne(caractère="*", longueur=10)` et appelez-la avec :
- Le caractère en premier (positionnel).
- La longueur comme paramètre nommé.

**Exemple :**
```python
print(dessiner_ligne("#", longueur=5))  # "#####"
```

---

#### **Exercice 4 : Fonction de configuration**
Écrivez une fonction `configurer(largeur, hauteur, couleur="bleu")` et appelez-la avec :
- La couleur en premier (paramètre nommé).
- Les dimensions dans l'ordre classique.

**Exemple :**
```python
print(configurer(couleur="rouge", largeur=10, hauteur=5))  # "10x5 en rouge"
```

---

### **6. Solutions aux Exercices**

#### **Solution Exercice 1 :**
```python
def formater_texte(texte, majuscules=False, alignement="gauche"):
    if majuscules:
        texte = texte.upper()
    if alignement == "droite":
        return texte.rjust(len(texte))
    elif alignement == "centre":
        return texte.center(len(texte))
    else:  # gauche
        return texte

print(formater_texte("bonjour", alignement="droite"))  # "bonjour" (aligné à droite)
```

#### **Solution Exercice 2 :**
```python
def calculer(a, b, opération="+"):
    if opération == "+":
        return a + b
    elif opération == "-":
        return a - b
    else:
        return "Opération non supportée"

print(calculer(b=10, a=5, opération="-"))  # 5
```

#### **Solution Exercice 3 :**
```python
def dessiner_ligne(caractère="*", longueur=10):
    return caractère * longueur

print(dessiner_ligne("#", longueur=5))  # "#####"
```

---

### **7. Cas Réel : Fonction de Logging Avancé**

```python
def logger(message, niveau="INFO", fichier=None, timestamp=True):
    log_entry = message
    if timestamp:
        log_entry = f"[{datetime.now()}] {log_entry}"
    log_entry = f"[{niveau}] {log_entry}"

    if fichier:
        with open(fichier, "a") as f:
            f.write(log_entry + "\n")
    else:
        print(log_entry)

# Appels avec paramètres nommés
logger("Début du programme", niveau="INFO")  # Niveau spécifié en premier
logger(message="Erreur critique", fichier="log.txt")  # Message en dernier
```

---


## **Conseils pour les Étudiants**

- **Testez dans le REPL** : Utilisez `python` en ligne de commande pour vérifier rapidement vos fonctions.
- **Comparez avec des boucles** : Par exemple, pour l'exercice 5 (`somme`), comparez une solution avec `*args` et une
  boucle manuelle.
- **Utilisez `help(fonction)`** dans le REPL pour explorer les attributs d'une fonction.

Ces exercices couvrent les cas d'usage courants et permettent de bien maîtriser la programmation fonctionnelle en
Python. Bonne pratique ! 🚀