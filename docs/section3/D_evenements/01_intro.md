# **1. Vue d'ensemble des événements système**

Pour gérer les événements système comme les interactions avec la souris et la fermeture de fenêtre dans PySide6, vous
interceptez les événements en sous-classant les widgets et en remplaçant leurs méthodes de gestion d'événements. Voici
un exemple d'approche structurée :

## **Exemple : Position de la souris**

```python
from PySide6.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QLabel
from PySide6.QtGui import QCursor
import sys


class CustomButton(QPushButton):
    def __init__(self, label, parent=None):
        super().__init__(label, parent)
        self.position_label = None

    def mousePressEvent(self, event):
        if self.position_label:
            pos = event.position()
            self.position_label.setText(f"Méthode de sous-classe : {pos.x():.0f}, {pos.y():.0f}")
        super().mousePressEvent(event)


class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Position de la souris sur QPushButton")
        self.resize(300, 200)

        layout = QVBoxLayout()

        # Label pour afficher la position
        self.position_label = QLabel("Cliquez sur un bouton pour voir la position")
        layout.addWidget(self.position_label)

        # Bouton utilisant la méthode QCursor
        self.cursor_button = QPushButton("Position via curseur")
        self.cursor_button.clicked.connect(self.show_cursor_position)
        layout.addWidget(self.cursor_button)

        # Bouton utilisant la méthode de sous-classe
        self.subclass_button = CustomButton("Méthode de sous-classe")
        self.subclass_button.position_label = self.position_label
        layout.addWidget(self.subclass_button)

        self.setLayout(layout)

    def show_cursor_position(self):
        pos = self.cursor_button.mapFromGlobal(QCursor.pos())
        self.position_label.setText(f"Méthode curseur : {pos.x()}, {pos.y()}")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
```

## **Mécanisme de base de gestion des événements**

### **1. Sous-classement des widgets**

Créez des classes de widgets personnalisées qui héritent des widgets PySide6 (par exemple, `QPushButton`, `QMainWindow`)
et remplacez les gestionnaires d'événements spécifiques :

```python
class CustomButton(QPushButton):
    def mousePressEvent(self, event):  # Remplacement du clic de souris
        pos = event.position()
        print(f"Cliqué à : {pos.x()}, {pos.y()}")
        super().mousePressEvent(event)  # Conservation du comportement par défaut
```

### **2. Accès aux détails des événements**

Utilisez l'objet événement en paramètre pour obtenir les détails de l'interaction :

- Position de la souris via `event.position()`
- Bouton de la souris via `event.button() == Qt.MouseButton.LeftButton`
- Modificateurs clavier via `event.modifiers() & Qt.KeyboardModifier.ShiftModifier`

### **3. Événements de fermeture de fenêtre**

Remplacez `closeEvent` dans votre classe de fenêtre principale pour intercepter les tentatives de fermeture :

```python
class MainWindow(QMainWindow):
    def closeEvent(self, event):
        print("Fermeture de la fenêtre tentée")
        event.ignore()  # Optionnel : empêcher la fermeture
        # OU event.accept() pour permettre la fermeture
```

## **Modèles d'implémentation clés**

### **Gestion des événements de souris**

L'exemple ci-dessus démontre deux approches efficaces :

1. **Méthode de sous-classe** (Recommandée)
    - Remplacez directement `mousePressEvent` dans les widgets personnalisés
    - Fournit un contrôle précis sur les éléments cibles
    - Montré dans votre classe `CustomButton`

2. **Méthode de position du curseur**
    - Utilise `QCursor.pos()` pour les coordonnées globales
    - Moins précise pour les interactions spécifiques aux widgets

### **Propagation des événements**

Lorsque les widgets enfants bloquent les événements (fréquent avec les champs de texte, voir exemple dans la section
suivante) :

- Utilisez `installEventFilter()` pour intercepter les événements des widgets enfants
- Définissez `setMouseTracking(True)` pour la détection continue du mouvement de la souris
- Assurez-vous que les politiques de focus sont correctement configurées

## **Bonnes pratiques**

1. **Chaînage à la classe parente**
   Appelez toujours `super().eventHandler(event)` sauf si vous bloquez explicitement le comportement par défaut

2. **Acceptation des événements**
   Utilisez `event.accept()`/`event.ignore()` pour contrôler la propagation des événements

3. **Gestion de plusieurs boutons**
   Gérez différents boutons de souris en utilisant les constantes du namespace Qt :
   ```python
   if event.button() == Qt.MouseButton.RightButton:
       handle_right_click()
   ```

Ces modèles vous permettent de créer des interfaces utilisateur réactives et bien structurées dans PySide6.