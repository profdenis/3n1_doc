# Héritage multiple

L'héritage multiple en Python est une fonctionnalité puissante qui permet à une classe d'hériter des attributs et
méthodes de plus d'une classe parente. Cela représente une différence significative avec Java, qui ne supporte que
l'héritage simple pour les classes (bien que Java permette d'implémenter plusieurs interfaces).

## Comment fonctionne l'héritage multiple en Python

En Python, l'héritage multiple est implémenté en listant toutes les classes parentes dans la définition de classe,
séparées par des virgules :

```python
class Parent1:
    def method1(self):
        print("Méthode de Parent1")


class Parent2:
    def method2(self):
        print("Méthode de Parent2")


class Enfant(Parent1, Parent2):
    pass


# Création d'une instance
enfant = Enfant()
enfant.method1()  # Sortie: Méthode de Parent1
enfant.method2()  # Sortie: Méthode de Parent2
```

Dans cet exemple, la classe `Enfant` hérite des méthodes de `Parent1` et `Parent2`, lui permettant d'utiliser à la fois
`method1()` et `method2()`.

## Exemple pratique : Le licorne mythique

Considérons un exemple plus concret utilisant une créature mythique :

```python
class Cheval:
    def __init__(self, nom):
        self.nom = nom

    def courir(self):
        return f"{self.nom} court."

    def manger_du_foin(self):
        return f"{self.nom} mange du foin."


class Narval:
    def nager(self):
        return f"{self.nom} nage."

    def a_un_corneau(self):
        return True


class Licorne(Cheval, Narval):
    def pouvoirs_magiques(self):
        return f"{self.nom} utilise des pouvoirs magiques!"
```

Ici, `Licorne` hérite des caractéristiques de `Cheval` (courir, manger du foin) et de `Narval` (nager, avoir un
corneau), tout en ajoutant sa propre capacité unique.

## Ordre de résolution des méthodes (MRO)

Lorsque qu'une méthode est appelée sur une instance, Python doit déterminer quelle implémentation utiliser, surtout si
plusieurs classes parentes définissent la même méthode. Python utilise l'algorithme C3 pour établir un ordre de
résolution des méthodes (MRO) :

```python
class A:
    def saluer(self):
        return "Bonjour depuis A"


class B:
    def saluer(self):
        return "Bonjour depuis B"


class C(A, B):
    pass


c = C()
print(c.saluer())  # Sortie: Bonjour depuis A
print(C.__mro__)  # Montre l'ordre de résolution des méthodes
```

La méthode de la première classe parente dans la liste d'héritage (`A` dans ce cas) est utilisée.

## Avantages de l'héritage multiple

1. **Réutilisabilité du code** : Permet de combiner des fonctionnalités provenant de différentes classes, réduisant
   ainsi la duplication de code.
2. **Flexibilité dans la conception des classes** : Permet de créer des structures de classes complexes en héritant de
   plusieurs classes de base.
3. **Modularité** : Supporte la création de mixins (classes spécialisées fournissant une fonctionnalité spécifique) qui
   peuvent être combinés avec diverses classes.

## Inconvénients de l'héritage multiple

1. **Ambiguïté et conflits de noms** : Lorsque plusieurs classes parentes définissent des méthodes avec le même nom,
   cela peut entraîner de la confusion.
2. **Complexité et maintenance** : À mesure que l'arborescence d'héritage grandit, comprendre et maintenir les relations
   entre les classes devient plus difficile.
3. **Problème du diamant** : Lorsqu'une classe hérite de deux classes qui ont un ancêtre commun, une ambiguïté peut
   survenir quant à savoir quelle implémentation utiliser.
4. **Couplage serré** : Les modifications apportées à une classe de base peuvent avoir des effets inattendus sur les
   classes dérivées.

## Le problème du diamant

Le problème du diamant est un défi spécifique dans l'héritage multiple :

```python
class A:
    def methode(self):
        print("Méthode depuis A")


class B(A):
    def methode(self):
        print("Méthode depuis B")


class C(A):
    def methode(self):
        print("Méthode depuis C")


class D(B, C):
    pass


d = D()
d.methode()  # Quelle méthode est appelée ?
```

Le MRO de Python résout ce problème en suivant un ordre spécifique, mais il s'agit toujours d'une complexité à laquelle
il faut être attentif.

L'héritage multiple est un outil puissant en Python, mais il doit être utilisé avec discernement. Lorsqu'il est utilisé
de manière appropriée, il peut conduire à un code élégant et modulaire. Lorsqu'il est trop utilisé, il peut créer des
défis de maintenance.

## Comment fonctionne `super()` avec l'héritage multiple en Python

Lorsque qu'une classe Python hérite de deux ou plusieurs classes, le comportement de `super()` est déterminé par l'
**ordre de résolution des méthodes (MRO)**, comme discuté ci-dessus.

### À quelle classe fait référence `super()` ?

Dans une classe qui hérite de plusieurs classes parentes, `super()` fait référence à la **prochaine classe dans le
MRO**, et non nécessairement à la première parente listée dans la définition de la classe. Par exemple :

```python
class A:
    def __init__(self):
        print("A initialisé")


class B:
    def __init__(self):
        print("B initialisé")


class C(A, B):
    def __init__(self):
        super().__init__()
        print("Enfant initialisé")


enfant = C()
```

**Sortie :**

```
A initialisé
Enfant initialisé
```

Ici, `super().__init__()` dans `Enfant` appelle `A.__init__()` parce que `A` est la prochaine classe dans le MRO après
`C`. Le MRO pour `C` est `[C, A, B, object]`.

### Comment faire référence à l'autre classe parente ?

Si vous souhaitez appeler explicitement une méthode d'une classe parente spécifique (et non seulement celle qui suit
dans le MRO), vous pouvez le faire en référençant directement la classe :

```python
class C(A, B):
    def __init__(self):
        super().__init__()  # Appelle A.__init__()
        B.__init__(self)  # Appelle explicitement B.__init__()
        print("C initialisé")
```

De cette manière, les deux initialiseurs des classes parentes sont appelés, mais soyez prudent - si les deux classes
parentes appellent `super()`, vous pourriez finir par appeler la même méthode plusieurs fois, en fonction du MRO et de
la conception de la classe.

### Utilisation avancée : Personnalisation de `super()`

Vous pouvez également personnaliser à partir de quelle classe `super()` commence sa recherche en passant des arguments :

```python
super(B, self).__init__()
```

Cela indique à Python de commencer à chercher la méthode après `Parent2` dans le MRO de `self`. Cela est rarement
nécessaire dans les conceptions de classes typiques, mais cela peut être utile dans les scénarios d'héritage multiple
avancés.

### Tableau récapitulatif

| Scénario                      | Ce que `super()` appelle                       | Comment appeler l'autre parent         |
|-------------------------------|------------------------------------------------|----------------------------------------|
| Héritage multiple `C(A, B)`   | Prochaine classe dans le MRO après la courante | Explicitement : `B.methode(self, ...)` |
| Personnalisation de `super()` | Après la classe spécifiée dans le MRO          | Utiliser `super(C, self).methode()`    |

### Points clés

- `super()` fait toujours référence à la prochaine classe dans le MRO, et non nécessairement à la première parente dans
  la définition de la classe.
- Pour appeler une méthode spécifique d'une classe parente, utilisez directement le nom de la classe parente.
- Soyez prudent avec l'héritage multiple et `super()` pour éviter les appels en double ou les initialisations
  manquantes.

Dans la plupart des cas, restez cohérent dans l'utilisation de `super()` et concevez vos classes pour qu'elles coopèrent
avec lui, surtout lorsque vous construisez des frameworks ou des mixins.

## Exemple avec le problème du diamant

```python
class Alpha:
    def __init__(self):
        print("Alpha initialisé")


class A(Alpha):
    def __init__(self):
        super().__init__()
        print("A initialisé")


class B(Alpha):
    def __init__(self):
        super().__init__()
        print("B initialisé")


class C(A, B):
    def __init__(self):
        super().__init__()  # Appelle A.__init__()
        B.__init__(self)  # Appelle explicitement B.__init__()
        print("C initialisé")


enfant = C()
print(C.__mro__)
```

### Sortie

```text
Alpha initialisé
B initialisé
A initialisé
Alpha initialisé
B initialisé
C initialisé
(<class '__main__.C'>, <class '__main__.A'>, <class '__main__.B'>, <class '__main__.Alpha'>, <class 'object'>)
```

**Pourquoi obtenons-nous plusieurs appels aux mêmes méthodes `__init__` ?**

Analysons étape par étape pourquoi cela se produit :

### Explication clé

La sortie se produit en raison de deux facteurs :

1. **Ordre de résolution des méthodes (MRO)** dans l'héritage multiple
2. **Appel explicite à `B.__init__`** dans la classe `C`

Voici comment le code s'exécute :

---

### Flux d'exécution

1. **`C()` est créé** → Appelle `C.__init__`
2. **`super().__init__()` dans `C`** → Suit le MRO pour appeler `A.__init__`
3. **`A.__init__` s'exécute** :
    - `super().__init__()` → La prochaine dans le MRO est `B`, donc `B.__init__` s'exécute
    - `B.__init__` → `super().__init__()` appelle `Alpha.__init__` (imprime "Alpha initialisé")
    - `B.__init__` se termine (imprime "B initialisé")
    - Retour à `A.__init__` (imprime "A initialisé")
4. **Appel explicite `B.__init__(self)` dans `C`** → Appelle directement `B.__init__` à nouveau :
    - `super().__init__()` → Appelle `Alpha.__init__` à nouveau (imprime "Alpha initialisé")
    - `B.__init__` se termine à nouveau (imprime "B initialisé")
5. **`C.__init__` se termine** (imprime "C initialisé")

---

### Pourquoi le MRO est important

Le MRO pour `C` est **`C → A → B → Alpha → object`** (visible dans la sortie). Cela signifie :

- Lorsque `super()` est appelé dans `A`, il cherche la prochaine classe dans la chaîne du MRO (`B`), et non le parent
  direct de `A` (`Alpha`).

---

### Pourquoi "Alpha" apparaît-il deux fois ?

1. Le premier "Alpha" provient de la chaîne `A → B → Alpha` via `super()` dans `C`
2. Le deuxième "Alpha" provient de l'appel explicite à `B.__init__` dans `C`, qui déclenche `B → Alpha` à nouveau

---

### Comment corriger cela (si nécessaire)

Si vous souhaitez éviter les initialisations en double :

```python
class C(A, B):
    def __init__(self):
        # Laissez le MRO gérer toutes les initialisations des parents
        super().__init__()  # Suit la chaîne C→A→B→Alpha
        print("C initialisé")
```

**Sortie avec cette correction :**

```
Alpha initialisé
B initialisé
A initialisé
C initialisé
(<class '__main__.C'>, <class '__main__.A'>, <class '__main__.B'>, <class '__main__.Alpha'>, <class 'object'>)
```

---

### Points clés à retenir

1. **Le MRO détermine le comportement de `super()`**, et non seulement les classes parentes
2. **Les appels explicites aux parents** (`B.__init__`) contournent le MRO et peuvent causer des doublons
3. **L'utilisation cohérente de `super()` est plus sûre dans les héritages complexes**

N'oubliez pas d'exécuter `print(C.__mro__)` pour voir l'ordre exact de résolution des méthodes.