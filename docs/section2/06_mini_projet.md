# Mini-Projet : Le Gestionnaire de Compagnons de Donjon

## 1. Le Concept

L'objectif est de créer un programme qui permet de gérer une équipe de héros (Guerriers, Mages, Archers) qui partent
explorer un donjon. On doit pouvoir ajouter des héros, les faire agir, et sauvegarder/charger l'état de l'équipe dans un
fichier texte pour ne pas perdre la progression.

## 2. Structure des Classes (L'architecture OO)

Le projet repose sur une hiérarchie de classes :

1. **Classe de base : `Hero`**
    * **Attributs :** `nom` (string), `points_de_vie` (int).
    * **Méthodes :**
        * `__init__` : Initialise le nom et les PV (points de vie).
        * `__repr__` : Doit retourner une chaîne de caractères formatée pour la sauvegarde (ex: `Hero|Aragorn|100`).
        * `action()` : Une méthode qui affiche un message générique (ex: "[Nom] se prépare...").

2. **Classes enfants (Héritage) :**
    * **Classe `Guerrier` (hérite de `Hero`) :**
        * **Attribut :** `force` (int).
        * **`__init__`** : Appelle `super().__init__` et initialise la force.
        * **`__repr__`** : Retourne le type, le nom, les PV et la force (ex: `Guerrier|Aragorn|100|15`).
        * **`action()`** (Polymorphisme) : Affiche "[Nom] donne un coup d'épée puissant !"
    * **Classe `Magicien` (hérite de `Hero`) :**
        * **Attribut :** `mana` (int).
        * **`__init__`** : Appelle `super().__init__` et initialise le mana.
        * **`__repr__`** : Retourne le type, le nom, les PV et le mana (ex: `Magicien|Gandalf|80|50`).
        * **`action()`** (Polymorphisme) : Affiche "[Nom] lance un sort de feu !"

## 3. La Persistance (Fichiers Texte)

Le fichier de sauvegarde (ex: `donjon.txt`) doit utiliser le format `Type|Nom|PV|AttributSpecial`. *Exemple de contenu
du fichier :*

```text
Guerrier|Thorin|120|20
Magicien|Saruman|70|60
Guerrier|Boromir|90|15
```

**Fonctions de gestion de fichier :**

* **`sauvegarder(liste_heros, nom_fichier)`** : Parcourt la liste des objets et écrit chaque `repr(objet)` sur une
  nouvelle ligne dans le fichier.
* **`charger(nom_fichier)`** : Lit le fichier ligne par ligne. Pour chaque ligne :
    1. On découpe la ligne avec le séparateur `|`.
    2. On regarde le premier élément (le type).
    3. On recrée l'objet correspondant avec les autres informations (en convertissant les nombres en `int`).
    4. On retourne la liste des objets recréés.

## 4. L'Interface Console (Le Menu)

Le programme doit tourner dans une boucle `while` et proposer les options suivantes :

1. **Afficher l'équipe** : Parcourt la liste et affiche les informations de chaque héros (vous pouvez redéfinir 
   `__str__` dans chaque classe et l'utiliser pour l'affichage).
2. **Ajouter un héros** : Demander à l'utilisateur le type (1: Guerrier, 2: Magicien), le nom, et les statistiques de
   base.
3. **Faire agir l'équipe (Polymorphisme)** : Parcourir la liste des héros et appeler la méthode `.action()` de chacun.
4. **Sauvegarder l'équipe** : Écrire la liste dans le fichier.
5. **Charger l'équipe** : Lire le fichier et remplacer la liste actuelle par celle chargée.
6. **Quitter**.

---

## 5. Extensions

Si vous avez terminé le projet et que vous souhaitez aller plus loin, voici deux défis supplémentaires pour tester votre
logique :

**1. Ajout de la classe `Archer` (Héritage)**

* Créez une nouvelle classe enfant `Archer` qui hérite de `Hero`.
* L'archer possède un attribut unique : `portee` (la distance de tir).
* Redéfinissez sa méthode `__repr__` pour inclure cette donnée afin qu'elle soit sauvegardable dans le fichier.
* Redéfinissez sa méthode `action()` pour qu'elle affiche : *"[Nom] tire une flèche à une distance de [portee]
  mètres !"*

**2. Gestion de la survie et des dégâts (Logique métier)**

* **Méthode de dégâts :** Ajoutez une méthode `recevoir_degats(montant)` dans la classe parente `Hero`. Cette méthode
  doit soustraire le montant des `points_de_vie` actuels.
* **État de santé :** Un héros est considéré comme "Inconscient" si ses `points_de_vie` tombent à 0 ou moins.
* **Affichage dynamique :** Modifiez la façon dont l'équipe est affichée (dans les `__str__`) pour qu'un héros dont les
  PV sont $\le 0$ soit affiché avec la mention **"(Inconscient)"** à côté de son nom.
* **Conséquence :** Modifiez la méthode `action()` de chaque classe pour que, si le héros est "Inconscient", il ne
  puisse plus agir (le message d'action ne doit pas s'afficher).

---