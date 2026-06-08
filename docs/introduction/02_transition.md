# Introduction à Python : Guide de Transition

**Objectif :** Passer du monde des accolades `{}` et du typage statique au monde de l'indentation et du typage
dynamique.

## 1. L'écosystème Python

Contrairement au Java ou au C, Python est un langage **interprété**.

* **L'interpréteur :** Le code n'est pas transformé en binaire avant exécution, mais lu ligne par ligne par
  l'interpréteur.
* **Le REPL (Read-Eval-Print Loop) :** Tapez `python` dans votre terminal. C'est un laboratoire instantané. Idéal pour
  tester une ligne de code ou une formule mathématique sans créer de fichier.
* **L'environnement de développement (IDE) :**
    * **PyCharm :** Recommandé pour les projets complexes (excellent support du débogage et de l'analyse statique).
    * **VS Code :** Très populaire, léger, nécessite l'extension Python.
* **Gestion des environnements (Note rapide) :** Mentionner que contrairement au C, on installe souvent des
  bibliothèques via `pip`.

## 2. Python comme calculatrice (Les particularités mathématiques)

Python est extrêmement puissant pour le calcul numérique.

* **Entiers à précision infinie :** Contrairement au `int` en C ou Java qui finit par "déborder" (*overflow*), un entier
  en Python grandit tant que votre RAM le permet.
    * *Exemple : $2^{100}$ fonctionne sans problème.*
* **La division (Attention piège !) :**
    * `/` : Division réelle (toujours retourne un `float`). Ex: `5 / 2` $\rightarrow$ `2.5`.
    * `//` : Division entière (tronque le résultat). Ex: `5 // 2` $\rightarrow$ `2`.
    * `%` : Modulo (reste de la division).

## 3. La syntaxe : Adieu les accolades, bonjour l'indentation

C'est le choc culturel principal pour un étudiant venant du C ou Java.

* **L'indentation est syntaxique :** En Python, l'espace blanc n'est pas là pour la lisibilité, il définit la structure
  du code (les blocs). Un mauvais décalage = une `IndentationError`.
* **Structures de contrôle :**
    * `if`, `elif`, `else` (Notez le `elif` au lieu de `else if`).
    * `while` : Identique aux autres langages.
    * `for` : En Python, le `for` est en fait un "for each". On itère sur des éléments d'une séquence, pas sur un
      compteur (on utilise `range()` pour simuler un `for(i=0...)`).
    * `match` : Introduit récemment (Python 3.10+), c'est le "pattern matching" (plus puissant qu'un simple `switch` en
      JS/C).

## 4. Fonctions et Modules

* **Définition :** Utilisation du mot-clé `def`. Pas besoin de spécifier le type de retour.
  ```python
  def saluer(nom):
      return f"Bonjour {nom}"
  ```
* **Importation :** On n'inclut pas de fichiers `.h`, on importe des modules.
  ```python
  import math
  print(math.sqrt(16))
  
  from random import randint # Import ciblé
  ```

## 5. Les Structures de Données (Le cœur de Python)

### Les Listes (`list`)

Ce sont des tableaux dynamiques (comme les `ArrayList` en Java ou les tableaux JS). Elles peuvent contenir des types
mélangés.

* `ma_liste = [1, "texte", 3.14]`
* Opérations : `.append()`, `.pop()`, slicing (`ma_liste[0:2]`).

### La Compréhension de liste (Le style "Pythonic")

C'est une manière concise et très rapide de créer des listes. C'est un concept clé pour ne pas écrire de boucles `for`
inutiles.

* *Approche classique :*
  ```python
  carres = []
  for x in range(10):
      carres.append(x**2)
  ```
* *Approche Pythonic :*
  ```python
  carres = [x**2 for x in range(10)]
  ```

### Les Dictionnaires (`dict`)

L'équivalent des objets JSON en JS ou des `HashMap` en Java. C'est une structure clé-valeur ultra performante.

* `mon_dict = {"nom": "Alice", "age": 20}`
* Accès : `mon_dict["nom"]`.

> **Note sur les tableaux :** En Python, pour faire du calcul matriciel intensif (comme en C ou avec des tableaux de
taille fixe), on utilise la bibliothèque **NumPy**. Les listes standards ne sont pas optimisées pour le calcul
scientifique pur.

## 6. Gestion des erreurs (Exceptions)

Le concept est identique à Java/JS, mais la syntaxe change.

* `try` ... `except` (au lieu de `catch`).
* `finally` pour le nettoyage.

```python
try:
    res = 10 / 0
except ZeroDivisionError:
    print("On ne peut pas diviser par zéro !")
```

## 7. Manipulation de fichiers (Le mode sécurisé)

On apprend dès le départ à utiliser le gestionnaire de contexte `with`. Cela garantit que le fichier est fermé même si
une erreur survient (évite les fuites de mémoire/fichiers).

```python
# Écriture
with open("test.txt", "w") as f:
    f.write("Hello Python\n")
    f.write("Deuxième ligne")

# Lecture
with open("test.txt", "r") as f:
    contenu = f.read()
    print(contenu)
```

---
