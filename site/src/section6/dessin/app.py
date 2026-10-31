"""
Application principale PySide6 de démonstration :
Illustre l'utilisation conjointe des patrons Factory Method et Abstract Factory
par le code client (MainWindow) sans aucun couplage aux formats concrets.
"""

from __future__ import annotations
import sys

from PySide6.QtWidgets import (
    QApplication,
    QMainWindow,
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QPushButton,
    QLabel,
    QStatusBar,
    QGroupBox,
)

try:
    from .documents import Document
    from .editeurs import EditeurDocument, EditeurCanvas, EditeurAscii
except (ImportError, ValueError):
    from documents import Document
    from editeurs import EditeurDocument, EditeurCanvas, EditeurAscii


class MainWindow(QMainWindow):
    """
    Fenêtre principale de l'application de dessin.
    Démontre comment le code client interagit UNIQUEMENT avec :
    - EditeurDocument (Factory Method)
    - FabriqueFormes (Abstract Factory via l'éditeur actif)
    - Document (Produit générique)
    SANS aucun 'if / elif' sur le type concret de document ou de forme !
    """

    def __init__(self):
        super().__init__()
        self.setWindowTitle("Démo Design Patterns : Fabrique & Fabrique Abstraite")
        self.resize(750, 520)

        # Éditeurs disponibles (les deux créateurs concrets)
        self.editeur_canvas = EditeurCanvas()
        self.editeur_ascii = EditeurAscii()

        # Éditeur actuellement actif (référence polymorphique EditeurDocument)
        self.editeur_actif: EditeurDocument = self.editeur_canvas

        self._setup_ui()

        # Création du document initial via la Factory Method
        self.action_nouveau_canvas()

    def _setup_ui(self) -> None:
        widget_central = QWidget()
        self.setCentralWidget(widget_central)
        layout_principal = QVBoxLayout(widget_central)

        # --- Section 1 : Contrôles de création de document (Factory Method) ---
        groupe_editeur = QGroupBox("1. Patron Fabrique (Factory Method) - Sélection de l'Éditeur")
        layout_editeur = QHBoxLayout(groupe_editeur)

        btn_canvas = QPushButton("🎨 Éditeur Canvas (Nouveau Document)")
        btn_canvas.setStyleSheet("font-weight: bold; padding: 6px;")
        btn_canvas.clicked.connect(self.action_nouveau_canvas)
        layout_editeur.addWidget(btn_canvas)

        btn_ascii = QPushButton("💻 Éditeur ASCII Art (Nouveau Document)")
        btn_ascii.setStyleSheet("font-weight: bold; padding: 6px;")
        btn_ascii.clicked.connect(self.action_nouveau_ascii)
        layout_editeur.addWidget(btn_ascii)

        layout_principal.addWidget(groupe_editeur)

        # --- Section 2 : Barre d'outils de dessin (Abstract Factory) ---
        groupe_formes = QGroupBox("2. Patron Fabrique Abstraite (Abstract Factory) - Outils de dessin")
        layout_formes = QHBoxLayout(groupe_formes)

        btn_rect = QPushButton("➕ Ajouter Rectangle")
        btn_rect.clicked.connect(self.action_ajouter_rectangle)
        layout_formes.addWidget(btn_rect)

        btn_cercle = QPushButton("➕ Ajouter Cercle")
        btn_cercle.clicked.connect(self.action_ajouter_cercle)
        layout_formes.addWidget(btn_cercle)

        btn_ligne = QPushButton("➕ Ajouter Ligne")
        btn_ligne.clicked.connect(self.action_ajouter_ligne)
        layout_formes.addWidget(btn_ligne)

        btn_effacer = QPushButton("🗑️ Effacer")
        btn_effacer.clicked.connect(self.action_effacer)
        layout_formes.addWidget(btn_effacer)

        layout_principal.addWidget(groupe_formes)

        # --- Section 3 : Zone d'affichage du document ---
        self.label_info = QLabel("Document actif : Aucun")
        self.label_info.setStyleSheet("font-size: 13px; font-weight: bold; color: #333333; margin-top: 4px;")
        layout_principal.addWidget(self.label_info)

        self.layout_conteneur_doc = QVBoxLayout()
        layout_principal.addLayout(self.layout_conteneur_doc, stretch=1)

        # Barre d'état
        self.setStatusBar(QStatusBar(self))

    # --- Actions du Menu / Boutons ---

    def action_nouveau_canvas(self) -> None:
        """Active l'éditeur Canvas et crée un nouveau CanvasDoc."""
        self.editeur_actif = self.editeur_canvas
        # Appel polymorphique à nouveau_document() via Factory Method
        doc = self.editeur_actif.nouveau_document()
        self._mettre_a_jour_vue_document(doc)
        self.statusBar().showMessage("Nouveau document créé via EditeurCanvas.creer_document() -> CanvasDoc")

    def action_nouveau_ascii(self) -> None:
        """Active l'éditeur ASCII et crée un nouveau AsciiDoc."""
        self.editeur_actif = self.editeur_ascii
        # Appel polymorphique à nouveau_document() via Factory Method
        doc = self.editeur_actif.nouveau_document()
        self._mettre_a_jour_vue_document(doc)
        self.statusBar().showMessage("Nouveau document créé via EditeurAscii.creer_document() -> AsciiDoc")

    def _mettre_a_jour_vue_document(self, doc: Document) -> None:
        """Remplace le composant visuel affiché par celui du document actif."""
        self.label_info.setText(f"Éditeur actif : {self.editeur_actif.nom_format} | Titre : {doc.titre}")

        # Nettoie l'ancien widget
        while self.layout_conteneur_doc.count():
            item = self.layout_conteneur_doc.takeAt(0)
            if item.widget():
                item.widget().setParent(None)

        # Insère le widget polymorphique fourni par le document
        self.layout_conteneur_doc.addWidget(doc.obtenir_widget())

    def action_ajouter_rectangle(self) -> None:
        """
        DÉMONSTRATION CLÉ :
        Création d'un rectangle via la Fabrique Abstraite SANS se soucier
        du format de document (Canvas ou ASCII).
        """
        doc = self.editeur_actif.document_courant
        if doc is None:
            return

        # Appel polymorphique à la fabrique abstraite
        forme = self.editeur_actif.fabrique_formes.creer_rectangle()
        doc.ajouter_forme(forme)
        self.statusBar().showMessage(
            f"Forme créée : {forme.__class__.__name__} via {self.editeur_actif.fabrique_formes.__class__.__name__}"
        )

    def action_ajouter_cercle(self) -> None:
        """Création d'un cercle via la Fabrique Abstraite."""
        doc = self.editeur_actif.document_courant
        if doc is None:
            return

        forme = self.editeur_actif.fabrique_formes.creer_cercle()
        doc.ajouter_forme(forme)
        self.statusBar().showMessage(
            f"Forme créée : {forme.__class__.__name__} via {self.editeur_actif.fabrique_formes.__class__.__name__}"
        )

    def action_ajouter_ligne(self) -> None:
        """Création d'une ligne via la Fabrique Abstraite."""
        doc = self.editeur_actif.document_courant
        if doc is None:
            return

        forme = self.editeur_actif.fabrique_formes.creer_ligne()
        doc.ajouter_forme(forme)
        self.statusBar().showMessage(
            f"Forme créée : {forme.__class__.__name__} via {self.editeur_actif.fabrique_formes.__class__.__name__}"
        )

    def action_effacer(self) -> None:
        """Efface le document actif."""
        doc = self.editeur_actif.document_courant
        if doc:
            doc.effacer()
            self.statusBar().showMessage("Document effacé.")


# ==============================================================================
# POINT D'ENTRÉE PRINCIPAL
# ==============================================================================

if __name__ == "__main__":
    app = QApplication(sys.argv)
    fenetre = MainWindow()
    fenetre.show()
    sys.exit(app.exec())
