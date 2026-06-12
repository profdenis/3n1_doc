# **2. Exemple : Propagation et bulle des événements dans PySide6**

Lorsque vous interagissez avec les widgets dans une application PySide6, les événements (comme les clics de souris) sont
d'abord livrés au widget sous le curseur. Si ce widget ne gère pas complètement l'événement (c'est-à-dire qu'il appelle
`event.ignore()`), l'événement est ensuite "remonté" à son widget parent, et ainsi de suite, jusqu'à ce qu'il soit
traité ou atteigne la fenêtre de niveau supérieur.

Voici un exemple concis qui démontre cette propagation en utilisant des widgets personnalisés et la méthode `event()`.
Le widget enfant imprimera un message et ignorera l'événement, permettant au parent de répondre également :

```python
import sys
from PySide6.QtWidgets import QApplication, QFrame, QVBoxLayout, QLabel, QPushButton
from PySide6.QtCore import QEvent


class ChildButton(QPushButton):
    def event(self, event):
        if event.type() == QEvent.Type.MouseButtonPress:
            print("ChildButton : événement MouseButtonPress (ignoré, propagation vers le parent)")
            event.ignore()  # Permet à l'événement de se propager au parent
            return False
        return super().event(event)


class MainFrame(QFrame):
    def event(self, event):
        if event.type() == QEvent.Type.MouseButtonPress:
            print("MainFrame : événement MouseButtonPress (reçu du enfant)")
        return super().event(event)


app = QApplication(sys.argv)
main_frame = MainFrame()
main_frame.setWindowTitle("Démonstration de propagation d'événements")
layout = QVBoxLayout(main_frame)

label = QLabel("Cliquez sur le bouton ci-dessous")
layout.addWidget(label)

button = ChildButton("Cliquez ici")
layout.addWidget(button)

main_frame.setLayout(layout)
main_frame.show()
sys.exit(app.exec())
```

### **Ce qui se passe ici ?**

- Lorsque vous cliquez sur le bouton, la méthode `event()` de `ChildButton` est appelée en premier.
- Elle imprime un message et appelle `event.ignore()`, ce qui permet à l'événement de se propager vers le parent (
  `MainFrame`).
- La méthode `event()` de `MainFrame` reçoit alors le même événement et imprime son propre message.

### **Points clés**

- **Accepter un événement** (`event.accept()`) arrête la propagation.
- **Ignorer un événement** (`event.ignore()`) permet à l'événement de remonter vers les widgets parents.
- Ce schéma est essentiel pour les widgets personnalisés qui doivent parfois déléguer la gestion des événements à leur
  parent ou implémenter une surveillance globale des événements.

Cet exemple démontre comment vous pouvez contrôler la propagation des événements dans PySide6 en choisissant d'accepter
ou d'ignorer les événements dans les méthodes de gestion d'événements de vos widgets.

## **Que se passe-t-il si un widget n'a pas de widget parent ?**

Lorsque qu'un événement est ignoré (en utilisant `event.ignore()`) dans un widget sans parent (une fenêtre de niveau
supérieur), l'événement **ne disparaît pas** mais est plutôt propagé vers la **boucle d'événements au niveau de l'
application** pour une éventuelle gestion. Voici le détail :

1. **Pas de propagation parente**
   Puisque le widget n'a pas de parent, il n'y a pas de hiérarchie à travers laquelle "remonter". L'événement sort du
   scope du widget mais reste dans la file d'attente de traitement de l'application.

2. **Gestion au niveau de l'application**
   La boucle d'événements Qt peut encore traiter l'événement par :
    - Les filtres d'événements globaux (`QApplication.instance().installEventFilter()`)
    - Le comportement par défaut de la plateforme (par exemple, les actions du gestionnaire de fenêtres pour les
      événements de fermeture)
    - D'autres gestionnaires au niveau de l'application

3. **Exemple clé : Événements de fermeture de fenêtre**
   Pour une fenêtre de niveau supérieur ignorant `closeEvent` :
   ```python
   class MainWindow(QMainWindow):
       def closeEvent(self, event):
           event.ignore()  # La fenêtre reste ouverte
   ```
   La demande de fermeture est ignorée par la fenêtre mais atteint toujours l'application, qui respecte l'appel à
   `ignore()` en ne terminant pas.

**Implications critiques**

- Les événements ignorés dans les widgets sans parent *peuvent* encore déclencher un comportement au niveau de
  l'application s'ils ne sont pas explicitement bloqués
- Utilisez `event.accept()`/`event.ignore()` stratégiquement même dans les fenêtres de niveau supérieur pour contrôler
  les comportements par défaut de Qt

## **Gestion globale des événements**

L'utilisation de `QApplication.instance().installEventFilter()` vous permet de surveiller ou d'intercepter **tous les
événements de votre application**, pas seulement ceux pour un widget spécifique. Cela est particulièrement utile pour
implémenter des raccourcis globaux, des fonctionnalités d'accessibilité ou une gestion personnalisée des événements qui
devrait s'appliquer partout.

### **Exemple : Bloquer toute entrée clavier vers les champs de texte sauf '0' et '1'**

Supposons que vous souhaitez restreindre chaque champ de texte (`QLineEdit`, `QTextEdit`, etc.) dans votre application
afin que les utilisateurs ne puissent saisir que les chiffres '0' et '1', quel que soit le widget d'entrée sur lequel
ils se concentrent. Au lieu de sous-classer chaque widget d'entrée, vous pouvez installer un seul filtre d'événements
global sur l'objet application.

```python
import sys
from PySide6.QtWidgets import QApplication, QWidget, QVBoxLayout, QLineEdit, QLabel
from PySide6.QtCore import QObject, QEvent


class BinaryInputFilter(QObject):
    def eventFilter(self, obj, event):
        # Filtrer les appuis sur les touches pour tous les widgets
        if event.type() == QEvent.Type.KeyPress:
            # Ne filtrer que les widgets QLineEdit
            if isinstance(obj, QLineEdit):
                text = event.text()
                if text and text not in ('0', '1'):
                    # Bloquer l'événement (ne pas le laisser atteindre le widget)
                    return True
        # Permettre le traitement normal
        return False


app = QApplication(sys.argv)

# Installer le filtre sur l'instance de l'application
binary_filter = BinaryInputFilter()
app.installEventFilter(binary_filter)

window = QWidget()
layout = QVBoxLayout(window)
layout.addWidget(QLabel("Seuls '0' et '1' sont autorisés :"))
layout.addWidget(QLineEdit())
layout.addWidget(QLineEdit())
window.show()

sys.exit(app.exec())
```

#### **Comment ça fonctionne**

- La classe `BinaryInputFilter` vérifie chaque événement d'appui sur une touche pour tous les widgets de l'application.
- Si l'événement concerne un `QLineEdit` et que la touche n'est pas '0' ou '1', l'événement est bloqué (`return True`),
  donc le caractère n'apparaît jamais dans l'entrée.
- Tous les autres événements sont traités normalement (`return False`).

**Cette approche est puissante mais doit être utilisée avec précaution, car elle affecte toute l'application et peut
avoir des implications de performance si elle est trop utilisée**.

!!! info "Filtre d'événements global : `installEventFilter`"
    Cette méthode est directement liée aux situations où vous souhaitez surveiller ou modifier le comportement des
    événements à travers de nombreux widgets, comme les entrées de texte, sans sous-classer chacun d'eux ou vous soucier de
    la propagation des événements entre les widgets parent et enfant. Le filtre d'événements global voit l'événement *avant*
    qu'il n'atteigne un widget quelconque, ce qui le rend idéal pour imposer des règles ou comportements au niveau de
    l'application.
