# Exercices 1

### **Exercices sur Python (Niveau 1 : Bases)**

#### **1. Calculatrice interactive**

Écrivez un script qui demande à l'utilisateur deux nombres et une opération (`+`, `-`, `*`, `/`), puis affiche le
résultat.

- Gestion des erreurs (division par zéro).
- Utilisez `input()` pour lire les entrées.

**Exemple :**

```
Entrez le premier nombre : 10
Entrez le deuxième nombre : 5
Choisissez une opération (+, -, *, /) : /
Résultat : 2.0
```

---

#### **2. Conversion de température**

Écrivez un programme qui convertit des degrés Celsius en Fahrenheit et vice versa.

- Formule : `F = C × 9/5 + 32` (Celsius → Fahrenheit).
- Utilisez une condition pour choisir la direction de conversion.

**Exemple :**

```
1. Celsius vers Fahrenheit
2. Fahrenheit vers Celsius
Choix : 1
Température en Celsius : 20
Résultat : 68.0 °F
```

---

#### **3. Mot de passe sécurisé**

Demandez à l'utilisateur un mot de passe et vérifiez s'il est "sécurisé" (longueur ≥ 8 et contient au moins une
majuscule, un chiffre).

- Utilisez des conditions imbriquées.

**Exemple :**

```
Entrez un mot de passe : Secr3t
Mot de passe sécurisé ! ✅
```

---

#### **4. Table de multiplication**

Écrivez un programme qui affiche la table de multiplication d'un nombre donné (par exemple, 7) jusqu'à 10.

- Utilisez une boucle `for` ou `while`.

**Exemple :**

```
Table de 7 :
7 × 1 = 7
7 × 2 = 14
...
7 × 10 = 70
```

---

#### **5. Jeu "Devine le nombre"**

Le programme génère un nombre aléatoire entre 1 et 100, et l'utilisateur doit le deviner.

- Donnez des indices ("Trop grand", "Trop petit").
- Comptez le nombre d'essais.

**Exemple :**

```
Je pense à un nombre entre 1 et 100. Devinez-le !
Votre essai : 50
Trop petit ! Essayez plus haut.
Votre essai : 75
Trop grand ! Essayez plus bas.
...
Bravo ! Vous avez trouvé en 4 essais.
```

---

### **Exercices sur les fonctions (Niveau 2)**

#### **6. Fonction de factorielle**

Écrivez une fonction `factorielle(n)` qui calcule la factorielle d'un nombre entier positif (
`n! = n × (n-1) × ... × 1`).

- Gestion des erreurs si `n < 0`.

**Exemple :**

```python
print(factorielle(5))  # 120
```

---

#### **7. Fonction de somme de chiffres**

Écrivez une fonction `somme_chiffres(n)` qui retourne la somme des chiffres d'un nombre entier.

- Exemple : `somme_chiffres(123)` → `6` (1 + 2 + 3).

---

#### **8. Fonction de palindrome**

Une chaîne est un palindrome si elle se lit de la même manière à l'envers (ex: "radar").
Écrivez une fonction `est_palindrome(s)` qui retourne `True` ou `False`.

**Exemple :**

```python
print(est_palindrome("radar"))  # True
print(est_palindrome("python"))  # False
```

---

#### **9. Fonction récursive**

Écrivez une fonction récursive `fibonacci(n)` qui retourne le n-ième nombre de la suite de Fibonacci (
`0, 1, 1, 2, 3, 5, ...`).

**Exemple :**

```python
print(fibonacci(6))  # 5
```

---

### **Exercices sur les modules (Niveau 3)**

#### **10. Utilisation de `math`**

Écrivez un programme qui :

- Calcule l'aire d'un cercle (`π × r²`) en utilisant `math.pi`.
- Calcule la racine carrée d'un nombre avec `math.sqrt()`.

**Exemple :**

```python
import math

rayon = 5
aire = math.pi * rayon ** 2
print(f"Aire du cercle : {aire:.2f}")  # 78.54
```

---

#### **11. Générateur de mots aléatoires**

Utilisez le module `random` pour :

- Générer un mot aléatoire parmi une liste de mots (ex: `["pomme", "banane", "cerise"]`).
- Affichez un message comme : `"Le mot du jour est : banane"`.

---

#### **12. Module personnalisé**

Créez deux fichiers :

1. `utils.py` contenant une fonction `soustraction(a, b)`.
2. `main.py` qui importe et utilise cette fonction.

**Contenu de `utils.py` :**

```python
def soustraction(a, b):
    return a - b
```

**Contenu de `main.py` :**

```python
from utils import soustraction

resultat = soustraction(10, 3)
print(resultat)  # 7
```
