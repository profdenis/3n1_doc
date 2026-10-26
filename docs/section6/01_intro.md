# Patrons de conception

Les _design patterns_ ou **patrons de conception** en français, sont des solutions générales réutilisables à des
problèmes communs rencontrés dans la conception logicielle. Ce sont essentiellement des _modèles_ ou des _schémas_
éprouvés qui peuvent aider à résoudre certains problèmes de conception spécifiques.

Ces patrons fournissent un moyen standard de résoudre des problèmes connus et récurrents, ce qui permet aux
développeurs de ne pas réinventer la roue à chaque fois qu'ils rencontrent ces problèmes.

Ils peuvent être classés en trois catégories principales :

1. **Patrons de création** : Ces patrons sont conçus pour aider à la création d'objets tout en cachant les détails de
   leur création. Ils encapsulent la connaissance sur quels objets concrets le système utilise, mais ils cachent
   également comment ces instances sont créées et mises ensemble. Des exemples incluent le _Singleton_, _Factory
   Method_, _Abstract Factory_, _Prototype_ et _Builder_.

2. **Patrons de structure** : Ces patrons concernent la composition de classes ou d'objets pour former de nouvelles
   structures plus grandes. Ils expliquent comment assembler les objets et les classes pour former des structures plus
   grandes. Des exemples incluent le _Adapter_, _Bridge_, _Composite_, _Decorator_, _Facade_, _Flyweight_ et _Proxy_.

3. **Patrons de comportement** : Ces patrons se concentrent sur l'interaction entre les objets, comment ils
   communiquent et comment certains objets sont contrôlés par d'autres. Des exemples incluent le _Chain of
   Responsibility_, _Command_, _Interpreter_, _Iterator_, _Mediator_, _Memento_, _Observer_ (ou _Publish/Subscribe_),
   _State_, _Strategy_, _Template Method_ et _Visitor_.

Les _design patterns_ sont un outil de communication puissant entre les développeurs. En disant, par exemple, "Utilisons
le patron Strategy ici", vous communiquez beaucoup d'informations sur la manière dont vous envisagez de résoudre
un problème de conception.

---

## L'Évolution des Design Patterns et l'Impact du Multiparadigme

L'arrivée des langages **multiparadigmes** (Python, Java moderne, Kotlin, ...) a radicalement modifié l'utilisation des
Design Patterns classiques décrits par le *Gang of Four (GoF)*.

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
    * Avec Qt/PySide6, on peut connecter une fonction à un signal sans avoir à créer une classe spécifique.
* **Le Pattern Strategy :**
    * *Avant :* On définissait une interface `Strategy` et plusieurs classes concrètes (ex: `CalculRapide`,
      `CalculLent`).
    * *Maintenant :* On passe directement une fonction de calcul en paramètre. L'objet n'a plus besoin de connaître la
      hiérarchie de classes, il a seulement besoin de savoir qu'il peut "appeler" cet objet.
    * Exemple en Python : pour trier une liste de nombres, on peut utiliser la fonction `sorted()` avec une fonction de
      comparaison personnalisée. Pas besoin de créer une classe spécifique (comme une implémentation de `Comparator` en
      Java) pour chaque stratégie de tri.

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