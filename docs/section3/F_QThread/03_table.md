# Exemple : Chargeur CSV

## Nouveaux concepts dans cet exemple

### 1. **Entrée/Sortie de fichiers dans les threads d'arrière-plan**

```python
# Lecture du fichier CSV dans le thread worker - PAS dans le thread principal
with open(self.file_path, 'r', newline='', encoding='utf-8') as file:
    csv_reader = csv.reader(file)
    headers = next(csv_reader)  # Lire la ligne d'en-tête
    for row in csv_reader:  # Lire les lignes de données
        data_rows.append(row)
```

**Point clé :** Les opérations sur fichiers peuvent être lentes, surtout pour les gros fichiers, donc elles doivent être
dans des threads d'arrière-plan.

### 2. **Calcul de progression pour des tâches réelles**

```python
# Premier passage : compter les lignes pour le calcul de progression
total_rows = sum(1 for row in csv_reader) - 1

# Deuxième passage : mettre à jour la progression pendant la lecture
progress = 30 + int((row_index / total_rows) * 60)
self.progress_update.emit(min(progress, 90))
```

**Point clé :** Les barres de progression réelles nécessitent de connaître le travail total à l'avance.

### 3. **Transfert de données complexes entre threads**

```python
# Le signal transporte à la fois les en-têtes et les données
data_loaded = Signal(list, list)

# Émettre une structure de données complexe
self.data_loaded.emit(headers, data_rows)
```

**Concept important :** Les signaux peuvent transporter plusieurs paramètres et types de données complexes.

### 4. **Remplissage de QTableWidget**

```python
def populate_table(self, headers, data_rows):
    # Définir les dimensions du tableau
    self.table.setColumnCount(len(headers))
    self.table.setRowCount(len(data_rows))

    # Définir les en-têtes
    self.table.setHorizontalHeaderLabels(headers)

    # Remplir chaque cellule
    for row_index, row_data in enumerate(data_rows):
        for col_index, cell_data in enumerate(row_data):
            item = QTableWidgetItem(str(cell_data))
            self.table.setItem(row_index, col_index, item)
```

**Nouveau concept GUI :** Comment remplir programmatiquement des tableaux avec des données dynamiques.

### 5. **Intégration de la boîte de dialogue de fichier**

```python
file_path, _ = QFileDialog.getOpenFileName(
    self,
    "Sélectionner un fichier CSV",
    "",
    "Fichiers CSV (*.csv);;Tous les fichiers (*)"
)
```

**Compétence pratique :** Laisser l'utilisateur sélectionner des fichiers au lieu de coder des chemins en dur.

### 6. **Gestion des erreurs dans les threads d'arrière-plan**

```python
try:
# Opérations sur fichiers
except FileNotFoundError:
    self.error_occurred.emit(f"Fichier introuvable : {self.file_path}")
except PermissionError:
    self.error_occurred.emit(f"Permission refusée : {self.file_path}")
except UnicodeDecodeError:
    self.error_occurred.emit("Impossible de décoder le fichier...")
```

**Modèle important :** Gérer les erreurs dans le thread worker et les signaler via des signaux.

### 7. **Gestion de l'état de l'UI pour les opérations sur fichiers**

```python
def load_csv_file(self, file_path):
    # Désactiver les boutons pendant le chargement
    self.load_button.setEnabled(False)
    self.clear_button.setEnabled(False)

    # Afficher la barre de progression
    self.progress_bar.setVisible(True)

    # Effacer les données existantes
    self.table.setRowCount(0)
```

**Principe UX :** Toujours donner un retour visuel et empêcher les actions utilisateur conflictuelles.

## Ce que cet exemple nous apprend

1. **Gestion de fichiers réels** - Les fichiers CSV sont courants dans les applications professionnelles
2. **Amélioration progressive** - Commencer avec le threading basique, ajouter l'E/S de fichiers, la progression, la
   gestion des erreurs
3. **Visualisation de données** - Comment afficher des données structurées dans des tableaux
4. **Expérience utilisateur** - Boîtes de dialogue de fichier, barres de progression, messages d'erreur
5. **Modèles pratiques** - Lecture de fichiers en deux passes (compter puis traiter)

## Exécution de l'exemple

L'application inclut une fonction `create_sample_csv()` qui génère des données de test, donc nous pouvons l'exécuter
immédiatement sans avoir besoin de nos propres fichiers CSV.

**Fonctionnalités à démontrer :**

- Cliquer sur "Charger fichier CSV" pour voir la boîte de dialogue
- Observer la barre de progression pendant le chargement
- Voir les données s'afficher dans le tableau
- Essayer de cliquer sur des boutons pendant le chargement (ils sont désactivés)
- Utiliser le bouton "Effacer le tableau"
- Le tableau supporte le tri en cliquant sur les en-têtes de colonne

## Code complet

```python
import sys
import csv
import time
from PySide6.QtCore import QThread, Signal
from PySide6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout,
                               QHBoxLayout, QPushButton, QLabel, QProgressBar,
                               QTableWidget, QTableWidgetItem, QFileDialog,
                               QMessageBox, QHeaderView)


class CSVLoaderThread(QThread):
    """Thread d'arrière-plan pour charger les fichiers CSV"""

    # Signaux pour la communication avec le thread principal
    progress_update = Signal(int)  # Pourcentage de progression
    status_update = Signal(str)  # Messages de statut
    data_loaded = Signal(list, list)  # En-têtes et lignes de données
    error_occurred = Signal(str)  # Messages d'erreur

    def __init__(self, file_path):
        super().__init__()
        self.file_path = file_path

    def run(self):
        """Charger le fichier CSV dans le thread d'arrière-plan"""
        try:
            self.status_update.emit("Ouverture du fichier...")
            self.progress_update.emit(10)

            # Simuler un temps de traitement
            time.sleep(0.5)

            # Premier passage : compter les lignes totales pour le calcul de progression
            self.status_update.emit("Analyse de la structure du fichier...")
            with open(self.file_path, 'r', newline='', encoding='utf-8') as file:
                csv_reader = csv.reader(file)
                total_rows = sum(1 for row in csv_reader) - 1  # Soustraire la ligne d'en-tête

            self.progress_update.emit(20)
            time.sleep(0.2)

            # Deuxième passage : lire réellement les données
            self.status_update.emit("Lecture des données CSV...")
            headers = []
            data_rows = []

            with open(self.file_path, 'r', newline='', encoding='utf-8') as file:
                csv_reader = csv.reader(file)

                # Lire la ligne d'en-tête
                headers = next(csv_reader)
                self.progress_update.emit(30)

                # Lire les lignes de données avec mises à jour de progression
                for row_index, row in enumerate(csv_reader):
                    data_rows.append(row)

                    # Mettre à jour la progression toutes les 100 lignes environ
                    if row_index % max(1, total_rows // 10) == 0:
                        progress = 30 + int((row_index / total_rows) * 60)
                        self.progress_update.emit(min(progress, 90))
                        self.status_update.emit(f"Chargement de la ligne {row_index + 1} sur {total_rows}")

                    # Petite pause pour rendre la progression visible (à supprimer dans les apps réelles)
                    if row_index % 50 == 0:
                        time.sleep(0.01)

            self.progress_update.emit(95)
            self.status_update.emit("Finalisation des données...")
            time.sleep(0.2)

            # Envoyer les données chargées au thread principal
            self.data_loaded.emit(headers, data_rows)
            self.progress_update.emit(100)
            self.status_update.emit(f"Chargement réussi de {len(data_rows)} lignes")

        except FileNotFoundError:
            self.error_occurred.emit(f"Fichier introuvable : {self.file_path}")
        except PermissionError:
            self.error_occurred.emit(f"Permission refusée : {self.file_path}")
        except UnicodeDecodeError:
            self.error_occurred.emit(
                "Impossible de décoder le fichier. Veuillez vérifier qu'il s'agit d'un CSV valide avec encodage UTF-8.")
        except Exception as e:
            self.error_occurred.emit(f"Erreur lors du chargement du CSV : {str(e)}")


class CSVLoaderApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.loader_thread = None
        self.init_ui()

    def init_ui(self):
        # Créer le widget central et le layout principal
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout(central_widget)

        # Panneau de contrôle
        control_layout = QHBoxLayout()

        self.load_button = QPushButton("Charger fichier CSV")
        self.load_button.clicked.connect(self.select_and_load_file)

        self.clear_button = QPushButton("Effacer le tableau")
        self.clear_button.clicked.connect(self.clear_table)
        self.clear_button.setEnabled(False)

        control_layout.addWidget(self.load_button)
        control_layout.addWidget(self.clear_button)
        control_layout.addStretch()  # Pousser les boutons à gauche

        main_layout.addLayout(control_layout)

        # Section statut et progression
        self.status_label = QLabel("Prêt à charger un fichier CSV")
        main_layout.addWidget(self.status_label)

        self.progress_bar = QProgressBar()
        self.progress_bar.setVisible(False)  # Masquer initialement
        main_layout.addWidget(self.progress_bar)

        # Tableau de données
        self.table = QTableWidget()
        self.table.setSortingEnabled(True)  # Activer le tri des colonnes

        # Faire étirer les en-têtes du tableau pour remplir la largeur
        header = self.table.horizontalHeader()
        header.setSectionResizeMode(QHeaderView.ResizeMode.Stretch)

        main_layout.addWidget(self.table)

        # Étiquette d'information sur le fichier
        self.info_label = QLabel("")
        self.info_label.setStyleSheet("color: gray; font-size: 10px;")
        main_layout.addWidget(self.info_label)

        # Paramètres de la fenêtre
        self.setWindowTitle("Chargeur de fichiers CSV - Démonstration de threading d'arrière-plan")
        self.setGeometry(200, 200, 800, 600)

    def select_and_load_file(self):
        """Ouvrir la boîte de dialogue et charger le fichier CSV sélectionné"""
        file_path, _ = QFileDialog.getOpenFileName(
            self,
            "Sélectionner un fichier CSV",
            "",
            "Fichiers CSV (*.csv);;Tous les fichiers (*)"
        )

        if file_path:
            self.load_csv_file(file_path)

    def load_csv_file(self, file_path):
        """Démarrer le chargement du fichier CSV dans un thread d'arrière-plan"""
        # Mettre à jour l'état de l'UI
        self.load_button.setEnabled(False)
        self.clear_button.setEnabled(False)
        self.progress_bar.setVisible(True)
        self.progress_bar.setValue(0)

        # Effacer les données existantes du tableau
        self.table.setRowCount(0)
        self.table.setColumnCount(0)

        # Créer et démarrer le thread de chargement
        self.loader_thread = CSVLoaderThread(file_path)

        # Connecter les signaux
        self.loader_thread.progress_update.connect(self.update_progress)
        self.loader_thread.status_update.connect(self.update_status)
        self.loader_thread.data_loaded.connect(self.populate_table)
        self.loader_thread.error_occurred.connect(self.handle_error)
        self.loader_thread.finished.connect(self.loading_finished)

        # Démarrer le chargement en arrière-plan
        self.loader_thread.start()

        # Mettre à jour l'étiquette d'information
        self.info_label.setText(f"Chargement : {file_path}")

    def update_progress(self, value):
        """Mettre à jour la barre de progression"""
        self.progress_bar.setValue(value)

    def update_status(self, message):
        """Mettre à jour l'étiquette de statut"""
        self.status_label.setText(message)

    def populate_table(self, headers, data_rows):
        """Remplir le tableau avec les données chargées (s'exécute dans le thread principal)"""
        # Définir les dimensions du tableau
        self.table.setColumnCount(len(headers))
        self.table.setRowCount(len(data_rows))

        # Définir les en-têtes
        self.table.setHorizontalHeaderLabels(headers)

        # Remplir les données
        for row_index, row_data in enumerate(data_rows):
            for col_index, cell_data in enumerate(row_data):
                # S'assurer de ne pas dépasser le nombre de colonnes
                if col_index < len(headers):
                    item = QTableWidgetItem(str(cell_data))
                    self.table.setItem(row_index, col_index, item)

        # Mettre à jour l'information
        self.info_label.setText(
            f"Chargé {len(data_rows)} lignes × {len(headers)} colonnes"
        )

        self.clear_button.setEnabled(True)

    def handle_error(self, error_message):
        """Gérer les erreurs de chargement"""
        QMessageBox.critical(self, "Erreur lors du chargement du CSV", error_message)
        self.status_label.setText("Une erreur s'est produite lors du chargement du fichier")
        self.info_label.setText("Aucun fichier chargé")

    def loading_finished(self):
        """Nettoyer après la fin du chargement"""
        # Réinitialiser l'état de l'UI
        self.load_button.setEnabled(True)
        self.progress_bar.setVisible(False)

        # Nettoyer le thread
        self.loader_thread = None

    def clear_table(self):
        """Effacer les données du tableau"""
        self.table.setRowCount(0)
        self.table.setColumnCount(0)
        self.clear_button.setEnabled(False)
        self.status_label.setText("Tableau effacé")
        self.info_label.setText("Aucun fichier chargé")


def create_sample_csv():
    """Créer un fichier CSV d'exemple pour les tests"""
    sample_data = [
        ["Nom", "Âge", "Ville", "Service", "Salaire"],
        ["Alice Johnson", "28", "New York", "Ingénierie", "75000"],
        ["Bob Smith", "34", "San Francisco", "Marketing", "68000"],
        ["Carol Davis", "31", "Chicago", "Ventes", "62000"],
        ["David Wilson", "29", "Boston", "Ingénierie", "78000"],
        ["Eva Brown", "26", "Seattle", "Design", "65000"],
        ["Frank Miller", "35", "Los Angeles", "Management", "95000"],
        ["Grace Lee", "30", "Denver", "Ingénierie", "72000"],
        ["Henry Taylor", "32", "Miami", "Ventes", "58000"],
        ["Ivy Chen", "27", "Portland", "Marketing", "64000"],
        ["Jack Robinson", "33", "Austin", "Ingénierie", "76000"]
    ]

    with open("sample_employees.csv", "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerows(sample_data)

    print("Créé sample_employees.csv pour les tests")


if __name__ == "__main__":
    app = QApplication(sys.argv)

    # Créer un fichier CSV d'exemple pour les tests
    create_sample_csv()

    window = CSVLoaderApp()
    window.show()

    sys.exit(app.exec())
```