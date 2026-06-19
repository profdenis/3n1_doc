# Principes OO

## Clean Code : A Handbook of Agile Software Craftsmanship

Ce livre influent, écrit par Robert C. Martin, qui est également connu sous le nom de "Uncle Bob". L'objectif de ce
livre est d'enseigner aux développeurs de logiciels les principes de l'écriture de logiciels de haute qualité. Voici un
bref résumé de certains des concepts clés présentés dans le livre :

1. **Code propre** : L'auteur définit le "code propre" comme un code qui a été écrit par quelqu'un qui se soucie
   réellement de son travail. Pour lui, un bon code peut être lu et amélioré par d'autres développeurs, et a une
   structure claire.

2. **Noms significatifs** : Les noms pour les fonctions, les variables et les classes doivent être clairs et précis. Ils
   devraient révéler leur intention et ne laisser aucune place à l'ambiguïté.

3. **Fonctions** : Les fonctions doivent être petites et ne faire qu'une seule chose. Elles devraient seulement avoir un
   niveau d'abstraction et les commentaires doivent être évités autant que possible. L'auteur explique en détail comment
   créer des fonctions efficaces.

4. **Commentaires** : En règle générale, les commentaires devraient être évités. Un bon code est auto-documenté. Si vous
   devez écrire des commentaires pour expliquer votre code, il serait préférable de le réécrire.

5. **Formattage** : Il est essentiel d'avoir un bon format pour votre code. Un bon format facilite la lisibilité et la
   compréhension du code.

6. **Gestion des erreurs** : L'auteur suggère que les erreurs doivent être gérées correctement en utilisant des
   exceptions plutôt que des codes d'erreur retournés.

7. **Répétition de code** : La répétition de code est une mauvaise habitude qui peut rendre votre code ennuyeux et
   difficile à maintenir. Utiliser des abstractions et des méthodes pour éviter la duplication du code.

8. **Principes SOLID** : Il explique également certains principes de la conception orientée objet, tels que les
   principes SOLID : _Single Responsibility_, _Open/Closed_, _Liskov Substitution_, _Interface Segregation_ et
   _Dependency Inversion_.

9. **Code smells et refactorisation** : Le livre présente également différentes "odeurs de code" (_code smells_) qui
   indiquent d'éventuels problèmes de conception du code et montre comment ces problèmes peuvent être résolus par le
   refactorisation.

En résumé, "Clean Code" est une ressource précieuse pour tout développeur de logiciels cherchant à améliorer ses
compétences en codage et à écrire des logiciels de meilleure qualité.

## SOLID

[https://en.wikipedia.org/wiki/SOLID](https://en.wikipedia.org/wiki/SOLID)

[https://fr.wikipedia.org/wiki/SOLID_(informatique)](https://fr.wikipedia.org/wiki/SOLID_(informatique))

**SOLID** est un acronyme pour un ensemble de cinq principes de conception de logiciels orientés objet qui aident à
rendre les systèmes de logiciels plus compréhensibles, flexibles et maintenables. Voici ce que chaque lettre de
l'acronyme SOLID signifie :

1. **S - Principe de Responsabilité Unique (Single Responsibility Principle)** : Ce principe stipule qu'une classe ou un
   module devrait avoir une, et seulement une, raison de changer. En d'autres termes, une classe ou un module devrait
   avoir une seule responsabilité ou tâche.

2. **O - Principe ouvert/fermé (Open/Closed Principle)** : Ce principe stipule que les entités logicielles (classes,
   modules, fonctions, etc.) devraient être ouvertes à l'extension, mais fermées à la modification. Cela signifie que
   vous devriez être capable d'ajouter de nouvelles fonctionnalités à une entité sans modifier son code source.

3. **L - Principe de substitution de Liskov (Liskov Substitution Principle)** : Ce principe stipule que dans un
   programme, les objets d'une superclasse devraient pouvoir être remplacés par des objets d'une sous-classe
   sans affecter l'exactitude de ce programme.

4. **I - Principe de ségregation d'interface (Interface Segregation Principle)** : Ce principe stipule que les clients
   ne devraient pas être forcés de dépendre des interfaces qu'ils n'utilisent pas.

5. **D - Principe d'inversion de dépendance (Dependency Inversion Principle)** : Ce principe stipule que les modules de
   haut niveau ne devraient pas dépendre des modules de bas niveau. Les deux devraient dépendre des abstractions.

Suivre ces principes peut aider à éviter les mauvaises pratiques de conception, à réduire le couplage dans le code, à
rendre le code plus facile à maintenir et à améliorer la lisibilité et la reproductibilité du code.

### Responsabilité unique (Single responsibility principle SRP)

_Une classe, une fonction ou une méthode doit avoir une et une seule responsabilité._

Selon le principe de responsabilité unique, une classe, un module ou une fonction ne devrait avoir qu'une seule raison
de changer. Autrement dit, chaque entité logicielle doit être responsable d'un seul aspect particulier de la
fonctionnalité du logiciel.

Pour donner un exemple, supposons que vous ayez un objet dans votre application qui gère la logique de manipulation des
utilisateurs (c'est-à-dire, l'ajout, la suppression et la mise à jour des utilisateurs). Si ce même objet est aussi
responsable de l'affichage des utilisateurs à l'écran, alors il a deux raisons de changer : une raison technique (
modification du code pour manipuler les utilisateurs différemment) et une raison esthétique (modification du code pour
changer l'affichage des utilisateurs à l'écran). C'est une violation du principe SRP.

Ce principe encourage à séparer les préoccupations pour améliorer la lisibilité et la maintenabilité

### Ouvert/fermé (Open/closed principle)

_Une entité applicative (classe, fonction, module ...) doit être fermée à la modification directe, mais ouverte à
l'extension._

Le principe Ouvert/fermé, souvent abrégé en OCP (Open/Closed Principle), est un concept important en programmation
orientée objet, et est l'un des cinq principes fondamentaux du SOLID, un acronyme pour un ensemble de principes de
conception orientée objet conçus pour rendre le code plus compréhensible, flexible et maintenable.

Selon le principe Ouvert/fermé, souvent abrégé en OCP (Open/Closed Principle), les entités logicielles (classes,
modules, fonctions, etc.) doivent être ouvertes à l'extension, mais fermées à la modification. Cela signifie que vous
devriez pouvoir ajouter de nouvelles fonctionnalités ou comportements à une entité sans avoir à modifier son code
source.

L'intention est de réduire le risque de nouvelles erreurs et réduire les dépendances dans le système. De cette façon,
lorsque nous ajoutons de nouvelles fonctionnalités ou changeons le comportement du système, nous ajoutons du nouveau
code (extension), nous n'avons pas besoin de modifier le code existant (fermé pour modification).

Un exemple de la manière d'appliquer l'OCP est l'utilisation de **polymorphisme** où la classe de base reste la même et
de nouvelles fonctionnalités sont ajoutées en créant de nouvelles classes qui héritent de la classe de base.

### Substitution de Liskov (Liskov substitution principle)

_Une instance de type `T` doit pouvoir être remplacée par une instance de type `G`, tel que `G` sous-type de `T`, sans
que cela modifie la cohérence du programme_.

Ce principe a été introduit par Barbara Liskov en 1987 lors d'une conférence. Le principe stipule que si une classe `B`
hérite d'une classe `A`, alors nous devrions être capables de remplacer `A` par `B` sans affecter le comportement de
notre programme. C'est-à-dire, un objet de type superclasse peut être remplacé par un objet de type sous-classe sans
perturber l'exactitude ou le comportement du programme.

Par exemple, considérons une classe `Oiseau` qui a une méthode `voler`. Maintenant, considérons une
sous-classe `Pingouin`, qui est un type d'oiseau, mais qui ne peut pas voler. Selon le principe de substitution de
Liskov, nous devrions pouvoir utiliser un objet `Pingouin` là où nous utilisons un objet `Oiseau` dans notre programme.
Cependant, si notre programme attend que les oiseaux puissent voler, alors cette substitution causerait un problème, car
les pingouins ne peuvent pas voler. C'est une violation du principe de substitution de Liskov.

En substance, le principe de substitution de Liskov encourage à assurer que les sous-classes soient absolument
substituables par leurs superclasses sans altérer la logique du programme. Solliciter ce principe lors de la conception
de logiciels aide à garantir la polymorphie et augmente la réutilisabilité des modules logiciels.

### Ségrégation des interfaces (Interface segregation principle)

_Préférer plusieurs interfaces spécifiques pour chaque client plutôt qu'une seule interface générale_.

L'ISP stipule que "_les clients ne devraient pas être forcés de dépendre des interfaces qu'ils n'utilisent pas_". En
termes simples, cela signifie que les grandes interfaces monolithiques doivent être évitées en faveur de plus petites,
plus spécifiques qui sont plus facilement gérables et utilisables par les classes.

Pour donner un exemple, supposons que vous ayez une interface `Imprimante` avec les méthodes `imprimer`, `scanner`
et `faxer`. C'est bien pour une imprimante multifonction qui peut faire tout cela, mais qu'en est-il d'une imprimante de
base qui ne peut qu'imprimer ? Selon l'ISP, il serait préférable d'avoir des interfaces séparées pour chaque
fonctionnalité, de sorte que l'imprimante de base n'ait pas besoin de dépendre (ou d'implémenter de manière
artificielle) des méthodes `scanner` et `faxer` qu'elle ne peut pas utiliser.

L'avantage de l'ISP est qu'il réduit le couplage entre les composants et améliore leur modularité, facilitant ainsi la
maintenance, la réutilisation et l'évolution du code.

### Inversion des dépendances (Dependency inversion principle)

_Il faut dépendre des abstractions, pas des implémentations_

Le DIP stipule que :

1. Les modules de haut niveau ne doivent pas dépendre des modules de bas niveau. Les deux doivent dépendre des
   abstractions.

2. Les abstractions ne doivent pas dépendre des détails. Les détails doivent dépendre des abstractions.

Par "module de haut niveau", on entend une classe (ou un ensemble de classes) qui est à un niveau d'abstraction élevé,
c'est-à-dire plus orientée vers les objectifs métier. Et par "module de bas niveau", on entend une classe (ou un
ensemble de classes) qui est à un niveau d'abstraction bas, c'est-à-dire plus orientée vers les détails techniques ou
l'infrastructure.

En d'autres termes, plutôt que de laisser les classes de haut niveau (plus proches des opérations métier) dépendre
directement des classes de bas niveau (plus proches des opérations techniques), les deux devraient dépendre d'interfaces
abstraites. Ainsi, si les détails de la mise en œuvre d'une classe de bas niveau doivent changer, cela n'a aucun impact
sur les classes de haut niveau.

L'avantage de ce principe est qu'il contribue à définir un système fortement cohérent mais faiblement couplé, ce qui
rend le code plus flexible, plus facile à tester, à maintenir et à faire évoluer.

## Autres Principes

### DRY / WET

#### DRY (Don't Repeat Yourself)

#### Opposé de DRY: WET (Write Everything Twice)

[https://en.wikipedia.org/wiki/Don%27t_repeat_yourself](https://en.wikipedia.org/wiki/Don%27t_repeat_yourself)

[https://fr.wikipedia.org/wiki/Ne_vous_répétez_pas](https://fr.wikipedia.org/wiki/Ne_vous_répétez_pas)

**DRY** signifie **Don't Repeat Yourself** (_Ne vous répétez pas_ en français). C'est un principe de développement
logiciel qui vise à réduire la répétition de code. L'idée est que chaque morceau de logique doit avoir un emplacement
unique et définitif dans le système. Si vous découvrez que vous écrivez le même code à plusieurs reprises, vous devriez
chercher un moyen de le centraliser et de le réutiliser, plutôt que de le dupliquer. Le respect de ce principe rend le
code plus lisible, plus efficace et plus facile à maintenir.

À l'opposé, **WET** signifie **Write Everything Twice** (_Écrire tout deux fois_ en français) ou **We Enjoy Typing** (
_Nous aimons taper_ en français). C'est souvent utilisé de manière humoristique pour décrire du code qui viole le
principe DRY, c'est-à-dire du code qui a beaucoup de répétitions inutiles.

Il est important de noter que le principe DRY n'encourage pas à éviter toute duplication à tout prix. Parfois, essayer
d'éliminer toute duplication peut conduire à une conception trop complexe et difficile à comprendre. Il s'agit plutôt
d'éviter la duplication de la logique du système. Une duplication apparemment similaire peut être acceptable si les
motivations et les usages derrière elles sont différents.

### KISS

[https://en.wikipedia.org/wiki/KISS_principle](https://en.wikipedia.org/wiki/KISS_principle)

[https://fr.wikipedia.org/wiki/Principe_KISS](https://fr.wikipedia.org/wiki/Principe_KISS)

#### Keep it simple, stupid

En développement logiciel, **KISS** est un acronyme pour **Keep It Simple, Stupid** (_Garde ça simple, idiot_ en
français). Ce principe de conception encourage la simplicité dans la conception et l'écriture du code.

L'idée est d'éviter la complexité inutile. Par complexité inutile, on entend généralement des solutions _sur-conçues_
(_over-engineered_, ou trop élaborées), c'est-à-dire qui utilisent des conceptions plus complexes qu'il n'est réellement
nécessaire pour résoudre le problème à portée de main. Une solution plus complexe peut être plus difficile à comprendre,
à tester et à maintenir, et est également plus susceptible d'introduire des bugs.

Dans la pratique, suivre le principe KISS pourrait signifier de privilégier une conception plus simple même si elle est
un peu moins élégante, choisir une solution brute, mais efficace plutôt qu'une solution sophistiquée, mais délicate, ou
préférer des structures de code faciles à comprendre et à parcourir à des structures de code plus "intelligentes" mais
potentiellement déroutantes.

Il est important de noter que KISS ne signifie pas nécessairement choisir la solution la plus simple à court terme, mais
plutôt la solution qui reste simple sur toute la durée de vie du code, y compris sa maintenance et son évolution
futures.

### Loi de Demeter (LoD)

#### Principe de connaissance minimale

[https://en.wikipedia.org/wiki/Law_of_Demeter](https://en.wikipedia.org/wiki/Law_of_Demeter)

[https://fr.wikipedia.org/wiki/Loi_de_Déméter](https://fr.wikipedia.org/wiki/Loi_de_Déméter)

La Loi de Demeter est un principe de conception en programmation orientée objet qui encourage à réduire les dépendances
entre les objets. Aussi connu sous le nom de principe de _moindre connaissance_, il stipule qu'un objet ne devrait pas
connaître les détails internes des autres objets.

Formellement, la Loi de Demeter stipule que la méthode `M` d'un objet `O` ne devrait invoquer que les méthodes des
objets suivants :

- `O` lui-même
- un objet passé en paramètre à `M`
- un objet créé par `M`
- un objet composant de `O`

En d'autres termes, si vous avez un objet `A` qui contient un objet `B`, qui à son tour contient un objet `C`, la Loi de
Demeter suggère qu'`A` ne devrait pas accéder directement à `C`. Si vous avez une méthode dans `A` qui a besoin
d'interagir avec `C`, vous devriez avoir une méthode dans `B` qui sert d'intermédiaire.

L'idée derrière la loi est de minimiser le couplage entre les objets, en évitant qu'un objet ne connaisse trop les
détails internes des autres objets. Cela rend le système dans son ensemble plus modulaire et robuste, car les objets
peuvent être modifiés sans affecter grandement les autres objets.

Il est important de noter que la Loi de Demeter est un principe directeur plutôt qu'un ensemble de règles strictes à
suivre. Il y aura des situations où il est approprié de rompre cette loi dans l'intérêt d'autres aspects de la
conception.

### Tell Don't ask

[https://martinfowler.com/bliki/TellDontAsk.html](https://martinfowler.com/bliki/TellDontAsk.html)

_**Tell-Don't-Ask** is a principle that helps people remember that object-orientation is about bundling data with the
functions that operate on that data. It reminds us that rather than asking an object for data and acting on that data,
we should instead tell an object what to do._

_**Tell-Don't-Ask** est un principe qui aide les gens à se rappeler que la programmation orientée objet consiste à
regrouper des données avec les fonctions qui opèrent sur ces données. Il nous rappelle qu'au lieu de demander à un objet
des données et d'agir sur ces données, nous devrions plutôt dire à un objet ce qu'il doit faire._

Le principe "**Tell, Don't Ask**" (Dis-le, ne le demande pas) est un principe de conception en programmation orientée
objet qui encourage à dire à un objet ce qu'il doit faire, plutôt que de demander à l'objet ses données et de manipuler
ces dernières.

Essentiellement, cela signifie que vous devriez essayer d'éviter de demander à un objet son état, de prendre cet état et
de faire quelque chose avec lui. À la place, l'objet devrait être responsable de faire quelque chose avec son propre
état.

Voici un exemple pour illustrer ce principe :

Considérons deux classes, `Car` et `Driver`. Une approche qui **ne** suit **pas** le principe "Tell, Don't Ask" pourrait
ressembler à ceci :

```java
public class Driver {
    public void drive() {
        Car car = new Car();
        if (car.getFuel() > 0) {
            car.moveForward();
        }
    }
}
```

Le problème ici est que la classe `Driver` doit demander à la voiture combien de carburant elle a, puis décider quoi
faire en fonction de cette information.

Une approche qui suit le principe "Tell, Don't Ask" pourrait ressembler à ceci :

```java
public class Driver {
    public void drive() {
        Car car = new Car();
        car.moveForward();
    }
}

public class Car {
    public void moveForward() {
        if (this.fuel > 0) {
            // code pour avancer
        }
    }
}
```

L'avantage de cette approche est qu'elle décentralise la logique et la responsabilité, rendant le code plus modulaire et
facile à maintenir et à comprendre.

### Orthogonalité

Le principe d'orthogonalité est un concept de conception logicielle qui stipule que les composants d'un système sont
orthogonaux s'ils peuvent être modifiés indépendamment les uns des autres. Autrement dit, changer quelque chose dans une
partie du système n'affecte pas d'autres parties du système.

L'idée vient de l'orthogonalité en mathématiques, où deux vecteurs sont orthogonaux s'ils sont perpendiculaires l'un à
l'autre, signifiant qu'ils n'ont pas d'impact l'un sur l'autre.

Quand ce principe est appliqué à la conception logicielle, il a pour but de minimiser les dépendances entre les
différents modules ou composants. Les avantages de ce principe sont :

- **Isolation des erreurs** : une erreur dans un composant ne se propage pas aux autres.
- **Facilité de compréhension** : chaque composant peut être compris indépendamment des autres.
- **Facilité de modification** : une modification d'un composant n'affecte pas les autres, rendant le développement et
  la maintenance du système plus faciles.

Par exemple, si vous développez une application avec une interface utilisateur, une base de données, et une logique
métier, ces trois éléments devraient être conçus de manière à ce qu'ils puissent être développés et modifiés
indépendamment les uns des autres. Ils communiqueraient par le biais d'interfaces clairement définies, sans avoir besoin
de connaître les détails de mise en œuvre des autres.

### Éviter l'optimisation prématurée

L'optimisation prématurée est la pratique de l'optimisation micro performante d'un code avant de comprendre clairement
quels sont les véritables goulets d'étranglement de performance. _"Éviter l'optimisation prématurée"_ est un principe
communément cité en programmation, attribué à Donald Knuth, un éminent informaticien. La citation complète de Knuth
est :

_"Nous devrions oublier les petites économies, disons environ 97% du temps : l'optimisation prématurée est la racine de
tous les maux. Pourtant, nous ne devrions pas manquer nos chances dans ce 3% critique."_

Ce principe suggère que la majorité de l'effort en optimisation devrait être consacrée aux zones d'un programme où les
gains de performance auront un impact significatif. Ces zones ne peuvent être efficacement identifiées qu'après que les
problématiques de performances ont été clairement définies, souvent via le _monitoring_ ou le _profilage_ du code en
question.

Cela aide à éviter de dépenser du temps sur des optimisations minuscules qui n'affectent que très peu les performances
globales, tout en rendant potentiellement le code plus complexe et difficile à maintenir. Cela ne signifie pas que les
performances ne sont pas importantes, mais qu'elles doivent être abordées de manière systématique et informée.

### Règle des 5 lignes

La "règle des 5 lignes" en développement logiciel est une directive heuristique suggérant que les fonctions ou méthodes
doivent idéalement être courtes, généralement dans les cinq lignes de code. L'idée derrière cette règle est de
promouvoir la lisibilité, la maintenabilité et la simplicité du code.

La logique derrière la règle des 5 lignes inclut :

1. **Lisibilité** : Des fonctions plus courtes sont plus faciles à comprendre d'un coup d'œil, ce qui rend plus simple
   pour les développeurs de comprendre ce que fait la fonction et comment elle atteint son but.

2. **Maintenabilité** : Les petites fonctions sont généralement plus faciles à maintenir et à modifier. Lorsque les
   fonctions sont concises, il est plus facile d'isoler et de corriger les bugs, d'ajouter de nouvelles fonctionnalités
   ou de refactoriser le code sans affecter involontairement d'autres parties du système.

3. **Testabilité** : Les fonctions courtes sont souvent plus faciles à tester, car elles ont tendance à avoir moins de
   chemins d'exécution et de dépendances. Cela rend plus simple d'écrire des tests unitaires qui couvrent tous les
   scénarios possibles.

4. **Réduction de la complexité** : Garder les fonctions courtes peut aider à réduire la complexité globale de la base
   de code. Les fonctions complexes comportant de nombreuses lignes de code sont plus difficiles à comprendre et sont
   souvent le signe que la fonction fait trop de choses et devrait être décomposée en pièces plus petites et plus
   gérables.

5. **Amélioration de la réutilisabilité** : Les fonctions courtes sont plus susceptibles d'être réutilisées dans
   différentes parties de la base de code car elles ont tendance à être plus ciblées et ont une seule responsabilité.
   Cela peut conduire à un code plus modulaire et plus facile à maintenir en général.

Il est important de noter que la règle des 5 lignes est une directive plutôt qu'une règle stricte. Bien que viser des
fonctions courtes soit généralement bénéfique, il peut y avoir des cas où des fonctions plus longues sont nécessaires ou
appropriées. La clé est de prioriser la lisibilité, la maintenabilité et la simplicité dans la conception du code et
d'utiliser son discernement lors de la détermination de la longueur appropriée pour une fonction en fonction du contexte
spécifique et des exigences du projet logiciel.

### Les commentaires de code doivent expliquer pourquoi, pas quoi

Cette règle suggère que les commentaires dans le code devraient **se concentrer sur l'explication du but, de
l'intention, ou de la justification derrière le code** plutôt que de décrire ce que fait le code.

Un code bien écrit devrait être auto-explicatif, et les commentaires devraient fournir un contexte ou un éclairage
supplémentaire.

### Refactorisation de code

La **refactorisation** (_refactoring_) de code est le processus de restructuration du code existant sans en changer le
comportement externe afin d'améliorer sa lisibilité, sa maintenabilité et/ou ses performances. Voici quelques règles et
directives communes pour la refactorisation de code :

1. **Règle de trois** : cette règle suggère que si vous vous trouvez en train d'écrire un code similaire pour la
   troisième fois, il est temps de le refactoriser en une fonction, une méthode ou une classe réutilisable. Elle aide à
   prévenir la duplication de code et favorise la réutilisabilité.

2. **Refactoriser tôt, refactoriser souvent** : ce principe préconise de traiter les "odeurs de code" et d'améliorer la
   qualité du code en continu tout au long du processus de développement, plutôt que de laisser la dette technique
   s'accumuler. Refactoriser régulièrement de petits morceaux de code peut aider à garder la base de code propre et
   maintenable.

3. **Extraire jusqu'à épuisement** : lors de la refactorisation, cette règle conseille aux développeurs de continuer à
   extraire de plus petites fonctions ou méthodes à partir de plus grandes jusqu'à ce qu'elles ne puissent plus
   raisonnablement être décomposées davantage. Elle favorise la création de petites unités de code ciblées et
   réutilisables.

4. **Principes SOLID** : ces principes (Single Responsibility, Open/Closed, Liskov Substitution, Interface Segregation
   et Dependency Inversion) fournissent des directives pour écrire un code orienté objet propre, maintenable et
   extensible. Le respect de ces principes nécessite souvent de refactoriser le code existant pour s'y conformer.

5. **Refactoriser agressivement après avoir ajouté des fonctionnalités** : chaque fois qu'une nouvelle fonctionnalité
   est ajoutée à la base de code, il est recommandé de passer en revue le code existant et de le refactoriser si
   nécessaire pour maintenir la qualité et la cohérence du code. Cela aide à prévenir l'accumulation de la dette
   technique et à s'assurer que la base de code reste propre et maintenable.

6. **Utiliser des outils de refactorisation automatisés** : l'utilisation d'outils de refactorisation automatisés
   fournis par des environnements de développement intégrés (IDE) ou des plugins tiers peut rendre le processus de
   refactorisation plus efficace et moins sujet aux erreurs. Ces outils peuvent aider à renommer les variables, à
   extraire des méthodes et à effectuer d'autres tâches de refactorisation courantes avec un minimum d'effort manuel.

7. **Préserver le comportement avec les tests** : lors de la refactorisation du code, il est crucial de s'assurer que le
   comportement du code reste inchangé. L'écriture et la maintenance de tests unitaires exhaustifs peuvent aider à
   valider que le code refactorisé se comporte comme prévu et à détecter d'éventuels effets secondaires involontaires.

### Code smells

En développement logiciel, les **"odeurs de code"** désignent certains modèles ou caractéristiques du code qui peuvent
signaler des problèmes plus profonds ou des zones potentiellement améliorables. Ce ne sont pas des bugs en soi, mais
plutôt des indicateurs de problèmes de conception ou de violations des bonnes pratiques de codage. Les odeurs de code
peuvent rendre le code plus difficile à comprendre, à maintenir et à étendre. Identifier et traiter les odeurs de code
par la refactorisation peut aider à améliorer la qualité et la maintenabilité du code. Certaines odeurs de code
courantes incluent :

1. **Longue Méthode** : Les méthodes ou fonctions qui sont excessivement longues et accomplissent plusieurs tâches. Les
   longues méthodes sont plus difficiles à comprendre, à tester, et à maintenir.

2. **Grande Classe** : Les classes qui sont trop complexes, avec trop d'attributs et de méthodes. Les grandes classes
   violent le principe de la responsabilité unique et peuvent être difficiles à gérer.

3. **Code Dupliqué** : Des fragments de code identiques ou très similaires apparaissant à plusieurs endroits. Le code
   dupliqué viole le principe Ne vous répétez pas (DRY) et rend la maintenance plus difficile.

4. **Envie de fonctionnalité** : Lorsqu'une méthode dans une classe accède aux données ou au comportement d'une autre
   classe plus qu'à sa propre donnée ou son comportement. Cela suggère que la méthode pourrait appartenir à l'autre
   classe et indique un éventuel problème de conception.

5. **Obsession Primitive** : Utilisation excessive de types de données primitifs au lieu de créer des classes ou des
   énumérations personnalisées. L'obsession primitive peut conduire à la duplication de code, à une lisibilité réduite,
   et à une maintenabilité diminuée.

6. **Objet Dieu** : Une classe qui sait ou fait trop de choses, devenant souvent un point central de dépendances dans la
   base de code. Les objets dieux sont difficiles à comprendre, à tester, et à maintenir et peuvent conduire à un code
   étroitement couplé.

7. **Commentaires** : Des commentaires excessifs ou trompeurs dans le code, qui peuvent indiquer que le code n'est pas
   auto-explicatif. Bien que les commentaires puissent être utiles, ils ne doivent pas être utilisés comme substitut à
   l'écriture de code propre et expressif.

8. **Regroupements de données** : Lorsque des groupes de champs de données apparaissent ensemble à plusieurs endroits
   dans la base de code, suggérant qu'ils pourraient être encapsulés dans une classe séparée.

9. **Déclarations Switch** : Utilisation excessive de déclarations `switch` ou `case`, surtout lorsqu'elles apparaissent
   à plusieurs endroits dans la base de code. Les déclarations `switch` peuvent rendre le code plus difficile à étendre
   et à maintenir, violant ainsi le principe ouvert/fermé.

10. **Intimité Inappropriée** : Classes qui dépendent excessivement les unes des autres en détails internes ou qui ont
    trop de dépendances. L'intimité inappropriée peut conduire à un code étroitement couplé qui est difficile à
    refactoriser ou à étendre.

L'identification et le traitement des odeurs de code est une partie essentielle du processus de refactorisation, aidant
à améliorer la qualité globale, la lisibilité, et la maintenabilité de la base de code.
