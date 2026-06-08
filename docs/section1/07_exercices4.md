# Exercices 4

## **Exercices de Base**

### **1. Longueur et accès aux caractères**

Écrivez un programme qui :

- Affiche la longueur de la chaîne `"Bonjour"`.
- Affiche le premier et le dernier caractère.

**Résultat attendu :**

```
Longueur : 7
Premier caractère : B
Dernier caractère : r
```

---

### **2. Conversion de casse**

Étant donné la chaîne `"PyThOn"`, affichez :

- Sa version en minuscules.
- Sa version en majuscules.

**Résultat attendu :**

```
minuscules : python
majuscules : PYTHON
```

---

### **3. Suppression d'espaces**

Nettoyez la chaîne `"   Bonjour   "` pour qu'elle n'ait plus d'espaces avant/après.

**Résultat attendu :**

```
"Bonjour"
```

---

## **Exercices Intermédiaires**

### **4. Découpage (`split`)**

Découpez la phrase `"Bonjour, monde!"` en une liste de mots (en utilisant l'espace comme séparateur).

**Résultat attendu :**

```python
["Bonjour,", "monde!"]
```

---

### **5. Concaténation (`join`)**

À partir de la liste `["Bonjour", "monde"]`, créez une chaîne `"Bonjour-monde"` en utilisant `-` comme séparateur.

**Résultat attendu :**

```
"Bonjour-monde"
```

---

### **6. Recherche et remplacement**

Étant donné la chaîne `"Hello, world!"` :

- Trouvez la position de `"world"`.
- Remplacez `"world"` par `"Python"`.

**Résultat attendu :**

```
Position : 7
Nouvelle chaîne : "Hello, Python!"
```

---

## **Exercices Avancés**

### **7. Compteur de mots**

Écrivez une fonction `compter_mots(phrase)` qui retourne le nombre de mots dans une phrase.
**Indice :** Utilisez `split()`.

**Exemple :**

```python
print(compter_mots("Bonjour monde!"))  # 2
```

---

### **8. Censurer un mot**

Écrivez une fonction `censurer(texte, mot)` qui remplace toutes les occurrences de `mot` par `***`.
**Exemple :**

```python
print(censurer("Bonjour monde, bonjour Python", "bonjour"))
# "*** monde, *** Python"
```

---

### **9. Vérification de contenu**

Écrivez une fonction `est_valide(mot_de_passe)` qui vérifie si un mot de passe :

- A au moins 8 caractères.
- Contient au moins une majuscule et un chiffre.

**Exemple :**

```python
print(est_valide("Secr3t"))  # False (trop court)
print(est_valide("Secr3t!"))  # True
```

---

## **Exercices Défi**

### **10. Formatage de texte**

Étant donné une liste `[("Alice", 25), ("Bob", 30)]`, générez la chaîne suivante :

```
Nom : Alice, Âge : 25
Nom : Bob, Âge : 30
```

---

### **11. Nettoyage avancé**

Écrivez une fonction `nettoyer_texte(texte)` qui :

- Supprime les espaces en début/fin.
- Remplace les tabulations par des espaces.
- Convertit la chaîne en minuscules.

**Exemple :**

```python
print(nettoyer_texte("\t  Bonjour\t"))
# "bonjour"
```

---

### **12. Jeu de devinette**

Modifiez l'exercice "Devine le nombre" pour :

- Accepter des réponses comme `"plus"` ou `"moins"` au lieu de nombres.
- Convertir les entrées en minuscules avant comparaison.

**Exemple :**

```
Je pense à un nombre entre 1 et 100. Devinez-le !
Votre essai : plus
Trop petit ! Essayez plus haut.
```

---

## **Corrigés Partiels**

### **Exercice 4 (`split`) :**

```python
phrase = "Bonjour, monde!"
mots = phrase.split()
print(mots)  # ["Bonjour,", "monde!"]
```

### **Exercice 8 (Censurer un mot) :**

```python
def censurer(texte, mot):
    return texte.replace(mot, "***")
```

---

## **Conseils pour les Étudiants**

- **Testez dans le REPL** : Utilisez `python` en ligne de commande pour vérifier rapidement vos fonctions.
- **Comparez avec des boucles** : Par exemple, pour compter les mots, comparez une solution avec `split()` et une boucle
  manuelle.
- **Utilisez `help(str)`** dans le REPL pour voir toutes les méthodes disponibles sur les chaînes.

Ces exercices couvrent les cas d'usage courants et permettent de bien maîtriser la manipulation des chaînes en Python.
Bonne pratique ! 🚀