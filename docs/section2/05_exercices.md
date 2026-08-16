# Exercices

## **Exercices de Base (Héritage Simple)**

### **1. Classe `Animal` et Sous-Classes**

Créez une classe `Animal` avec :

- Un constructeur pour `nom`.
- Une méthode `faire_son()` qui retourne `"Un son indéfini"`.

Puis créez deux sous-classes :

- `Chien` : redéfinissez `faire_son()` pour retourner `"Wouf!"`.
- `Chat` : redéfinissez `faire_son()` pour retourner `"Miaou!"`.

**Exemple :**

```python
animaux = [Chien("Rex"), Chat("Felix")]
for animal in animaux:
    print(animal.faire_son())  # "Wouf!" puis "Miaou!"
```

---

### **2. Classe `Forme` et Sous-Classes**

Créez une classe `Forme` avec :

- Une méthode `aire()` qui retourne `0`.
  Puis deux sous-classes :
- `Cercle(radius)` : calcule l'aire (`π × r²`).
- `Rectangle(largeur, hauteur)` : calcule l'aire (`largeur × hauteur`).

**Exemple :**

```python
formes = [Cercle(5), Rectangle(4, 6)]
for forme in formes:
    print(f"Aire: {forme.aire()}")  # ~78.5 puis 24
```

---

## **Exercices Intermédiaires (Polymorphisme)**

### **3. Polymorphisme avec `match`**

Étant donné les classes de l'exercice 1, écrivez une fonction `decrire_animal(animal)` qui utilise `match` pour :

- Afficher `"C'est un chien"` si c'est un `Chien`.
- Afficher `"C'est un chat"` si c'est un `Chat`.
- Sinon afficher `"Autre animal"`.

**Exemple :**

```python
print(decrire_animal(Chien("Rex")))  # "C'est un chien"
```

---

### **4. Polymorphisme avec Méthodes Abstraites**

Modifiez l'exercice 2 pour simuler une méthode abstraite `aire()` dans `Forme` (en Python, utilisez une exception si non
redéfinie). Les vraies méthodes abstraites (avec le décorateur `@abstractmethod`) seront présentées dans la section sur
la programmation OO avancée.

**Exemple :**

```python
try:
    forme = Forme()
    print(forme.aire())
except NotImplementedError:
    print("Erreur: aire() non implémentée!")
```

---

## **Exercices Avancés (Duck Typing + Match)**

### **5. Duck Typing avec `match`**

Créez deux classes sans héritage :

- `Voiture` : méthode `deplacer()` → `"La voiture roule"`.
- `Avion` : méthode `deplacer()` → `"L'avion vole"`.

Écrivez une fonction `decrire_deplacement(obj)` qui utilise `match` pour afficher le message approprié.

**Exemple :**

```python
print(decrire_deplacement(Voiture()))  # "La voiture roule"
```

---

### **6. Système de Paiement (Polymorphisme)**

Créez une classe `Paiement` avec :

- Une méthode `traiter()` qui retourne `"Paiement non supporté"`.

Puis deux sous-classes :

- `CarteCredit` : `traiter()` → `"Paiement par carte"`.
- `PayPal` : `traiter()` → `"Paiement PayPal"`.

Utilisez `match` pour afficher le type de paiement.

**Exemple :**

```python
paiements = [CarteCredit(), PayPal()]
for paiement in paiements:
    print(paiement.traiter())  # "Paiement par carte", puis "Paiement PayPal"
```

---

## **Exercices Défi (Combinaisons)**

### **7. Jeu de Rôle avec `match`**

Créez un système simple avec :

- `Personnage(nom, points_de_vie)`.
- Sous-classes : `Guerrier`, `Mage`.
- Chaque classe redéfinit `attaquer()` et `__str__()`.

Utilisez `match` pour afficher les statistiques d'un personnage.

**Exemple :**

```python
guerrier = Guerrier("Aragorn", 100)
print(guerrier.attaquer())  # "Attaque avec une épée!"
```

---

### **8. Système de Fichiers (Duck Typing)**

Créez des classes `FichierTexte` et `FichierImage` sans héritage, chacune avec :

- `lire()` : retourne le contenu.
- `taille()` : retourne la taille.

Utilisez `match` pour afficher le type de fichier.

**Exemple :**

```python
fichiers = [FichierTexte("data.txt"), FichierImage("photo.jpg")]
for fichier in fichiers:
    print(f"Type: {type(fichier).__name__}")  # "FichierTexte", puis "FichierImage"
```

---

## **Exercices supplémentaires**

Remplacez l'utilisation de `match` par des méthodes dans les différentes classes, et utilisez le polymorphisme pour 
appeler ces méthodes. 


## **Conseils pour les Étudiants**

- Pour le `duck typing`, concentrez-vous sur **les méthodes** plutôt que sur l'héritage.
- Utilisez `match` pour remplacer les chaînes d'`if isinstance()`.
- Testez vos solutions avec des objets de types inattendus (cas par défaut).
