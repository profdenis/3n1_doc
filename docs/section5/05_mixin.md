# Les *mixins*

## 1. Introduction : qu'est-ce qu'un mixin?

Un mixin est une petite classe qui ajoute un comportement précis à d'autres classes par héritage, sans jamais servir de
classe de base « principale ». C'est la façon légitime et pratique d'utiliser l'héritage multiple.

### Pourquoi l'héritage multiple est déconseillé

En général, on évite l'héritage multiple : il rend le code plus complexe et plus difficile à raisonner. Le cas classique
est le **problème du losange** (diamant) : une classe `D` hérite de `B` et de `C`, qui héritent toutes deux de `A`. Si
`B` et `C` redéfinissent chacune une méthode de `A`, laquelle `D` doit-elle utiliser? Chaque langage répond à sa manière
(héritage virtuel en C++, ordre de résolution C3 en Python, interdiction pure et simple pour les classes en Java), mais
dans tous les cas le comportement devient difficile à prévoir pour quiconque lit le code.

### L'idée du mixin

Un mixin évite ces difficultés en respectant une discipline stricte. Il se distingue d'une classe de base ordinaire par
les caractéristiques suivantes :

- **Il exprime « peut faire », pas « est un ».** Une classe `Livre` n' *est pas* un `Serialisable`; elle *sait* se
  sérialiser.
- **Il a une seule responsabilité**, petite et bien délimitée (journaliser, comparer, convertir en JSON, etc.).
- **Il n'est jamais instancié seul.** Il n'a de sens que mélangé à une autre classe.
- **Il a peu ou pas d'état propre.** Il s'appuie sur ce que la classe hôte fournit (attributs ou méthodes).
- **Il ne crée pas de hiérarchie parallèle.** Comme les mixins n'héritent pas d'une base commune et ne redéfinissent pas
  les mêmes méthodes, le losange problématique ne se présente pratiquement jamais.

Autrement dit, on garde l'avantage de l'héritage multiple (réutiliser du code dans plusieurs classes non reliées) en
retirant son principal danger (des parents qui se marchent sur les pieds).

### Les mixins selon les langages

Les langages n'offrent pas tous le même soutien aux mixins. On distingue trois situations :

| Langage | Mécanisme                               | Soutien aux mixins                                                                                    |
|---------|-----------------------------------------|-------------------------------------------------------------------------------------------------------|
| Rust    | Traits avec méthodes par défaut         | Direct : pas d'héritage de classes, on « ajoute » des comportements par les traits                    |
| Java    | Interfaces avec méthodes `default`      | Partiel : une interface fournit une implémentation par défaut, mais sans état                         |
| Python  | Héritage multiple de classes ordinaires | Aucun soutien spécifique : un mixin est simplement une classe écrite et utilisée selon une convention |

En Python, il n'existe donc ni mot-clé `mixin` ni vérification par le langage. Tout repose sur l'héritage multiple, sur
l'ordre de résolution des méthodes (MRO) et sur la discipline du programmeur. C'est pourquoi il est essentiel de bien
comprendre l'héritage multiple, vu à la section précédente, avant d'écrire ses propres mixins.

### Mixins et protocoles : à ne pas confondre

La section sur les protocoles vous a montré comment *décrire* ce qu'un objet sait faire (sa forme), sans fournir de
code. Un mixin fait l'inverse : il *fournit* le code qui permet de le faire. Les deux se complètent bien : un protocole
peut décrire ce qu'un mixin exige de sa classe hôte (voir la section 4).

## 2. Les mixins en Python : principes

En Python, un mixin est une classe ordinaire, qu'on ajoute à la liste des parents d'une autre classe. La recette tient
en quelques règles.

### La recette de base

```python
class MonMixin:
    """Ajoute un comportement. Ne s'utilise jamais seul."""

    def ma_methode(self):
        ...


class MaClasse(MonMixin, ClasseDeBase):
    ...
```

Le mixin se place **avant** la classe de base dans la liste des parents. La raison tient à l'ordre de résolution des
méthodes (MRO) : Python cherche une méthode dans la classe elle-même, puis chez ses parents de gauche à droite. Placé en
premier, le mixin peut donc compléter ou remplacer ce que fournit la classe de base.

### Voir le MRO

Le MRO est consultable à tout moment avec l'attribut `__mro__` :

```python
class Base:
    def saluer(self):
        return "Bonjour"


class PolitesseMixin:
    def saluer(self):
        return super().saluer() + ", cher client"


class Employe(PolitesseMixin, Base):
    pass


print(Employe().saluer())  # Bonjour, cher client
print(Employe.__mro__)
# (Employe, PolitesseMixin, Base, object)
```

Dans `PolitesseMixin.saluer`, l'appel `super()` ne désigne pas forcément la classe de base du mixin (ici, `object`) : il
désigne **la classe suivante dans le MRO de l'objet réel**, soit `Base`. C'est ce qu'on appelle l'héritage coopératif,
et c'est ce qui rend les mixins composables.

### Les conventions à respecter

Python ne vérifie rien : ces conventions sont ce qui sépare un mixin bien conçu d'un héritage multiple confus.

- **Nommer la classe avec le suffixe `Mixin`** (`JsonMixin`, `LoggableMixin`), pour que l'intention soit claire à la
  lecture.
- **Une seule responsabilité** par mixin.
- **Ne pas l'instancier.** Au besoin, documentez-le dans la docstring.
- **Éviter l'état propre.** Un mixin sans `__init__` est le plus simple. S'il en faut un, il accepte `*args, **kwargs`
  et appelle `super().__init__(*args, **kwargs)`.
- **Utiliser `super()`** plutôt qu'un appel direct à une classe nommée, pour que les mixins s'enchaînent correctement.
- **Documenter ce que le mixin attend de la classe hôte** (attributs ou méthodes requis), puisque rien ne l'impose
  automatiquement.
- **Placer les mixins à gauche** de la classe de base dans la liste des parents.

### Quand utiliser un mixin

Un mixin est un bon choix quand un même comportement doit s'ajouter à plusieurs classes qui n'ont pas de lien
hiérarchique (un livre, un client et une facture qui doivent tous pouvoir s'exporter en JSON, par exemple). Si le
comportement ne concerne qu'une seule classe, ou si les classes partagent déjà une base naturelle, une méthode ordinaire
ou l'héritage simple suffit.

## 3. Exemples simples

Voici trois mixins courts, chacun avec une seule responsabilité, puis leur combinaison dans une même classe.

### Exemple 1 : convertir en JSON

```python
import json


class JsonMixin:
    """Ajoute to_json(). Exige que les attributs de l'objet soient sérialisables."""

    def to_json(self):
        return json.dumps(vars(self), ensure_ascii=False)


class Livre(JsonMixin):
    def __init__(self, titre, auteur):
        self.titre = titre
        self.auteur = auteur


print(Livre("Dune", "Frank Herbert").to_json())
# {"titre": "Dune", "auteur": "Frank Herbert"}
```

`Livre` n'a rien à savoir de JSON : le comportement vient entièrement du mixin. N'importe quelle autre classe (`Client`,
`Facture`) peut l'obtenir en ajoutant `JsonMixin` à ses parents.

### Exemple 2 : un `repr` automatique

```python
class ReprMixin:
    """Fournit un __repr__ lisible à partir des attributs de l'objet."""

    def __repr__(self):
        attributs = ", ".join(f"{nom}={valeur!r}" for nom, valeur in vars(self).items())
        return f"{type(self).__name__}({attributs})"
```

Plus besoin de réécrire `__repr__` dans chaque classe : on la mélange avec ce mixin.

### Exemple 3 : comparer à partir d'une clé

Ce mixin a une **exigence** envers sa classe hôte : elle doit définir une méthode `_cle()`. On le signale clairement, et
on fait échouer l'appel si l'exigence n'est pas respectée.

```python
class ComparableMixin:
    """Fournit <, <=, > et >= à partir d'une méthode _cle() que la classe doit définir."""

    def _cle(self):
        raise NotImplementedError("La classe doit définir _cle()")

    def __lt__(self, autre):
        if not isinstance(autre, ComparableMixin):
            return NotImplemented
        return self._cle() < autre._cle()

    def __le__(self, autre):
        if not isinstance(autre, ComparableMixin):
            return NotImplemented
        return self._cle() <= autre._cle()

    def __gt__(self, autre):
        if not isinstance(autre, ComparableMixin):
            return NotImplemented
        return self._cle() > autre._cle()

    def __ge__(self, autre):
        if not isinstance(autre, ComparableMixin):
            return NotImplemented
        return self._cle() >= autre._cle()
```

### Combiner les trois

La force des mixins apparaît quand on en assemble plusieurs dans la même classe :

```python
class Produit(ReprMixin, JsonMixin, ComparableMixin):
    def __init__(self, nom, prix):
        self.nom = nom
        self.prix = prix

    def _cle(self):  # exigence de ComparableMixin
        return self.prix


clavier = Produit("Clavier", 49.99)
souris = Produit("Souris", 24.50)

print(clavier)  # Produit(nom='Clavier', prix=49.99)
print(souris.to_json())  # {"nom": "Souris", "prix": 24.5}
print(souris < clavier)  # True
print(sorted([clavier, souris]))  # [Produit(nom='Souris', ...), Produit(nom='Clavier', ...)]
print(Produit.__mro__)
# (Produit, ReprMixin, JsonMixin, ComparableMixin, object)
```

Trois comportements indépendants, aucun conflit, et `Produit` ne contient que ce qui lui est propre. Remarquez que les
mixins n'ont aucune méthode en commun : c'est ce qui évite les problèmes liés au losange.

### À retenir

Un bon mixin est court, a un nom clair, ne s'instancie pas et dit explicitement ce qu'il attend de sa classe hôte.

## 4. Exemple plus complexe : un mini-modèle de données

Cet exemple assemble cinq mixins autour d'une classe de base `Entite`. Il illustre ce qui distingue un vrai mixin d'un
simple héritage multiple : des comportements indépendants, qui s'enchaînent grâce à `super()` et qu'on combine à la
carte selon la classe. Le code a été exécuté tel quel.

### Le principe : des « crochets » dans la classe de base

`Entite` définit des méthodes vides (`valider`, `avant_sauvegarde`, `apres_sauvegarde`) qui servent de points
d'accroche. Chaque mixin les complète en appelant `super()` pour passer la main au suivant dans le MRO. La base joue le
rôle de fin de chaîne.

```python
import json
from datetime import datetime
from typing import Protocol


class Entite:
    """Base du modèle : fournit les crochets (hooks) que les mixins étendent."""
    _prochain_id = 1

    def __init__(self, **kwargs):
        super().__init__(**kwargs)  # object.__init__ refuse les arguments en trop
        self.id = Entite._prochain_id
        Entite._prochain_id += 1

    def valider(self):
        """Retourne la liste des erreurs de validation (vide par défaut)."""
        return []

    def avant_sauvegarde(self):
        pass

    def apres_sauvegarde(self):
        pass
```

### Les mixins

Chacun a une seule responsabilité et ne connaît ni les autres mixins ni les classes finales.

```python
class HorodatageMixin:
    """Ajoute les attributs cree_le et modifie_le."""

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.cree_le = datetime.now()
        self.modifie_le = self.cree_le

    def avant_sauvegarde(self):
        super().avant_sauvegarde()
        self.modifie_le = datetime.now()


class ValidationMixin:
    """Refuse la sauvegarde si valider() retourne des erreurs."""

    def avant_sauvegarde(self):
        erreurs = self.valider()
        if erreurs:
            raise ValueError("; ".join(erreurs))
        super().avant_sauvegarde()


class JournalMixin:
    """Écrit une trace après chaque sauvegarde."""

    def apres_sauvegarde(self):
        super().apres_sauvegarde()
        print(f"[journal] {type(self).__name__} #{self.id} sauvegardé")


class SerialisationMixin:
    """Ajoute to_dict() et to_json()."""

    def to_dict(self):
        return {
            cle: valeur.isoformat() if isinstance(valeur, datetime) else valeur
            for cle, valeur in vars(self).items()
        }

    def to_json(self):
        return json.dumps(self.to_dict(), ensure_ascii=False, indent=2)
```

### Un mixin qui exige quelque chose de sa classe hôte

`PersistableMixin` appelle des méthodes qu'il ne définit pas (`avant_sauvegarde`, `to_dict`, l'attribut `id`). On rend
cette exigence explicite avec un **protocole**, celui de la section précédente, utilisé ici comme annotation de `self`.
Rien n'est vérifié à l'exécution, mais un vérificateur de types comme mypy signalera une classe hôte incomplète, et le
lecteur sait exactement ce qui est attendu.

```python
class _Sauvegardable(Protocol):
    """Ce que PersistableMixin exige de sa classe hôte."""
    id: int

    def avant_sauvegarde(self) -> None: ...

    def apres_sauvegarde(self) -> None: ...

    def to_dict(self) -> dict: ...


class PersistableMixin:
    """Ajoute sauvegarder() : un dépôt en mémoire, pour l'exemple."""
    _depot = {}

    def sauvegarder(self: _Sauvegardable):
        self.avant_sauvegarde()
        PersistableMixin._depot[(type(self).__name__, self.id)] = self.to_dict()
        self.apres_sauvegarde()
```

### Assembler les classes finales

On choisit les mixins dont chaque classe a besoin. `Produit` les utilise tous; `Client` n'en veut que trois.

```python
class Produit(ValidationMixin, HorodatageMixin, JournalMixin,
              SerialisationMixin, PersistableMixin, Entite):
    def __init__(self, nom, prix, **kwargs):
        super().__init__(**kwargs)
        self.nom = nom
        self.prix = prix

    def valider(self):
        erreurs = super().valider()
        if not self.nom:
            erreurs.append("le nom est obligatoire")
        if self.prix < 0:
            erreurs.append("le prix doit être positif")
        return erreurs


class Client(JournalMixin, SerialisationMixin, PersistableMixin, Entite):
    def __init__(self, courriel, **kwargs):
        super().__init__(**kwargs)
        self.courriel = courriel
```

### Utilisation et résultat

```python
p = Produit("Clavier", 49.99)
p.sauvegarder()
print(p.to_json())

try:
    Produit("", -5).sauvegarder()
except ValueError as e:
    print("Refusé :", e)

Client("a@exemple.com").sauvegarder()
print([c.__name__ for c in Produit.__mro__])
print([c.__name__ for c in Client.__mro__])
```

Sortie (les dates varient) :

```text
[journal] Produit #1 sauvegardé
{
  "id": 1,
  "cree_le": "2026-10-08T16:37:41.171969",
  "modifie_le": "2026-10-08T16:37:41.172358",
  "nom": "Clavier",
  "prix": 49.99
}
Refusé : le nom est obligatoire; le prix doit être positif
[journal] Client #3 sauvegardé
['Produit', 'ValidationMixin', 'HorodatageMixin', 'JournalMixin', 'SerialisationMixin', 'PersistableMixin', 'Entite', 'object']
['Client', 'JournalMixin', 'SerialisationMixin', 'PersistableMixin', 'Entite', 'object']
```

### Ce qui se passe, étape par étape

1. **Construction.** `Produit(...)` appelle `super().__init__(**kwargs)`. La chaîne traverse `HorodatageMixin` puis
   `Entite`, qui attribue l'`id`. Au retour, chaque niveau ajoute ses attributs. Les mixins sans `__init__` sont
   simplement sautés.
2. **Sauvegarde.** `avant_sauvegarde()` suit le MRO : `ValidationMixin` valide d'abord (et lève une erreur au besoin),
   puis passe la main à `HorodatageMixin`, qui met à jour `modifie_le`, puis à `Entite`, qui ne fait rien. Si la
   validation échoue, rien n'est enregistré.
3. **Validation.** `Produit.valider` appelle `super().valider()` pour récupérer la liste de la base, puis ajoute ses
   propres erreurs.
4. **Journal.** `apres_sauvegarde()` descend d'abord jusqu'à `Entite`, puis `JournalMixin` écrit sa trace en remontant.
5. **Ordre = comportement.** Inverser `ValidationMixin` et `HorodatageMixin` dans la liste des parents ne casserait
   rien, mais l'horodatage serait mis à jour avant la validation. L'ordre des parents est donc une décision de
   conception.

Notez aussi que le deuxième produit (invalide) a consommé l'identifiant 2 : le client reçoit donc le numéro 3. C'est un
effet du constructeur de `Entite`, pas un bogue des mixins.

### Pourquoi `**kwargs` partout?

Pour que la chaîne `__init__` soit **coopérative** : chaque classe prélève ses propres arguments et transmet le reste.
Si un argument inconnu parvient jusqu'à `object.__init__`, Python lève une `TypeError`, ce qui signale immédiatement une
faute de frappe :

```python
Client("x@y.z", couleur="rouge")
# TypeError: object.__init__() takes exactly one argument (the instance to initialize)
```

### Pistes d'exercices

- Ajouter un `CacheMixin` qui mémorise le résultat de `to_dict()`.
- Créer une classe `Facture` qui utilise `ValidationMixin`, `SerialisationMixin` et `PersistableMixin` seulement.
- Écrire un `ArchivageMixin` qui ajoute un attribut `archive` et refuse de sauvegarder un objet archivé.
- Prédire, puis vérifier avec `__mro__`, l'ordre des appels si `JournalMixin` est placé en premier dans `Produit`.

## 5. Pièges, bonnes pratiques et alternatives

Les mixins sont puissants mais reposent sur des conventions : les erreurs courantes viennent presque toujours d'un oubli
de ces conventions.

### Les pièges classiques

- **Mixin placé après la classe de base.** Dans `class X(Base, Mixin)`, si `Base` définit déjà la méthode, celle du
  mixin n'est jamais appelée. Placez toujours les mixins à gauche.
- **MRO impossible.** Mettre `object` avant un mixin, comme dans `class X(object, Mixin)`, lève une `TypeError` («
  Cannot create a consistent method resolution order »), car `Mixin` hérite lui-même de `object`.
- **Oublier `super()`.** Un mixin qui redéfinit une méthode sans appeler `super()` coupe la chaîne : les mixins suivants
  et la classe de base ne sont plus exécutés.
- **Dépendances cachées.** Un mixin qui lit `self.prix` sans le dire plante avec une `AttributeError` dès qu'on le
  mélange à une classe qui n'a pas cet attribut. Documentez l'exigence, ou exprimez-la avec un protocole (section 4).
- **Collisions de noms.** Deux mixins qui définissent la même méthode ou le même attribut se masquent l'un l'autre.
  Gardez des noms précis, et préfixez les attributs internes (`_cache_json`).
- **Mixin qui devient une classe de base.** S'il a un état important, un `__init__` complexe, ou qu'on le comprend mal
  sans les autres, ce n'est plus un mixin.
- **Trop de mixins.** Au-delà de trois ou quatre, le MRO devient difficile à lire : c'est un signal pour revoir la
  conception.

### Liste de vérification avant d'écrire un mixin

- Peut-on résumer son rôle en une phrase qui commence par « Ajoute… »?
- Son nom se termine-t-il par `Mixin`?
- A-t-il peu ou pas d'état propre?
- Utilise-t-il `super()` partout où il redéfinit une méthode?
- Documente-t-il ce qu'il exige de la classe hôte?
- Fonctionnerait-il avec des classes sans aucun lien entre elles?

Une réponse négative à l'une de ces questions mérite qu'on s'arrête.

### Mixin, protocole, composition ou héritage simple?

Les mixins ne sont qu'un outil parmi d'autres. Voici comment choisir :

| Outil           | Fournit du code?     | À privilégier quand                                                                               |
|-----------------|----------------------|---------------------------------------------------------------------------------------------------|
| Héritage simple | Oui                  | Les classes forment une vraie relation « est un »                                                 |
| Mixin           | Oui                  | Plusieurs classes sans lien doivent partager un petit comportement                                |
| Protocole       | Non                  | On veut seulement décrire ce qu'un objet sait faire, sans l'obliger à hériter de quoi que ce soit |
| Composition     | Oui (par délégation) | Le comportement a un état propre ou doit pouvoir changer à l'exécution                            |

Règle pratique : commencez par la composition ou l'héritage simple, et passez aux mixins quand vous répétez le même
petit comportement dans des classes qui n'ont rien en commun.

### En résumé

- Un mixin est une petite classe qui ajoute **un** comportement; il exprime « peut faire », pas « est un ».
- En Python, c'est de l'héritage multiple discipliné : aucun mot-clé, seulement des conventions.
- Les mixins se placent **avant** la classe de base, et s'enchaînent avec `super()` selon le MRO.
- Un mixin documente (ou décrit par un protocole) ce qu'il attend de sa classe hôte.
- L'ordre des parents est une décision de conception, pas un détail.
