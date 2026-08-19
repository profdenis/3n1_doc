# **Widgets**

## **1. Types de Widgets dans Qt**

Les widgets sont les éléments graphiques de base (boutons, zones de texte, etc.).

### **A. `QLabel` (Étiquette)**

- **Description** : Affiche du texte ou une image (non modifiable par l'utilisateur).
- **Exemple** :
  ```python
  label = QLabel("Bonjour !")
  label.setAlignment(Qt.AlignmentFlag.AlignCenter)  # Centrage
  ```

### **B. `QPushButton` (Bouton)**

- **Description** : Bouton cliquable pour déclencher des actions.
- **Exemple** :
  ```python
  button = QPushButton("Cliquez-moi")
  button.clicked.connect(lambda: print("Bouton cliqué !"))
  ```

### **C. `QLineEdit` (Champ de texte)**

- **Description** : Zone pour saisir du texte en une ligne.
- **Exemple** :
  ```python
  line_edit = QLineEdit()
  line_edit.setPlaceholderText("Entrez votre nom")
  ```

### **D. `QTextEdit` (Zone de texte multiline)**

- **Description** : Zone pour du texte sur plusieurs lignes (avec mise en forme possible).
- **Exemple** :
  ```python
  text_edit = QTextEdit()
  text_edit.setPlainText("Texte par défaut")
  ```

### **E. `QComboBox` (Liste déroulante)**

- **Description** : Menu déroulant pour sélectionner une option.
- **Exemple** :
  ```python
  combo = QComboBox()
  combo.addItems(["Option 1", "Option 2", "Option 3"])
  ```

### **F. `QCheckBox` (Case à cocher)**

- **Description** : Case pour activer/désactiver une option.
- **Exemple** :
  ```python
  checkbox = QCheckBox("Accepter les conditions")
  checkbox.stateChanged.connect(lambda: print("État:", checkbox.isChecked()))
  ```

### **G. `QRadioButton` (Bouton radio)**

- **Description** : Bouton pour un choix exclusif dans un groupe.
- **Exemple** :
  ```python
  radio1 = QRadioButton("Choix 1")
  radio2 = QRadioButton("Choix 2")
  # Pour un groupe, utilisez QButtonGroup
  ```

### **H. `QSlider` (Curseur)**

- **Description** : Curseur pour sélectionner une valeur dans une plage.
- **Exemple** :
  ```python
  slider = QSlider(Qt.Orientation.Horizontal)
  slider.setRange(0, 100)  # Valeurs de 0 à 100
  ```

### **I. `QProgressBar` (Barre de progression)**

- **Description** : Affiche une barre de progression.
- **Exemple** :
  ```python
  progress = QProgressBar()
  progress.setRange(0, 100)
  progress.setValue(50)  # 50% complété
  ```

### **J. `QTableWidget` (Tableau)**

- **Description** : Tableau modifiable avec lignes/colonnes.
- **Exemple** :
  ```python
  table = QTableWidget(3, 2)  # 3 lignes, 2 colonnes
  table.setItem(0, 0, QTableWidgetItem("Ligne 1, Colonne 1"))
  ```

### **K. `QListWidget` (Liste)**

- **Description** : Liste d'éléments sélectionnables.
- **Exemple** :
  ```python
  list_widget = QListWidget()
  list_widget.addItems(["Élément 1", "Élément 2"])
  ```

---

## **2. Tableau Récapitulatif**

| Widget         | Description                      | Exemples d'utilisation typiques              |
|----------------|----------------------------------|----------------------------------------------|
| `QLabel`       | Texte/image non modifiable       | Titres, descriptions, icônes                 |
| `QPushButton`  | Bouton cliquable                 | Actions (OK, Annuler), boutons de navigation |
| `QLineEdit`    | Champ de texte en une ligne      | Saisie rapide (nom, email)                   |
| `QTextEdit`    | Zone de texte multiline          | Éditeur de code, zone de commentaires        |
| `QComboBox`    | Liste déroulante                 | Sélection d'options (pays, catégories)       |
| `QCheckBox`    | Case à cocher                    | Options binaires (activer/désactiver)        |
| `QRadioButton` | Bouton radio                     | Choix exclusif (genre, niveau de difficulté) |
| `QSlider`      | Curseur pour valeurs numériques  | Volume, luminosité, filtres                  |
| `QProgressBar` | Barre de progression             | Téléchargements, traitements en cours        |
| `QTableWidget` | Tableau modifiable               | Données tabulaires (feuilles de calcul)      |
| `QListWidget`  | Liste d'éléments sélectionnables | Playlists, listes de tâches                  |

---

## **3. Exemple Combiné**

```python
# Formulaire simple avec plusieurs widgets
form_layout = QFormLayout()
form_layout.addRow(QLabel("Nom:"), QLineEdit())
form_layout.addRow(QLabel("Âge:"), QSpinBox())  # Champ numérique
form_layout.addRow(QCheckBox("Accepter"))
```

---

### **Remarques**

- Les widgets peuvent être **personnalisés** (couleurs, polices, etc.).
- Pour des interfaces complexes, combinez plusieurs widgets dans un layout.
