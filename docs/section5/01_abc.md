# **Classes Abstraites (ABC)**

## **1. Introduction aux ABC (Abstract Base Classes)**

En Python, une **classe abstraite** est une classe qui ne peut pas être instanciée directement et qui définit des
**méthodes abstraites** (sans implémentation). Elle sert de **modèle pour d'autres classes**.

### **Comparaison avec Java**

| Concept           | Java                       | Python                                                  |
|-------------------|----------------------------|---------------------------------------------------------|
| Classe abstraite  | `abstract class`           | `@abstractmethod` dans une classe régulière ou une ABC. |
| Méthode abstraite | `abstract void methode();` | `@abstractmethod def methode(): ...`.                   |

---

## **2. Création d'une ABC en Python**

### **Méthode 1 : Avec le module `abc` (recommandé)**

```python
from abc import ABC, abstractmethod


class Forme(ABC):  # Héritage de ABC pour marquer comme abstraite
    @abstractmethod
    def aire(self) -> float:
        pass  # Pas d'implémentation ici

    @abstractmethod
    def perimetre(self) -> float:
        pass


# Utilisation :
class Cercle(Forme):
    def __init__(self, rayon):
        self.rayon = rayon

    def aire(self) -> float:  # Implémentation obligatoire
        return 3.14 * self.rayon ** 2

    def perimetre(self) -> float:
        return 2 * 3.14 * self.rayon


# Test :
cercle = Cercle(5)
print(cercle.aire())  # Affiche : 78.5
```

### **Méthode 2 : Sans `abc` (moins recommandé)**

```python
class Forme:
    def aire(self) -> float:
        raise NotImplementedError("Méthode non implémentée")


# Utilisation :
class Carre(Forme):
    def __init__(self, cote):
        self.cote = cote

    def aire(self) -> float:  # Implémentation obligatoire
        return self.cote ** 2


# Test :
carre = Carre(4)
print(carre.aire())  # Affiche : 16
```

---

## **3. Règles des ABC**

1. **Une classe avec au moins une `@abstractmethod` ne peut pas être instanciée.**
   ```python
   forme = Forme()  # Lève TypeError: Can't instantiate abstract class
   ```

2. **Les sous-classes doivent implémenter toutes les méthodes abstraites.**
   ```python
   class Triangle(Forme):  # Oublie de définir `perimetre`
       def aire(self) -> float:
           return 10

   triangle = Triangle()  # Lève TypeError: Can't instantiate abstract class
   ```

3. **Une sous-classe peut ajouter des méthodes non abstraites.**
   ```python
   class Rectangle(Forme):
       def aire(self) -> float:
           return self.largeur * self.hauteur

       def perimetre(self) -> float:
           return 2 * (self.largeur + self.hauteur)

       def est_carre(self) -> bool:  # Méthode supplémentaire
           return self.largeur == self.hauteur
   ```

---

## **4. Avantages des ABC**

- ✅ **Forcer une structure commune** entre les classes dérivées.
- ✅ **Documenter clairement les méthodes obligatoires**.
- ✅ **Éviter les erreurs d'implémentation** (Python lève une erreur si une méthode abstraite est oubliée).

---

## **5. Exemple complet : Système de formes géométriques**

```python
from abc import ABC, abstractmethod


class Forme(ABC):
    @abstractmethod
    def aire(self) -> float:
        pass

    @abstractmethod
    def perimetre(self) -> float:
        pass


class Cercle(Forme):
    def __init__(self, rayon: float):
        self.rayon = rayon

    def aire(self) -> float:
        return 3.14 * self.rayon ** 2

    def perimetre(self) -> float:
        return 2 * 3.14 * self.rayon


class Rectangle(Forme):
    def __init__(self, largeur: float, hauteur: float):
        self.largeur = largeur
        self.hauteur = hauteur

    def aire(self) -> float:
        return self.largeur * self.hauteur

    def perimetre(self) -> float:
        return 2 * (self.largeur + self.hauteur)


# Test :
formes = [Cercle(5), Rectangle(4, 6)]
for forme in formes:
    print(f"Aire: {forme.aire()}, Périmètre: {forme.perimetre()}")
```

---

## **6. Bonnes pratiques**

- ✅ **Utilisez `@abstractmethod` pour les méthodes qui doivent être redéfinies.**
- ✅ **Documentez les ABC avec des commentaires** (ex: "Cette classe doit être héritée").
- ❌ **Évitez de mélanger méthodes abstraites et concrètes dans une même classe** (sauf si nécessaire).

!!! warning "Ne faites pas d'extension de `dict`"

      Ne faites pas d'extension de la classe `dict` pour étendre ses fonctionnalités. Cela pourrait créer des problèmes car
      `dict` a été optimisée pour de meilleures performaces, avec une partie de son code écrite en C. Ces optimisations
      peuvent causer des problèmes dans les sous-classes.
      Voir [cet page](01a_dict.md) pour plus d'informations.

---

## **7. Exercice pour les étudiants**

### **Consigne**

Créez une hiérarchie de classes pour un système de véhicules :

1. Une classe abstraite `Vehicule` avec des méthodes abstraites `demarrer()` et `arreter()`.
2. Deux sous-classes : `Voiture` et `Moto`, qui implémentent ces méthodes.

**Bonus :**

- Ajoutez une méthode `afficher_infos()` dans chaque sous-classe pour afficher le type de véhicule.

---

## **8. Ressources supplémentaires**

- [Documentation officielle Python sur `abc`](https://docs.python.org/3/library/abc.html)
- [Tutoriel ABC pour débutants](https://realpython.com/python-abstract-classes/)

---

### **Résumé final**

| Concept           | Java                       | Python                                |
|-------------------|----------------------------|---------------------------------------|
| Classe abstraite  | `abstract class`           | Classe héritant de `ABC`.             |
| Méthode abstraite | `abstract void methode();` | `@abstractmethod def methode(): ...`. |

**Points clés :**

- Une ABC ne peut pas être instanciée.
- Les sous-classes doivent implémenter toutes les méthodes abstraites.
- Utilisez `@abstractmethod` pour définir des méthodes obligatoires.

