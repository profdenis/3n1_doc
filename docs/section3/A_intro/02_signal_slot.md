# **Signaux et Slots**

**Slots** : Récepteurs ou Mécanismes d'événements.

## **1. Qu'est-ce qu'un signal et un slot ?**

- **Signal** : Événement déclenché par l'utilisateur ou le système (ex: clic sur un bouton).
- **Slot** : Fonction appelée en réponse à un signal.
- **Traduction française** :
    - *Signal* → "Événement" ou "Signal" (terme technique accepté).
    - *Slot* → "Récepteur", "Méthode de traitement" ou "Fonction de rappel".

## **2. Exemple : Bouton qui modifie un texte aléatoire**

```python
import sys
import random
from PySide6.QtWidgets import (
    QApplication,
    QMainWindow,
    QPushButton,
    QLabel,
    QVBoxLayout,
    QWidget
)
from PySide6.QtCore import Qt


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Générateur de nombres")
        self.label = QLabel("Appuyez sur le bouton !", alignment=Qt.AlignmentFlag.AlignCenter)
        self.button = QPushButton("Générer un nombre")
        self.button.clicked.connect(self.update_label)

        # Création d'un conteneur central avec layout
        central_widget = QWidget()
        self.setCentralWidget(central_widget)  # Définir le widget central

        # Configuration du layout vertical
        layout = QVBoxLayout(central_widget)
        layout.addWidget(self.label)  # Ajoute le label en haut
        layout.addWidget(self.button)  # Ajoute le bouton en dessous

    def update_label(self):
        random_number = random.randint(0, 100)
        self.label.setText(f"Nombre généré : {random_number}")


app = QApplication(sys.argv)
window = MainWindow()
window.resize(300, 200)  # Taille de la fenêtre
window.show()
sys.exit(app.exec())
```

## **3. Explication du code**

1. `self.button.clicked.connect(self.update_label)` :
    - Le signal `clicked` du bouton est connecté au slot `update_label`.
2. `QVBoxLayout` :
    - Organise les widgets verticalement (label en haut, bouton en dessous).
3. `QWidget` comme conteneur central :
    - `central_widget` sert de support pour le layout.
    - `setCentralWidget(central_widget)` définit ce widget comme contenu principal.
4. Ajout des widgets au layout :
    - `layout.addWidget(self.label)`
    - `layout.addWidget(self.button)`
5. `def update_label(self):` :
    - Slot personnalisé qui génère un nombre aléatoire et met à jour le texte du label.
6. `self.label.setText(...)` :
    - Modifie dynamiquement le contenu du `QLabel`.

!!! info "Pourquoi utiliser un layout ?"
    Gestion automatique du redimensionnement : 

    - Les widgets s'adaptent si la fenêtre est agrandie.    
    - Code plus lisible 
    - Pas besoin de gérer manuellement les positions (move()).

## **4. Points clés**

- Les signaux/slots permettent une **programmation événementielle** (réactive).
- Un même signal peut être connecté à plusieurs slots (ex: un bouton qui déclenche deux actions).

---

### **Exercice pratique**

Modifiez l'exemple pour :

1. Ajouter un deuxième bouton qui incrémente un compteur.
2. Afficher le compteur dans un nouveau `QLabel`.
