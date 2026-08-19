# **2. Exemple avec un curseur et un cadran**

Voici un exemple PySide6 avec un curseur (`QSlider`), un cadran (`QDial`) et une étiquette qui restent synchronisés (
valeurs de 1 à 10) :

```python title="synchro1.py"
import sys
from PySide6.QtWidgets import QApplication, QWidget, QSlider, QDial, QLabel, QVBoxLayout
from PySide6.QtCore import Qt


class LinkedControlsApp(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()

        # Création des contrôles avec une plage de 1-10
        self.slider = QSlider(Qt.Orientation.Horizontal)
        self.dial = QDial()
        self.label = QLabel("Valeur : 1")

        # Définition des plages
        self.slider.setRange(1, 10)
        self.dial.setRange(1, 10)

        # Ajout au layout
        layout.addWidget(self.slider)
        layout.addWidget(self.dial)
        layout.addWidget(self.label)
        self.setLayout(layout)

        # Connexion des signaux avec prévention des boucles
        self.slider.valueChanged.connect(self.update_controls)
        self.dial.valueChanged.connect(self.update_controls)

    def update_controls(self, value):
        # Prévention des boucles de signaux
        sender = self.sender()

        if isinstance(sender, QSlider):
            widget = self.dial
        else:
            widget = self.slider

        widget.blockSignals(True)
        widget.setValue(value)
        widget.blockSignals(False)

        self.label.setText(f"Valeur : {value}")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = LinkedControlsApp()
    window.setWindowTitle("Démonstration de contrôles synchronisés")
    window.show()
    sys.exit(app.exec())
```

### Fonctionnalités clés

1. **Contrôles synchronisés** (`QSlider` et `QDial`) :
    - Le déplacement d'un contrôle met à jour l'autre instantanément
    - `blockSignals()` empêche les boucles de mise à jour infinies

2. **Affichage de la valeur** (`QLabel`) :
    - Affiche automatiquement la valeur actuelle (1-10)
    - Se met à jour à chaque changement de contrôle

3. **Gestion des plages** :
    - Les deux contrôles sont limités à 1-10 avec `setRange()`
    - Valeurs entières uniquement par défaut

### Utilisation

- Faites glisser le curseur horizontal ou faites tourner le cadran
- Les deux contrôles et l'étiquette resteront synchronisés
- Les valeurs s'enroulent automatiquement entre 1 et 10

Cet exemple démontre le mécanisme signal/slot de PySide6 tout en gérant les défis courants de synchronisation dans le
développement d'interfaces graphiques.

## Version alternative avec un attribut d'instance

Voici une version modifiée de `LinkedControlsApp` qui stocke explicitement la valeur actuelle dans un attribut
d'instance et utilise une méthode setter pour gérer les mises à jour :

```python title="synchro2.py"
import sys
from PySide6.QtWidgets import QApplication, QWidget, QSlider, QDial, QLabel, QVBoxLayout
from PySide6.QtCore import Qt


class DialWithLabel(QWidget):
    """
    Widget composite qui regroupe un QDial et un QLabel.
    Le label affiche toujours la valeur actuelle du cadran.
    Ce widget fournit une méthode setValue pour mettre à jour le cadran et le label ensemble.
    """

    def __init__(self, min_val, max_val):
        """
        Initialise le cadran et le label, et configure le layout.

        Args:
            min_val (int): Valeur minimale pour le cadran.
            max_val (int): Valeur maximale pour le cadran.
        """
        super().__init__()
        self.dial = QDial()
        self.label = QLabel()

        # Configuration du cadran
        self.dial.setNotchesVisible(True)
        self.dial.setRange(min_val, max_val)

        # Configuration du label
        self.label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # Disposition verticale des widgets
        layout = QVBoxLayout()
        layout.addWidget(self.dial)
        layout.addWidget(self.label)
        self.setLayout(layout)

    def setValue(self, value):
        """
        Définit la valeur du cadran et met à jour le label pour correspondre.

        Args:
            value (int): La valeur à définir sur le cadran et à afficher sur le label.
        """
        self.dial.setValue(value)
        self.label.setText(f"Valeur : {value}")


class LinkedControlsApp(QWidget):
    """
    Fenêtre principale de l'application.
    Contient un QSlider et un DialWithLabel.
    Garde les deux contrôles synchronisés, donc changer l'un met à jour l'autre.
    """

    def __init__(self):
        """
        Initialise la fenêtre de l'application et les contrôles.
        """
        super().__init__()
        self.current_value = 1  # Stocke la valeur actuelle partagée par le curseur et le cadran
        self.init_ui()

    def init_ui(self):
        """
        Configure l'interface utilisateur, connecte les signaux et initialise les valeurs des contrôles.
        """
        layout = QVBoxLayout()

        # Création du curseur et du widget composite cadran-avec-label
        self.slider = QSlider(Qt.Orientation.Horizontal)
        self.dial_widget = DialWithLabel(1, 10)

        # Définition de la plage du curseur pour correspondre au cadran
        self.slider.setRange(1, 10)

        # Ajout des widgets au layout
        layout.addWidget(self.slider)
        layout.addWidget(self.dial_widget)
        self.setLayout(layout)

        # Connexion des signaux valueChanged à la méthode de synchronisation
        self.slider.valueChanged.connect(self.set_current_value)
        self.dial_widget.dial.valueChanged.connect(self.set_current_value)

        # Définition des valeurs initiales pour les deux contrôles
        self.slider.setValue(self.current_value)
        self.dial_widget.setValue(self.current_value)

    def set_current_value(self, value):
        """
        Synchronise le curseur et le cadran pour qu'ils affichent toujours la même valeur.
        Met également à jour le label dans le widget du cadran.

        Args:
            value (int): La nouvelle valeur à définir sur les deux contrôles.
        """
        self.current_value = value

        # Détermine quel widget doit être mis à jour
        if self.sender() == self.slider:
            # Si le curseur a changé, met à jour le widget du cadran
            widget = self.dial_widget
        else:
            # Si le cadran a changé, met à jour le curseur et le label du widget du cadran
            widget = self.slider
            self.dial_widget.setValue(value)

        # Empêche les boucles de rétroaction des signaux lors de la mise à jour de l'autre widget
        widget.blockSignals(True)
        widget.setValue(value)
        widget.blockSignals(False)


if __name__ == "__main__":
    # Configuration standard d'une application PySide6
    app = QApplication(sys.argv)
    window = LinkedControlsApp()
    window.setWindowTitle("Contrôles synchronisés avec état")
    window.show()
    sys.exit(app.exec())
```

### Améliorations clés

1. **Gestion explicite de l'état** :
    - `self.current_value` stocke l'état actuel
    - Toutes les mises à jour des widgets dérivent de cette source unique de vérité

2. **Méthode setter dédiée** :
    - `set_current_value` gère les mises à jour d'état
    - Garantit que l'état et l'interface restent synchronisés
    - Empêche les boucles infinies en utilisant `blockSignals()`

3. **Initialisation** :
    - Les deux contrôles sont initialisés à `self.current_value`
    - Le label affiche la valeur initiale depuis l'attribut d'instance

4. **Encapsulation** :
    - La modification de l'état se fait uniquement par le setter
    - Les mises à jour de l'interface sont centralisées dans une méthode

### Notes d'utilisation

- L'attribut d'instance (`current_value`) agit comme la source de vérité
- Toute modification externe de `current_value` doit passer par `set_current_value`
- Le setter garantit que tous les widgets et le label restent synchronisés
- Le blocage des signaux empêche les boucles de mise à jour infinies entre les widgets connectés

Ce schéma fournit une séparation claire entre la gestion d'état et les mises à jour de l'interface, ce qui le rend plus
facile à étendre ou modifier ultérieurement.

## Version alternative avec un widget personnalisé

### Modifications clés

1. **`DialWithLabel` possède maintenant une méthode `setValue`**
    - Cette méthode met à jour à la fois le cadran et le label ensemble, encapsulant la logique pour les garder
      synchronisés.
2. **Logique de synchronisation des widgets**
    - Dans `set_current_value`, vous utilisez maintenant `setValue` sur soit le curseur soit le widget composite (
      `DialWithLabel`), selon celui qui a déclenché l'événement.
    - Lorsque le cadran déclenche le changement, vous appelez explicitement `self.dial_widget.setValue(value)` avant de
      mettre à jour le curseur.
3. **Gestion des signaux plus propre**
    - Toutes les mises à jour de valeur des widgets sont enveloppées dans `blockSignals(True/False)` pour prévenir les
      boucles de rétroaction.
4. **Docstrings** :
    - Des chaînes de documentation (*docstrings*) ont été ajoutées pour chaque classe et méthode
    - D'autres commentaires ont été ajoutés pour aider à comprendre le code

#### 1. Encapsulation avec `setValue`

La classe `DialWithLabel` expose maintenant une méthode `setValue(value)`. C'est un excellent choix de conception car :

- Elle **encapsule** la logique de mise à jour du cadran et de son label en un seul endroit.
- L'application principale n'a pas besoin de savoir comment le label est mis à jour - elle appelle simplement
  `setValue`.

#### 2. Synchronisation simplifiée

Dans `LinkedControlsApp.set_current_value`, le widget qui doit être mis à jour est déterminé :

- Si c'est le **curseur** qui a changé, il met à jour le cadran (et le label) en utilisant
  `self.dial_widget.setValue(value)`.
- Si c'est le **cadran** qui a changé, il met à jour le curseur et appelle également `self.dial_widget.setValue(value)`
  pour s'assurer que le label est toujours à jour.

**Cela garantit :**

- Les deux contrôles affichent toujours la même valeur.
- Le label correspond toujours au cadran.

#### 3. Blocage des signaux

Les appels à `blockSignals(True)` et `blockSignals(False)` sont exécutés autour des appels `setValue`.

- Cela empêche les boucles infinies où changer un widget déclencherait le signal de l'autre, qui déclencherait alors le
  premier à nouveau, et ainsi de suite.
- C'est une technique standard PySide6 pour synchroniser les widgets.

#### 4. Réutilisabilité

Le widget `DialWithLabel` est maintenant encore plus réutilisable. Toute partie de votre application peut l'utiliser et
simplement appeler `setValue()` pour mettre à jour à la fois le cadran et son label.

### Tableau récapitulatif

| Composant           | Responsabilité                                      | Amélioration dans votre version                             |
|---------------------|-----------------------------------------------------|-------------------------------------------------------------|
| `DialWithLabel`     | Gère le cadran et le label ensemble                 | `setValue` met à jour le cadran et le label                 |
| `LinkedControlsApp` | Coordonne le curseur et le widget cadran-avec-label | Plus simple, appelle simplement `setValue` quand nécessaire |
| Gestion des signaux | Empêche les boucles de rétroaction                  | Utilise `blockSignals` autour de tous les appels `setValue` |

Ce schéma fournit une séparation claire entre la gestion d'état et les mises à jour de l'interface, ce qui le rend plus
facile à étendre ou modifier ultérieurement.