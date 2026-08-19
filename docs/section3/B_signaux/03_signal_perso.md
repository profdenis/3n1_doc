# **3. Définition et utilisation de signaux personnalisés**

## Qu'est-ce que `Signal` et comment l'utiliser ?

**`Signal`** est utilisé dans PySide6 pour définir des signaux personnalisés que vos objets peuvent émettre. Les signaux
sont une partie centrale de l'architecture événementielle de Qt, permettant la communication entre objets. Vous les
utilisez pour notifier d'autres parties de votre application lorsqu'un événement se produit - comme un changement de
valeur, une tâche terminée ou une action utilisateur.

### Quand et pourquoi utiliser `Signal`

- Utilisez `Signal` lorsque vous souhaitez que votre classe personnalisée (généralement une sous-classe de `QObject`)
  notifie d'autres objets d'événements ou de changements d'état.
- Cela est particulièrement utile pour le découplage : l'objet émettant le signal n'a pas besoin de savoir qui le
  reçoit.

### Comment définir et utiliser un signal personnalisé

#### 1. Définir le signal comme attribut de classe

Les signaux doivent être définis comme attributs de classe dans une sous-classe de `QObject` :

```python
from PySide6.QtCore import QObject, Signal


class Counter(QObject):
    # Définir un signal qui émet un entier
    valueChanged = Signal(int)
```

#### 2. Connecter le signal à un slot

Un slot est toute fonction appelable (fonction ou méthode) qui doit répondre au signal :

```python
def print_value(value):
    print(f"Valeur du compteur : {value}")


counter = Counter()
counter.valueChanged.connect(print_value)
```

#### 3. Émettre le signal

Lorsque votre objet veut notifier les autres, il appelle `.emit()` sur le signal :

```python
counter.valueChanged.emit(42)  # Cela appellera print_value(42)
```

#### 4. Tout mettre ensemble : un exemple minimal

```python title="signal_perso.py"
from PySide6.QtCore import QObject, Signal


class Counter(QObject):
    valueChanged = Signal(int)  # Définir un signal personnalisé

    def __init__(self):
        super().__init__()
        self._value = 0

    def increment(self):
        self._value += 1
        self.valueChanged.emit(self._value)  # Émettre le signal


def handle_value(value):
    print(f"Valeur du compteur : {value}")


counter = Counter()
counter.valueChanged.connect(handle_value)
counter.increment()  # Sortie : Valeur du compteur : 1
```

### Points clés

- **Définir** les signaux comme attributs de classe en utilisant `Signal`.
- **Connecter** les signaux aux slots (fonctions/méthodes) en utilisant `.connect()`.
- **Émettre** le signal avec `.emit()` pour notifier tous les slots connectés.
- Les signaux peuvent transporter des arguments, et vous pouvez définir leurs types (par exemple `Signal(int, str)`).
- Utilisez les signaux personnalisés pour implémenter une communication propre et découplée entre objets dans votre
  application PySide6.

### Quand l'utiliser

- Lorsque vous souhaitez que votre objet notifie d'autres parties de votre programme de quelque chose qui s'est produit,
  sans coder ces relations.
- Exemple : Un modèle de données émet un signal lorsque ses données changent, et une vue se met à jour en réponse.

---

!!! info "En résumé"
    `Signal` vous permet de définir des événements que vos objets peuvent émettre. D'autres objets peuvent "écouter" ces
    événements en connectant des slots au signal. C'est une manière fondamentale de structurer les applications interactives
    pilotées par des événements dans PySide6.