# **Les agencements (Layouts)**

## **1. Types de Layouts dans Qt**

Les layouts permettent d'organiser les widgets de manière dynamique (adaptative au redimensionnement).

### **A. `QVBoxLayout` (Vertical)**

- **Description** : Dispose les widgets verticalement (les uns en dessous des autres).
- **Exemple** :
  ```python
  layout = QVBoxLayout()
  layout.addWidget(QLabel("Label 1"))
  layout.addWidget(QPushButton("Bouton 1"))
  layout.addStretch()  # Espace élastique en bas
  ```

### **B. `QHBoxLayout` (Horizontal)**

- **Description** : Dispose les widgets horizontalement (les uns à côté des autres).
- **Exemple** :
  ```python
  layout = QHBoxLayout()
  layout.addWidget(QPushButton("Gauche"))
  layout.addWidget(QLabel("Milieu"))
  layout.addWidget(QPushButton("Droite"))
  ```

### **C. `QGridLayout` (Grille)**

- **Description** : Dispose les widgets dans une grille (lignes/colonnes).
- **Exemple** :
  ```python
  grid = QGridLayout()
  grid.addWidget(QLabel("Ligne 1"), 0, 0)  # (ligne, colonne)
  grid.addWidget(QPushButton("OK"), 1, 1)
  ```

### **D. `QFormLayout` (Formulaire)**

- **Description** : Dispose les widgets comme un formulaire (étiquette + champ).
- **Exemple** :
  ```python
  form = QFormLayout()
  form.addRow(QLabel("Nom:"), QLineEdit())
  form.addRow(QLabel("Âge:"), QSpinBox())
  ```

### **E. `QStackedLayout` (Piles)**

- **Description** : Affiche un seul widget à la fois (comme des onglets).
- **Exemple** :
  ```python
  stacked = QStackedLayout()
  stacked.addWidget(QLabel("Page 1"))
  stacked.addWidget(QPushButton("Page 2"))
  stacked.setCurrentIndex(0)  # Affiche la première page
  ```

### **F. `QSplitter` (Séparateurs)**

- **Description** : Permet de redimensionner manuellement les zones.
- **Exemple** :
  ```python
  splitter = QSplitter()
  splitter.addWidget(QLabel("Gauche"))
  splitter.addWidget(QTextEdit("Droite"))
  ```

---

## **2. Tableau Récapitulatif**

| Layout           | Description                         | Exemples d'utilisation typiques             |
|------------------|-------------------------------------|---------------------------------------------|
| `QVBoxLayout`    | Widgets empilés verticalement       | Menus, listes, formulaires simples          |
| `QHBoxLayout`    | Widgets alignés horizontalement     | Barres d'outils, en-têtes de tableau        |
| `QGridLayout`    | Grille (lignes/colonnes)            | Tableaux, grilles de boutons                |
| `QFormLayout`    | Formulaire (étiquette + champ)      | Paramètres, configurations                  |
| `QStackedLayout` | Piles (un widget visible à la fois) | Onglets, vues dynamiques                    |
| `QSplitter`      | Zones redimensionnables             | Editeurs de code, visualisateurs de données |

---

## **3. Exemple Combiné**

Pour combiner plusieurs layouts :

```python
# Layout principal (vertical)
main_layout = QVBoxLayout()
main_layout.addWidget(QLabel("Titre"))

# Sous-layout horizontal pour les boutons
button_layout = QHBoxLayout()
button_layout.addWidget(QPushButton("OK"))
button_layout.addWidget(QPushButton("Annuler"))

main_layout.addLayout(button_layout)  # Ajoute le sous-layout au principal
```

---

### **Remarques**

- Les layouts peuvent être **imbriqués** (ex: un `QVBoxLayout` contenant un `QHBoxLayout`).
- Utilisez `addStretch()` pour ajouter de l'espace élastique.
- Pour des interfaces complexes, combinez plusieurs types de layouts.
