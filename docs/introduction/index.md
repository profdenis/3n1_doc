Voici une proposition de notes de cours structurées pour ton introduction. Elles sont conçues pour être projetées ou
distribuées, avec un ton qui invite à la réflexion plutôt qu'à la simple mémorisation.

---

# Introduction à la Programmation Orientée Objet (POO 2)

## De la Taxonomie à l'Ingénierie des Systèmes

### 1. Objectif du cours

L'objectif de ce cours n'est pas d'apprendre un nouveau langage, mais de passer du statut de **"codeur"** (quelqu'un qui
écrit de la syntaxe) à celui d'**"ingénieur logiciel"** (quelqu'un qui conçoit des systèmes robustes, évolutifs et
maintenables).

Nous utiliserons **Python** comme laboratoire d'expérimentation, non pas pour sa syntaxe, mais pour sa flexibilité qui
permet d'illustrer les grands principes de conception.

---

### 2. Perspective Historique : Deux visions de l'Objet

L'Orienté-Objet n'a pas une seule définition unique. L'histoire de l'informatique est marquée par la confrontation de
deux courants de pensée majeurs.

| Caractéristique | École du **Message Passing** (ex: Smalltalk)   | École de la **Hiérarchie** (ex: Simula, C++, Java) |
|:----------------|:-----------------------------------------------|:---------------------------------------------------|
| **Métaphore**   | Biologique (cellules communiquant entre elles) | Taxonomique (classification du monde réel)         |
| **Concept clé** | **Le Comportement** (ce que l'objet *fait*)    | **La Structure** (ce que l'objet *est*)            |
| **Mécanisme**   | Envoi de messages à des entités autonomes      | Appels de méthodes sur des hiérarchies de classes  |
| **Philosophie** | L'objet est une boîte noire qui réagit         | L'objet est une branche dans un arbre généalogique |
| **Force**       | Flexibilité extrême, polymorphisme dynamique   | Organisation rigide, prévisibilité, réutilisation  |


!!! note "Note importante"
    Le courant de la "Hiérarchie" a dominé l'industrie pendant des décennies. C'est ce que la
    plupart des gens appellent "faire de l'OO". Mais cette vision a ses limites face à la complexité moderne.

---

### 3. Le Mythe : OO $\neq$ Héritage

Une erreur commune est de croire que l'Orienté-Objet se résume à créer des arbres d'héritage complexes.

* **L'Héritage (*Is-a*) :** "Un Chien **est un** Animal". C'est une relation de parenté rigide.
* **La Composition (*Has-a*) :** "Une Voiture **a un** Moteur". C'est une relation d'assemblage.

#### Pourquoi l'industrie s'éloigne de l'héritage massif ?

1. **Le couplage fort :** Modifier la classe parente peut briser involontairement des dizaines de classes enfants (le
   problème de la *Fragile Base Class*).
2. **L'explosion combinatoire :** Si un objet doit appartenir à plusieurs catégories, l'héritage devient un cauchemar (
   le *Problème du Diamant*).
3. **La rigidité :** L'héritage définit la nature d'un objet au moment de la compilation. On ne peut pas changer sa "
   nature" durant l'exécution.

**Le paradigme moderne privilégie la Composition et les Interfaces (ou Protocoles) :** on ne définit plus ce qu'un objet
*est*, mais ce qu'il est capable de *faire*.

---

### 4. La Boussole du Développeur : Les principes SOLID

Pour éviter que le code ne devienne un chaos ingérable, nous utiliserons les principes **SOLID** comme boussole de
conception. Nous reviendrons sur chacun d'eux tout au long du semestre.

* **S - Single Responsibility (SRP) :** Une classe/fonction ne doit avoir qu'une seule raison de changer.
* **O - Open/Closed (OCP) :** Un logiciel doit être ouvert à l'extension, mais fermé à la modification.
* **L - Liskov Substitution (LSP) :** Une sous-classe doit pouvoir remplacer sa classe de base sans casser le système.
* **I - Interface Segregation (ISP) :** Il vaut mieux plusieurs petites interfaces spécialisées qu'une seule grosse
  interface généraliste.
* **D - Dependency Inversion (DIP) :** Dépendre des abstractions (interfaces), pas des implémentations concrètes.

---

### 5. Vers une approche Multi-Paradigme et Data-Centric

Le monde logiciel actuel ne se limite plus à l'OO pur. Nous allons naviguer entre plusieurs approches :

1. **L'approche Objet (Comportement) :** Pour orchestrer la logique métier.
2. **L'approche Fonctionnelle (Données immuables) :** Pour traiter les données de manière prévisible et sans effets de
   bord.
3. **L'approche Data-Centric (Contrats) :** Utiliser des structures de données claires (comme les `dataclasses` en
   Python ou les `records` en Java) qui servent de contrats entre le Backend, l'API et le Frontend.

### Résumé du contrat d'apprentissage

| Ce que nous allons faire                         | Ce que nous ne ferons pas                                  |
|:-------------------------------------------------|:-----------------------------------------------------------|
| Apprendre à concevoir des systèmes robustes      | Apprendre par cœur une syntaxe de langage                  |
| Utiliser Python pour illustrer des concepts      | Faire du script de base sans structure                     |
| Pratiquer l'injection de dépendances             | Créer des hiérarchies d'héritage rigides                   |
| Appliquer les principes SOLID de façon itérative | Chercher la "pureté" théorique au détriment du pragmatisme |

---

!!! note "Sagesse populaire"
    *« La complexité est inévitable, mais le chaos est optionnel. »*
    

Le monde du logiciel est complexe. Vous ne pourrez jamais construire quelque chose de simple. Mais vous avez le choix :
soit vous laissez cette complexité devenir un chaos qui rendra votre vie impossible, soit vous utilisez les outils (
SOLID, Composition, Tests) pour dompter ce chaos et transformer la complexité en un système organisé.