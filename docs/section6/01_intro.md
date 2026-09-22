# De l'Architecture Classique à l'Agilité des Langages Modernes

### *L'évolution des modèles de conception face à l'essor du multiparadigme*

---

## 1. Le Modèle MVC Classique : La Triade Fondamentale

L'architecture **MVC (Modèle-Vue-Contrôleur)** est née de la volonté de séparer la gestion des données de leur
représentation visuelle. L'idée est de diviser une application en trois composants distincts :

* **Le Modèle (Model) :** La "source de vérité". Il contient les données brutes et la logique métier (ex: calculs, accès
  à la base de données). Il ne sait pas comment il est affiché.
* **La Vue (View) :** La représentation visuelle des données. Elle "observe" le modèle et se met à jour quand celui-ci
  change.
* **Le Contrôleur (Controller) :** Le chef d'orchestre. Il reçoit les entrées utilisateur (clics, touches), les traduit
  en commandes et les transmet au Modèle ou à la Vue.

**Le problème historique :** Dans les langages de programmation strictement orientés-objets (comme les premières
versions de Java), le Contrôleur est une entité nécessaire pour faire le pont. Cela crée une séparation nette, mais
aussi une complexité structurelle importante (beaucoup de classes "intermédiaires").

---

## 2. L'approche Qt/PySide6 : Le modèle MVD

Dans les frameworks modernes comme **Qt (PySide6)**, le MVC a évolué vers le modèle **MVD (Modèle-Vue-Delegate)**. La
distinction est subtile mais fondamentale : le "Contrôleur" est en grande partie absorbé par deux mécanismes :

1. **Le mécanisme de Signal/Slot :** Il permet de lier une action (un signal) à une fonction (un slot) de manière
   extrêmement directe, rendant la classe "Contrôleur" souvent superflue.
2. **Le Déléguer (Delegate) :** Il gère à la fois l'affichage spécialisé (ex: une barre de progression dans une cellule)
   et l'interaction (l'édition d'une cellule).

---

## 3. L'Évolution des Design Patterns et l'Impact du Multiparadigme

L'arrivée des langages **multiparadigmes** (Python, C++, Java moderne) a radicalement modifié l'utilisation des Design
Patterns classiques décrits par le *Gang of Four (GoF)*.

### L'influence des fonctions de première classe

Dans les langages anciens, une fonction était un bloc de code rigide. Pour passer un comportement à un objet, il fallait
créer une classe entière pour encapsuler une seule méthode.

Avec l'introduction des **lambdas** et des **références de fonctions** (fonctions considérées comme des objets que l'on
peut passer en paramètre), de nombreux patterns de conception ont "disparu" ou ont été simplifiés, car le langage fait
maintenant le travail que le pattern faisait auparavant.

#### Exemples de simplification :

* **Le Pattern Command :**
    * *Avant :* On créait une classe `UndoCommand` avec une méthode `execute()`.
    * *Maintenant :* On passe simplement une fonction (ou une lambda) à un gestionnaire. Le pattern est devenu une
      simple instruction de langage.
* **Le Pattern Strategy :**
    * *Avant :* On définissait une interface `Strategy` et plusieurs classes concrètes (ex: `CalculRapide`,
      `CalculLent`).
    * *Maintenant :* On passe directement une fonction de calcul en paramètre. L'objet n'a plus besoin de connaître la
      hiérarchie de classes, il a seulement besoin de savoir qu'il peut "appeler" cet objet.

### Vers la Composition plutôt que l'Héritage

Cette évolution favorise un changement de philosophie majeur : **"La préférence pour la composition sur l'héritage"**.

Plutôt que de construire des hiérarchies de classes de plus en plus profondes et rigides (l'héritage), les développeurs
modernes préfèrent assembler des comportements de manière dynamique. On n'hérite plus d'un comportement, on
l'**injecte** sous forme de fonctions ou de petits objets spécialisés.

**Conclusion :**

Un Design Pattern n'est pas une règle absolue, mais une réponse à un besoin de structure. Si votre langage vous offre
déjà la flexibilité nécessaire via les fonctions et la composition, imposer un pattern complexe est une erreur de
conception.

*Dans la suite de ce cours, nous étudierons comment ces patterns s'adaptent précisément à ce nouveau paysage.*