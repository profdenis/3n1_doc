import sys
from PySide6.QtWidgets import (QApplication, QMainWindow, QTableView,
                               QVBoxLayout, QWidget, QLabel, QHeaderView)
from PySide6.QtCore import QAbstractTableModel, Qt, QModelIndex, QSortFilterProxyModel


# --- 1. LE MODÈLE (La source de vérité, très simple) ---
class ProductModel(QAbstractTableModel):
    def __init__(self, data):
        super().__init__()
        self._data = data
        self._headers = ["Produit", "Prix (€)", "Stock"]

    def rowCount(self, parent=QModelIndex()):
        return len(self._data)

    def columnCount(self, parent=QModelIndex()):
        return len(self._data[0])

    def headerData(self, section, orientation, role=Qt.ItemDataRole.DisplayRole):
        if role == Qt.ItemDataRole.DisplayRole and orientation == Qt.Orientation.Horizontal:
            return self._headers[section]
        return None

    def data(self, index, role=Qt.ItemDataRole.DisplayRole):
        if not index.isValid():
            return None

        row = index.row()
        col = index.column()
        value = self._data[row][col]

        # On ne gère que l'affichage ici
        if role == Qt.ItemDataRole.DisplayRole:
            if isinstance(value, float): return f"{value:.2f}"
            if isinstance(value, int): return str(value)
            return str(value)

        # On fournit la donnée brute pour le tri (via le Proxy)
        if role == Qt.ItemDataRole.UserRole:
            return value

        return None


# --- 2. LE PROXY (Le "Contrôleur" de tri) ---
class NumericSortProxyModel(QSortFilterProxyModel):
    """
    Un proxy qui sait comment comparer numériquement les données
    en demandant la valeur brute (UserRole) au modèle source.
    """

    def lessThan(self, left, right):
        # On récupère les valeurs réelles (int/float) du modèle source
        left_data = self.sourceModel().data(left, Qt.ItemDataRole.UserRole)
        right_data = self.sourceModel().data(right, Qt.ItemDataRole.UserRole)

        try:
            # On tente de comparer en convertissant en float pour la sécurité
            return float(left_data) < float(right_data)
        except (ValueError, TypeError):
            # Si ce n'est pas numérique, on laisse le comportement par défaut (string)
            return super().lessThan(left, right)


# --- 3. LA VUE (L'interface) ---
class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Architecture MVD : Proxy Model")
        self.resize(500, 400)

        # Données brutes
        raw_data = [
            ["Clavier Mécanique", 89.50, 120],
            ["Souris Gamer", 45.0, 50],
            ["Écran 4K", 350.0, 10],
            ["Tapis de souris", 12.99, 200],
            ["Casque Audio", 120.5, 5],
        ]

        # Normalement, on irait chercher les données depuis une base de données ou un fichier externe
        # Pour simplifier l'exemple, on utilise des données fictives "hardcodées"
        # Étape 1 : Le Modèle (Data)
        self.source_model = ProductModel(raw_data)

        # Étape 2 : Le Proxy (Logique de tri)
        self.proxy_model = NumericSortProxyModel()
        self.proxy_model.setSourceModel(self.source_model)

        # Étape 3 : La Vue (Affichage) - On connecte la vue au PROXY
        self.view = QTableView()
        self.view.setModel(self.proxy_model)
        self.view.setSortingEnabled(True)
        self.view.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)

        layout = QVBoxLayout()
        layout.addWidget(QLabel("Tri numérique via QSortFilterProxyModel :"))
        layout.addWidget(self.view)

        central_widget = QWidget()
        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
