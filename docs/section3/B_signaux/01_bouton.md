# **1. Introduction à la gestion des événements**

La gestion des événements est centrale pour créer des applications graphiques interactives. Dans PySide6, les événements
comme les clics sur boutons, les mouvements de souris ou les pressions de touches sont gérés à l'aide d'un mécanisme
puissant appelé **signaux et slots**. Ce système vous permet de répondre aux actions de l'utilisateur de manière propre
et découplée.

- **Signal** : Une notification d'événement émise par un widget (par exemple, un bouton émet un signal lorsqu'il est
  cliqué).
- **Slot** : Une fonction ou méthode Python qui est appelée en réponse à un signal.

Lorsque qu'un signal est émis (par exemple, lorsqu'un bouton est cliqué), tout slot connecté est exécuté. C'est le cœur
de la programmation événementielle dans PySide6.

## Événements implémentés avec des signaux dans Qt

Dans Qt (et donc PySide6), la plupart des actions utilisateur (événements) sont implémentées comme des signaux.
Les widgets émettent des signaux lorsqu'un événement se produit (comme un clic sur un bouton), et vous connectez ces
signaux à des slots (fonctions) pour définir ce qui doit se produire en réponse.

Cela n'est pas exactement la même chose que le
*pattern Observer-Observable*, mais *signals and slots* jouent un rôle similaire. Dans une certaine mesure, les widgets
sont des _observables_, et les slots sont des _observers_, et les signaux sont utilisés par les observables (widgets)
pour contacter (ou exécuter) les observateurs (slots).

## Exemple : Un bouton qui affiche un nombre aléatoire

Voici un exemple minimal PySide6 avec un bouton et une étiquette. Lorsque le bouton est cliqué, un entier aléatoire
entre 1 et 100 (inclus) est affiché dans l'étiquette.

```python
import sys
import random
from PySide6.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QLabel


class RandomNumberApp(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        self.layout = QVBoxLayout()

        self.label = QLabel("Cliquez sur le bouton pour obtenir un nombre aléatoire !", self)
        self.button = QPushButton("Générer un nombre aléatoire", self)

        self.layout.addWidget(self.label)
        self.layout.addWidget(self.button)
        self.setLayout(self.layout)

        # Connexion du signal 'clicked' du bouton au slot (fonction de gestion)
        self.button.clicked.connect(self.show_random_number)

    def show_random_number(self):
        number = random.randint(1, 100)
        self.label.setText(f"Nombre aléatoire : {number}")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = RandomNumberApp()
    window.setWindowTitle("Générateur de nombres aléatoires")
    window.show()
    sys.exit(app.exec())
```

### Points clés

- Le signal `clicked` du bouton est connecté à la méthode `show_random_number`, qui est appelée chaque fois que le
  bouton est pressé.
- L'application utilise `app.exec()` pour démarrer la boucle d'événements, comme requis dans PySide6.
- Tous les widgets sont importés de `PySide6.QtWidgets`.

C'est la manière recommandée de gérer les événements (signaux et slots) dans PySide6.

## Résumé

- PySide6 utilise **signals and slots** pour la gestion des événements.
- Les signaux sont émis par les widgets lorsqu'ils se produisent (comme un clic sur un bouton).
- Les slots sont des fonctions qui répondent à ces signaux.
- La connexion des signaux aux slots vous permet de définir des comportements interactifs dans votre interface
  graphique.

Cet exemple démontre le schéma de base que vous utiliserez tout au long du développement avec PySide6 : connectez les
signaux des widgets à vos propres fonctions pour faire répondre votre application aux actions de l'utilisateur.
