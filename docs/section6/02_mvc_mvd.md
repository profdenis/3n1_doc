# Architecture de Données Avancée : Le Modèle Proxy dans Qt/PySide6

## 1. Le Problème : Le Piège du Tri Lexicographique

Lorsque vous affichez des données numériques dans un tableau (via `QTableWidget` ou `QTableView`), le comportement par
défaut du système est souvent de traiter les informations comme du **texte** (chaînes de caractères).

**Le problème :** Dans un tri textuel (lexicographique), la valeur `"100"` est considérée comme *inférieure* à `"2"`,
car le premier caractère `"1"` est inférieur à `"2"`. Pour un utilisateur, cela rend le tableau inutilisable pour des
données monétaires ou des quantités.

## 2. La Solution : Le Modèle MVD et le Proxy

Pour résoudre ce problème de manière architecturale et propre, on utilise l'architecture **MVD (Modèle-Vue-Délégué)** en
introduisant un composant intermédiaire : le **`QSortFilterProxyModel`**.

### L'Architecture en 3 Couches :

1. **Le Modèle Source (`QAbstractTableModel`)** : Il détient les données brutes (les types réels : `int`, `float`). Il
   est "aveugle" au tri.
2. **Le Proxy (`QSortFilterProxyModel`)** : Il agit comme une couche de transformation. Il intercepte les demandes de la
   vue et réorganise l'ordre des lignes selon une logique personnalisée.
3. **La Vue (`QTableView`)** : Elle ne communique qu'avec le Proxy. Elle demande simplement : "Quel est le contenu de la
   cellule (x, y) ?" et le Proxy lui répond après avoir fait ses calculs.

---

## 3. Implémentation Complète

```python
import sys
from PySide6.QtWidgets import (QApplication, QMainWindow, QTableView,
                               QVBoxLayout, QWidget, QLabel, QHeaderView)
from PySide6.QtCore import QAbstractTableModel, Qt, QModelIndex, QSortFilterProxyModel


# =================================================================
# 1. LE MODÈLE SOURCE (La Source de Vérité)
# =================================================================
class ProductModel(QAbstractTableModel):
    """
    Modèle qui contient les données brutes.
    Il sépare la donnée pour l'affichage (DisplayRole) 
    et la donnée pour la logique (UserRole).
    """

    def __init__(self, data):
        super().__init__()
        self._data = data
        self._headers = ["Produit", "Prix (€)", "Stock"]

    def rowCount(self, parent=QModelIndex()):
        return len(self._data)

    def columnCount(self, parent=QModelIndex()):
        return len(self._data[0])

    def headerData(self, section, orientation, role):
        if role == Qt.ItemDataRole.DisplayRole and orientation == Qt.Orientation.Horizontal:
            return self._headers[section]
        return None

    def data(self, index, role=Qt.ItemDataRole.DisplayRole):
        if not index.isValid():
            return None

        row = index.row()
        col = index.column()
        value = self._data[row][col]

        # --- Rôle d'affichage (Pour l'œil humain) ---
        if role == Qt.ItemDataRole.DisplayRole:
            if isinstance(value, float):
                return f"{value:.2f}"
            if isinstance(value, int):
                return str(value)
            return str(value)

        # --- Rôle de Donnée Brute (Pour le tri et la logique) ---
        # On utilise UserRole pour envoyer le type réel (float/int) 
        # sans la mise en forme (ex: sans le symbole €)
        if role == Qt.ItemDataRole.UserRole:
            return value

        return None


# =================================================================
# 2. LE PROXY (L'Intelligence de Tri)
# =================================================================
class NumericSortProxyModel(QSortFilterProxyModel):
    """
    Un proxy spécialisé qui redéfinit la règle de comparaison
    pour permettre un tri mathématique.
    """

    def lessThan(self, left, right):
        # On récupère les valeurs réelles stockées dans le modèle source
        # via le UserRole.
        left_data = self.sourceModel().data(left, Qt.ItemDataRole.UserRole)
        right_data = self.sourceModel().data(right, Qt.ItemDataRole.UserRole)

        try:
            # On force la conversion en float pour garantir une comparaison numérique
            return float(left_data) < float(right_data)
        except (ValueError, TypeError):
            # Si la donnée n'est pas un nombre, on repasse au tri textuel standard
            return super().lessThan(left, right)


# =================================================================
# 3. LA VUE (L'Interface Utilisateur)
# =================================================================
class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Architecture MVD : Le Modèle Proxy")
        self.resize(500, 400)

        # Données brutes (mélange de strings, floats, ints)
        raw_data = [
            ["Clavier Mécanique", 89.50, 120],
            ["Souris Gamer", 45.0, 50],
            ["Écran 4K", 350.0, 10],
            ["Tapis de souris", 12.99, 200],
            ["Casque Audio", 120.5, 5],
        ]

        # --- CHAÎNAGE DES COMPOSANTS ---
        # 1. On crée le modèle source
        self.source_model = ProductModel(raw_data)

        # 2. On crée le proxy et on le connecte au modèle source
        self.proxy_model = NumericSortProxyModel()
        self.proxy_model.setSourceModel(self.source_model)

        # 3. On connecte la vue au PROXY (et non au modèle source !)
        self.view = QTableView()
        self.view.setModel(self.proxy_model)
        self.view.setSortingEnabled(True)  # Active le tri au clic sur l'en-tête
        self.view.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)

        # Layout
        layout = QVBoxLayout()
        layout.addWidget(QLabel("Cliquez sur les en-têtes pour trier numériquement :"))
        layout.addWidget(self.view)

        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setStyle("Fusion")
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
```

---

## 4. Analyse Technique Détaillée

### A. Le Modèle et les "Rôles" de données

Un élément de tableau dans Qt n'est pas juste une valeur, c'est un ensemble de données organisées par **Rôles**. Dans
notre exemple, nous utilisons deux rôles essentiels :

1. **`Qt.ItemDataRole.DisplayRole`** : C'est la valeur "esthétique". On y stocke une chaîne de caractères formatée (ex:
   `"89.50"`). C'est ce que l'utilisateur voit à l'écran.
2. **`Qt.ItemDataRole.UserRole`** : C'est la valeur "mathématique". On y stocke la donnée brute (ex: `89.5`). C'est
   cette valeur que nous allons utiliser pour le calcul.

### B. Le Proxy et la méthode `lessThan`

La fonction `lessThan(left, right)` est le cœur de la logique de tri du Proxy.

* **`left` et `right`** : Ce ne sont pas des nombres, ce sont des objets `QModelIndex` (des coordonnées de cellule).
* **`self.sourceModel().data(index, role)`** : Le proxy va chercher la donnée dans le modèle original.
* **La Magie** : En demandant le `UserRole`, le Proxy récupère le `float` et non le `string`. La comparaison
  `10.0 < 2.0` devient alors fausse (correcte mathématiquement), contrairement à la comparaison de chaînes
  `"10.0" < "2.0"`.

### C. Le Flux de données lors d'un clic sur l'en-tête

Voici ce qui se passe réellement quand l'utilisateur clique sur une colonne pour trier :

1. **La Vue** détecte le clic et demande au **Proxy** de trier la colonne.
2. Le **Proxy** appelle sa méthode `lessThan` pour comparer les lignes entre elles.
3. Pour chaque comparaison, le **Proxy** demande au **Modèle Source** la valeur via le `UserRole`.
4. Une fois le nouvel ordre calculé, le **Proxy** notifie la **Vue** qu'elle doit se redessiner.
5. La **Vue** demande les données au **Proxy**, qui les récupère dans le **Modèle** via le `DisplayRole` pour
   l'affichage.

## 5. Résumé pour l'examen

| Composant         | Rôle      | Responsabilité                                      |
|:------------------|:----------|:----------------------------------------------------|
| **Modèle Source** | Données   | Stocker et fournir les données brutes et formatées. |
| **Proxy Model**   | Logique   | Transformer l'ordre des données (Tri/Filtre).       |
| **Vue**           | Interface | Afficher les données résultantes.                   |