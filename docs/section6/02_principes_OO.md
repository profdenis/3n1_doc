# Principes de Conception Orientée Objet

Ce document rassemble les principes fondamentaux, bonnes pratiques et heuristiques de conception logicielle orientée
objet. Leur objectif commun est d'optimiser l'efficacité du développement, de minimiser la dette technique et de
maximiser la maintenabilité, la lisibilité et la testabilité des systèmes logiciels.

---

## Clean Code : Concepts Clés

Le livre *Clean Code: A Handbook of Agile Software Craftsmanship* de Robert C. Martin (« Uncle Bob ») synthétise les
pratiques permettant d'écrire du code de haute qualité, durable et facilement transmissible :

1. **Code propre (*Clean Code*)** : Un code élégant, lisible et structuré, rédigé avec soin pour permettre à tout
   développeur d'en comprendre l'intention et de le faire évoluer sans effort inutile.
2. **Noms significatifs** : Choisir des identifiants (variables, fonctions, classes) explicites, sans ambiguïté, qui
   révèlent immédiatement leur intention métier ou technique.
3. **Fonctions courtes et focalisées** : Une fonction doit être brève, respecter un niveau d'abstraction unique et
   accomplir une seule tâche de manière exhaustive.
4. **Usage raisonné des commentaires** : Privilégier le code auto-documenté. Un commentaire doit expliquer le *pourquoi*
   (l'intention, le contexte métier) et non le *quoi* (ce que le code exécute déjà clairement).
5. **Formatage cohérent** : Adopter une mise en forme uniforme et claire pour faciliter le parcours visuel et la
   compréhension collective du code.
6. **Gestion rigoureuse des erreurs** : Traiter les cas d'erreur de façon explicite via des exceptions typées plutôt que
   par des codes de retour ambigus.
7. **Élimination de la duplication** : Réduire la redondance logique en favorisant la factorisation et l'abstraction
   pour éviter les dérives de maintenance.
8. **Principes SOLID** : Appliquer les cinq principes fondamentaux de conception objet pour garantir la modularité et la
   pérennité de l'architecture.
9. **Refactorisation continue** : Identifier et éliminer régulièrement les « odeurs de code » (*code smells*) sous la
   protection d'une suite de tests automatisés.

---

## Les Principes SOLID

Les principes **SOLID** constituent un ensemble de cinq règles de conception orientée objet formulées par Robert C.
Martin. Ils visent à construire des architectures robustes, faiblement couplées, hautement cohésives et faciles à
étendre et à tester.

| Lettre | Principe                            | Intitulé français          | Objectif principal                                                                          |
|:------:|:------------------------------------|:---------------------------|:--------------------------------------------------------------------------------------------|
| **S**  | **Single Responsibility Principle** | Responsabilité Unique      | Une classe ne doit avoir qu'une seule raison de changer.                                    |
| **O**  | **Open/Closed Principle**           | Ouvert / Fermé             | Ouvert à l'extension, fermé à la modification.                                              |
| **L**  | **Liskov Substitution Principle**   | Substitution de Liskov     | Une sous-classe doit pouvoir remplacer sa classe mère sans altérer le comportement attendu. |
| **I**  | **Interface Segregation Principle** | Ségrégation des Interfaces | Préférer plusieurs interfaces spécifiques à une seule interface générale.                   |
| **D**  | **Dependency Inversion Principle**  | Inversion des Dépendances  | Dépendre des abstractions, pas des implémentations concrètes.                               |

---

### S — Responsabilité Unique (Single Responsibility Principle - SRP)

> *« Une classe ou un module ne doit avoir qu'une et une seule raison de changer. »*

#### Explication

Chaque classe, module ou fonction doit être responsable d'une seule partie de la fonctionnalité du système. Lorsqu'une
classe cumule plusieurs responsabilités (par exemple la logique métier, la persistance des données et la génération de
l'affichage), toute modification sur un aspect risque d'introduire des régressions sur les autres.

#### Exemple en Python

❌ **Violation : une classe avec plusieurs responsabilités**

```python
class RapportUtilisateur:
    def __init__(self, nom: str, email: str):
        self.nom = nom
        self.email = email

    # Responsabilité 1 : formatage / présentation
    def generer_html(self) -> str:
        return f"<div><h1>{self.nom}</h1><p>{self.email}</p></div>"

    # Responsabilité 2 : persistance / accès aux données
    def sauvegarder_en_base(self) -> None:
        print(f"Sauvegarde de l'utilisateur {self.nom} dans la base de données...")
```

✅ **Conception conforme : séparation des responsabilités**

```python
from dataclasses import dataclass


# Responsabilité 1 : modèle de données
@dataclass
class Utilisateur:
    nom: str
    email: str


# Responsabilité 2 : formatage / présentation
class GenerateurRapportHTML:
    def generer(self, utilisateur: Utilisateur) -> str:
        return f"<div><h1>{utilisateur.nom}</h1><p>{utilisateur.email}</p></div>"


# Responsabilité 3 : persistance
class DepotUtilisateur:
    def sauvegarder(self, utilisateur: Utilisateur) -> None:
        print(f"Sauvegarde de l'utilisateur {utilisateur.nom} dans la base de données...")
```

#### Bénéfices

- **Isolation des changements** : Modifier le format de rendu (HTML vers PDF) n'impacte pas la persistance ni le modèle.
- **Testabilité accrue** : Chaque composant peut être testé unitairement en toute indépendance.

---

### O — Ouvert / Fermé (Open/Closed Principle - OCP)

> *« Les entités logicielles doivent être ouvertes à l'extension, mais fermées à la modification. »*

#### Explication

Il doit être possible d'étendre le comportement d'un module (ajouter de nouveaux cas, de nouveaux types de traitements)
sans modifier son code source existant et testé. Ce principe repose généralement sur le polymorphisme, les interfaces ou
l'injection de stratégies.

#### Exemple en Python

❌ **Violation : modification du code existant à chaque nouvel ajout**

```python
class CalculateurRemise:
    def calculer(self, montant: float, type_client: str) -> float:
        # Chaque nouveau statut oblige à modifier cette méthode
        if type_client == "standard":
            return montant
        elif type_client == "vip":
            return montant * 0.8
        elif type_client == "etudiant":
            return montant * 0.9
        raise ValueError(f"Type de client inconnu : {type_client}")
```

✅ **Conception conforme : extension par polymorphisme / stratégie**

```python
from abc import ABC, abstractmethod


class RegleRemise(ABC):
    @abstractmethod
    def appliquer(self, montant: float) -> float:
        pass


class RemiseStandard(RegleRemise):
    def appliquer(self, montant: float) -> float:
        return montant


class RemiseVIP(RegleRemise):
    def appliquer(self, montant: float) -> float:
        return montant * 0.8


class RemiseEtudiant(RegleRemise):
    def appliquer(self, montant: float) -> float:
        return montant * 0.9


class CalculateurRemise:
    def calculer(self, montant: float, regle: RegleRemise) -> float:
        return regle.appliquer(montant)
```

#### Bénéfices

- **Stabilité** : L'ajout d'une nouvelle règle de remise ne modifie aucune ligne de code existante.
- **Réduction des régressions** : Le code existant conserve sa validité sans risque d'effets de bord.

---

### L — Substitution de Liskov (Liskov Substitution Principle - LSP)

> *« Les sous-types doivent être substituables à leurs types de base sans altérer la cohérence ou la validité du
programme. »*

#### Explication

Formulé par Barbara Liskov, ce principe impose qu'une classe dérivée respecte le contrat de sa classe de base : elle ne
doit ni restreindre les préconditions, ni affaiblir les postconditions, ni lever d'exceptions inattendues pour les
méthodes héritées.

#### Exemple en Python

❌ **Violation : une sous-classe qui brise le contrat de la superclasse**

```python
class Oiseau:
    def voler(self) -> str:
        return "Je vole dans les airs."


class Autruche(Oiseau):
    def voler(self) -> str:
        # L'autruche ne vole pas : exception inattendue pour le code appelant
        raise NotImplementedError("Les autruches ne peuvent pas voler !")


def faire_voler(oiseau: Oiseau) -> None:
    print(oiseau.voler())  # Échoue si l'on passe une Autruche
```

✅ **Conception conforme : hiérarchie basée sur les capacités réelles**

```python
from abc import ABC, abstractmethod


class Oiseau(ABC):
    @abstractmethod
    def se_deplacer(self) -> str:
        pass


class OiseauVolant(Oiseau):
    def se_deplacer(self) -> str:
        return "Je vole dans les airs."


class Autruche(Oiseau):
    def se_deplacer(self) -> str:
        return "Je cours rapidement sur le sol."


def deplacer_animal(oiseau: Oiseau) -> None:
    print(oiseau.se_deplacer())  # Fonctionne de manière homogène pour tout oiseau
```

#### Bénéfices

- **Prévisibilité** : Le polymorphisme fonctionne en toute sécurité, sans vérifications de type (`isinstance`) au
  runtime.
- **Fiabilité architecturale** : Les contrats d'interface sont strictement garantis.

---

### I — Ségrégation des Interfaces (Interface Segregation Principle - ISP)

> *« Aucun client ne doit être contraint de dépendre de méthodes qu'il n'utilise pas. »*

#### Explication

Il est préférable de définir plusieurs interfaces fines, spécialisées et cohérentes plutôt qu'une interface volumineuse
(« grasse ») imposant aux classes d'implémenter des méthodes inutiles ou vides.

#### Exemple en Python

❌ **Violation : interface surchargée forçant des implémentations factices**

```python
from abc import ABC, abstractmethod


class AppareilMultifonction(ABC):
    @abstractmethod
    def imprimer(self, document: str) -> None:
        pass

    @abstractmethod
    def scanner(self) -> str:
        pass

    @abstractmethod
    def faxer(self, document: str) -> None:
        pass


class ImprimanteSimple(AppareilMultifonction):
    def imprimer(self, document: str) -> None:
        print(f"Impression : {document}")

    def scanner(self) -> str:
        raise NotImplementedError("Scanner non supporté.")

    def faxer(self, document: str) -> None:
        raise NotImplementedError("Fax non supporté.")
```

✅ **Conception conforme : interfaces modulaires et ciblées avec `Protocol`**

```python
from typing import Protocol


class Imprimable(Protocol):
    def imprimer(self, document: str) -> None:
        ...


class Scannable(Protocol):
    def scanner(self) -> str:
        ...


class Faxable(Protocol):
    def faxer(self, document: str) -> None:
        ...


class ImprimanteSimple:
    def imprimer(self, document: str) -> None:
        print(f"Impression : {document}")


class PhotocopieuseComplete:
    def imprimer(self, document: str) -> None:
        print(f"Impression : {document}")

    def scanner(self) -> str:
        return "Numérisation terminée."

    def faxer(self, document: str) -> None:
        print(f"Envoi par fax : {document}")


# Les fonctions clientes ne dépendent que des protocoles requis
def lancer_impression(appareil: Imprimable, document: str) -> None:
    appareil.imprimer(document)
```

#### Bénéfices

- **Faible couplage** : Les consommateurs ne dépendent que des fonctionnalités dont ils ont strictement besoin.
- **Modularité** : Combinaison flexible des compétences par composition ou héritage multiple ciblé.

---

### D — Inversion des Dépendances (Dependency Inversion Principle - DIP)

> *« Les modules de haut niveau ne doivent pas dépendre des modules de bas niveau. Tous deux doivent dépendre
d'abstractions. Les abstractions ne doivent pas dépendre des détails ; les détails doivent dépendre des abstractions. »*

#### Explication

Les composants métier (haut niveau) ne doivent pas instancier directement les composants techniques d'infrastructure
(bas niveau : bases de données, envoi de SMS, API externes). Ils collaborent à travers des contrats abstraits
(interfaces ou protocoles), et les dépendances concrètes sont injectées à la création.

#### Exemple en Python

❌ **Violation : dépendance directe d'une classe métier vers un service technique**

```python
class ServiceSMS:
    def envoyer(self, destinataire: str, message: str) -> None:
        print(f"Envoi du SMS à {destinataire} : {message}")


class GestionnaireCommandes:
    def __init__(self):
        # Couplage fort : dépendance directe vers l'implémentation concrète
        self.service_sms = ServiceSMS()

    def valider_commande(self, client: str) -> None:
        # Logique métier...
        self.service_sms.envoyer(client, "Votre commande est validée.")
```

✅ **Conception conforme : injection d'une abstraction**

```python
from typing import Protocol


# Abstraction (contrat)
class ServiceNotification(Protocol):
    def envoyer(self, destinataire: str, message: str) -> None:
        ...


class ServiceSMS:
    def envoyer(self, destinataire: str, message: str) -> None:
        print(f"SMS à {destinataire} : {message}")


class ServiceEmail:
    def envoyer(self, destinataire: str, message: str) -> None:
        print(f"Email à {destinataire} : {message}")


class GestionnaireCommandes:
    def __init__(self, notification: ServiceNotification):
        # Dépendance vers l'abstraction injectée
        self.notification = notification

    def valider_commande(self, client: str) -> None:
        # Logique métier...
        self.notification.envoyer(client, "Votre commande est validée.")
```

#### Bénéfices

- **Interchangeabilité** : Basculer d'un canal SMS vers un canal Email ou un mock de test sans modifier la logique
  métier.
- **Testabilité optimale** : Facilité totale d'injection de simulations ou de bouchons unitaire.

---

## Autres Principes et Bonnes Pratiques

### DRY vs WET

- **DRY (*Don't Repeat Yourself*)** : Chaque portion de connaissance ou de logique métier doit avoir une représentation
  unique, non ambiguë et faisant autorité au sein du système. La centralisation évite les oublis lors des modifications
  futures.
- **WET (*Write Everything Twice* ou *We Enjoy Typing*)** : Antipattern désignant la duplication répétée de code,
  augmentant le coût de maintenance et les risques de bugs divergents.

> **Nuance pragmatique** : DRY cible la duplication de la **logique métier**, non la similitude fortuite de deux
> structures de code ayant des raisons d'évoluer distinctement. Factoriser prématurément deux portions de code
> indépendantes crée un couplage artificiel indésirable.

---

### KISS (Keep It Simple, Stupid)

Le principe **KISS** préconise de privilégier la simplicité de conception et de proscrire la sur-ingénierie
(*over-engineering*).

- Choisir la solution la plus directe et compréhensible répondant aux exigences actuelles.
- Éviter d'anticiper des besoins hypothétiques qui complexifient inutilement la base de code.
- Un code simple est plus facile à relire, auditer, débugger et maintenir sur le long terme.

---

### Loi de Déméter (Law of Demeter - LoD)

Aussi appelée **Principe de moindre connaissance**, cette loi impose qu'un objet communique uniquement avec ses voisins
immédiats et ne navigue pas à travers la structure interne d'objets tiers.

Une méthode `M` d'un objet `O` ne doit appeler que les méthodes :

1. De `O` lui-même ;
2. Des paramètres passés à `M` ;
3. Des objets instanciés au sein de `M` ;
4. Des attributs directs composants de `O`.

❌ **Violation (chaînage excessif de dépendances / train de méthodes)** :

```python
# L'objet courant dépend de la structure interne de Client, Adresse et Ville
code_postal = commande.get_client().get_adresse().get_ville().get_code_postal()
```

✅ **Conception conforme** :

```python
# Délégation au voisin direct
code_postal = commande.obtenir_code_postal_livraison()
```

---

### Tell, Don't Ask

> *« Dites à l'objet ce qu'il doit accomplir plutôt que de lui demander ses données pour décider à sa place. »*

Ce principe favorise l'encapsulation en regroupant les données et les opérations qui les manipulent au sein du même
objet.

❌ **Violation (interrogation de l'état interne puis manipulation externe)** :

```python
class Chauffeur:
    def conduire(self, voiture: Voiture) -> None:
        if voiture.niveau_carburant > 0:
            voiture.niveau_carburant -= 1
            voiture.vitesse += 10
```

✅ **Conception conforme (ordre donné à l'objet responsable)** :

```python
class Chauffeur:
    def conduire(self, voiture: Voiture) -> None:
        voiture.accelerer()


class Voiture:
    def __init__(self):
        self.niveau_carburant = 50
        self.vitesse = 0

    def accelerer(self) -> None:
        if self.niveau_carburant > 0:
            self.niveau_carburant -= 1
            self.vitesse += 10
```

---

### Orthogonalité

Deux composants sont **orthogonaux** si la modification de l'un n'entraîne aucun impact collatéral sur l'autre.

- **Isolation des anomalies** : Une défaillance dans un composant reste confinée localement.
- **Évolution facilitée** : La refonte d'un module (ex. remplacement de la base de données ou de l'interface graphique)
  s'effectue sans altérer la logique métier.
- **Réduction de la complexité cognitive** : Chaque composant peut être analysé et raisonné individuellement.

---

### Éviter l'Optimisation Prématurée

> *« Nous devrions oublier les petites économies, disons environ 97 % du temps : l'optimisation prématurée est la racine
de tous les maux. Pourtant, nous ne devrions pas manquer nos chances dans ce 3 % critique. »*  
> — **Donald Knuth**

- Concevoir d'abord un code clair, correct et maintenable.
- N'optimiser que lorsque des mesures concrètes (profilage, métriques de performance) identifient un goulet
  d'étranglement avéré.
- Les optimisations prématurées complexifient souvent le code pour des gains marginaux voire inexistants.

---

### Règle des Cinq Lignes

Heuristique suggérant qu'une fonction ou méthode gagne à être concise (de l'ordre de 5 à 10 lignes de code effectif)
pour maximiser :

1. **La clarté immédiate** : Intention comprise en un coup d'œil.
2. **La focalisation** : Une seule opération élémentaire par fonction.
3. **La couverture de test** : Moins de branches conditionnelles et de cas limites à valider.

---

### Commentaires : Expliquer le « Pourquoi », pas le « Quoi »

- **À proscrire** : Les commentaires paraphrasant le code (`i += 1  # incrémente i de 1`).
- **À rechercher** : Les commentaires documentant les décisions non triviales, contraintes métier, choix d'algorithmes
  spécifiques ou contournements indispensables liés à des dépendances externes.

---

### Principes et Pratiques de Refactorisation

La **refactorisation** est le processus d'amélioration de la structure interne d'un code sans altérer son comportement
observable externe.

1. **Règle de Trois** : À la troisième duplication d'une logique similaire, factoriser dans une fonction ou classe
   dédiée.
2. **Refactoriser en continu (*Boy Scout Rule*)** : Laisser le code dans un état plus propre qu'on ne l'a trouvé lors de
   chaque intervention.
3. **Décomposition progressive** : Extraire des sous-fonctions jusqu'à ce que chaque unité réponde à un niveau
   d'abstraction homogène.
4. **Garantie par les tests** : Disposer d'une suite de tests unitaires automatisés avant toute opération de
   refactorisation afin de détecter immédiatement toute régression.
5. **Assistance outillée** : Tirer parti des fonctionnalités automatisées de refactorisation offertes par l'IDE
   (renommage sécurisé, extraction de méthode, déplacement de symbole).

---

### Catalogue des Odeurs de Code (*Code Smells*)

Les odeurs de code sont des indicateurs visuels et structurels signalant des défauts de conception potentiels :

| Odeur de code                                        | Symptôme                                                                        | Risque / Impact                                            | Piste de refactorisation                                    |
|:-----------------------------------------------------|:--------------------------------------------------------------------------------|:-----------------------------------------------------------|:------------------------------------------------------------|
| **Méthode Longue (*Long Method*)**                   | Fonction réalisant trop de traitements.                                         | Lisibilité faible, tests complexes.                        | Extraire des méthodes (*Extract Method*).                   |
| **Classe Volumineuse (*Large Class*)**               | Classe concentrant trop de champs et responsabilités.                           | Violation du SRP, couplage élevé.                          | Extraire des classes spécialisées (*Extract Class*).        |
| **Code Dupliqué (*Duplicate Code*)**                 | Blocs de code identiques ou très proches.                                       | Risque de bugs divergents lors des mises à jour.           | Factoriser dans une fonction ou classe partagée.            |
| **Obsession Primitive (*Primitive Obsession*)**      | Utilisation exclusive de types de base (`str`, `int`) pour des concepts métier. | Absence de validation centralisée, perte de sens.          | Créer des objets-valeurs (*Value Objects* / Dataclasses).   |
| **Envie de Fonctionnalité (*Feature Envy*)**         | Une méthode manipule plus les données d'une autre classe que les siennes.       | Mauvaise répartition des responsabilités.                  | Déplacer la méthode dans la classe cible (*Move Method*).   |
| **Objet Dieu (*God Object*)**                        | Une classe centrale omnisciente contrôlant l'ensemble du système.               | Goulot d'étranglement architectural, maintenance critique. | Redistribuer les responsabilités selon les principes SOLID. |
| **Amas de Données (*Data Clumps*)**                  | Groupes de variables passant toujours ensemble en paramètres.                   | Signature de fonction lourde, logique dispersée.           | Regrouper dans un objet ou une structure de données.        |
| **Conditions Multiples (*Switch Statements*)**       | Enchaînements de `switch` ou `if/elif` sur des types d'objets.                  | Violation de l'OCP lors de l'ajout de variantes.           | Remplacer par du polymorphisme ou le patron Stratégie.      |
| **Intimité Inappropriée (*Inappropriate Intimacy*)** | Classes accédant excessivement aux détails privés les unes des autres.          | Couplage fort, rupture d'encapsulation.                    | Rapprocher les méthodes ou réduire la visibilité.           |
