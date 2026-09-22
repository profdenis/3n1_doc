# **Exercice 3 : Ardoise de dessin interactive (Mini Paint)**

Cet exercice vous invite à construire une application graphique interactive avec **PySide6** permettant de dessiner
à main levée sur une surface dédiée (*canevas*).
Vous y pratiquerez la création d'un widget personnalisé (`QWidget`), l'interception fine des événements de la souris
(`mousePressEvent`, `mouseMoveEvent`, `mouseReleaseEvent`), le rendu graphique 2D (`QPainter`, `QPen`, `QPixmap`),
la synchronisation de contrôles (`QSlider` et `QSpinBox`), l'utilisation de boîtes de dialogue standards
(`QColorDialog`, `QFileDialog`),
l'ajout d'une barre d'outils avec actions groupées (`QToolBar`, `QActionGroup`), et la protection de session avec
`closeEvent`.

---

## **Partie 1 : Canevas de base et premier tracé**

**Objectif :** Créer un widget de dessin personnalisé réagissant aux mouvements de la souris.

- Créez une classe personnalisée `CanvasWidget` qui hérite de `QWidget`.
    - Dans son constructeur, fixez sa taille à `600x400` pixels.
    - Instanciez un objet `QPixmap` de même dimension et remplissez-le de blanc (`Qt.GlobalColor.white`). Ce `QPixmap`
      servira de mémoire tampon (*buffer*) sur laquelle les traits seront dessinés.
    - Définissez les attributs de tracé par défaut : couleur noire (`QColor("black")`), épaisseur de 3 pixels, et une
      variable `last_point = None`.
- Surchargez `paintEvent(self, event)` :
    - Instanciez un `QPainter` sur le widget (`self`) et dessinez le `QPixmap` à la position `(0, 0)`.
- Surchargez les méthodes de gestion d'événements de la souris :
    - `mousePressEvent(self, event)` : si le bouton gauche est pressé (`Qt.MouseButton.LeftButton`), enregistrez le
      point initial (`event.position().toPoint()`).
    - `mouseMoveEvent(self, event)` : si le bouton gauche est maintenu et que `last_point` existe :
        - Ouvrez un `QPainter` sur le `QPixmap`.
        - Configurez un `QPen` avec la couleur et l'épaisseur voulues (avec des extrémités et jointures arrondies :
          `Qt.PenCapStyle.RoundCap`, `Qt.PenJoinStyle.RoundJoin`).
        - Tracez une ligne entre `last_point` et le point courant avec `painter.drawLine()`.
        - Fermez le painter (`painter.end()`), mettez à jour `last_point`, et appelez `self.update()` pour redessiner le
          widget.
    - `mouseReleaseEvent(self, event)` : lorsque le bouton gauche est relâché, réinitialisez `last_point` à `None`.
- Créez la fenêtre principale `QMainWindow` et définissez une instance de `CanvasWidget` comme widget central.

---

## **Partie 2 : Réglage de l'épaisseur du trait et synchronisation des contrôles**

**Objectif :** Ajouter des contrôles pour moduler l'épaisseur du trait et synchroniser deux widgets entre eux.

- Dans `CanvasWidget`, ajoutez une méthode `set_pen_width(self, width)` pour modifier l'épaisseur du tracé.
- Dans la fenêtre principale :
    - Placez au-dessus du canevas une barre de réglage horizontale (`QHBoxLayout`).
    - Ajoutez un libellé `QLabel("Épaisseur :")`.
    - Ajoutez un curseur horizontal `QSlider` (plage de 1 à 30, valeur initiale 3).
    - Ajoutez un champ numérique `QSpinBox` (plage de 1 à 30, valeur initiale 3).
- Synchronisez bidirectionnellement le slider et la spinbox :
    - La modification du slider met à jour la spinbox (`slider.valueChanged.connect(spinbox.setValue)`).
    - La modification de la spinbox met à jour le slider (`spinbox.valueChanged.connect(slider.setValue)`).
- Connectez la valeur du slider à la méthode `set_pen_width` du canevas.

---

## **Partie 3 : Choix des couleurs et dialogue standard**

**Objectif :** Permettre le choix d'une couleur arbitraire grâce à `QColorDialog`.

- Dans `CanvasWidget`, ajoutez une méthode `set_pen_color(self, color)` permettant de changer la couleur active du
  pinceau.
- Dans la barre de contrôle de la fenêtre principale :
    - Ajoutez un bouton `QPushButton` étiqueté « Couleur... ».
    - Ajoutez un petit `QLabel` d'environ `24x24` pixels servant de pastille visuelle de la couleur sélectionnée (en
      configurant son style avec `setStyleSheet`).
- Connectez le bouton à une méthode qui ouvre la boîte de dialogue standard `QColorDialog.getColor()`.
- Si l'utilisateur valide une couleur (`color.isValid()`) :
    - Transmettez-la au canevas via `set_pen_color(color)`.
    - Mettez à jour la couleur d'arrière-plan de la pastille visuelle pour refléter le nouveau choix.

---

## **Partie 4 : Barre d'outils et modes de dessin (Pinceau, Gomme, Effacer tout)**

**Objectif :** Intégrer une `QToolBar` avec sélection exclusive d'outils et action d'effacement.

- Dans `CanvasWidget` :
    - Ajoutez un attribut `mode` pouvant valoir `"pen"` (pinceau) ou `"eraser"` (gomme).
    - Ajoutez une méthode `set_mode(self, mode)`.
    - Dans `mouseMoveEvent`, adaptez la couleur du tracé : si le mode est `"eraser"`, dessinez en blanc
      (`Qt.GlobalColor.white`), sinon avec la couleur choisie.
    - Ajoutez une méthode `clear_canvas(self)` qui remplit à nouveau le pixmap de blanc et déclenche `self.update()`.
- Dans `QMainWindow` :
    - Ajoutez une barre d'outils avec `self.addToolBar("Outils")`.
    - Créez un groupe d'actions exclusif `QActionGroup` contenant :
        - Une action basculable (*checkable*) « Pinceau », cochée par défaut.
        - Une action basculable « Gomme ».
    - Ajoutez un séparateur puis une action simple « Effacer tout » connectée à `canvas.clear_canvas()`.
    - Lorsque l'utilisateur sélectionne une nouvelle couleur depuis le bouton de dialogue, faites repasser
      automatiquement l'outil actif sur « Pinceau ».

---

## **Partie 5 : Enregistrement de l'image, barre d'état et confirmation de fermeture**

**Objectif :** Finaliser l'application avec l'exportation de fichier (`QFileDialog`), des informations en direct dans la
`QStatusBar` et la détection des modifications avant fermeture (`closeEvent`).

- **Suivi des modifications et du curseur :**
    - Activez le suivi de la souris sans clic sur le canevas : `self.setMouseTracking(True)`.
    - Dans `CanvasWidget`, déclarez deux signaux personnalisés :
        - `drawing_changed = Signal()` : émis à chaque fois qu'un trait est dessiné ou que le canevas est effacé.
        - `mouse_moved = Signal(QPoint)` : émis dans `mouseMoveEvent` pour transmettre la position courante du pointeur.
    - Dans `MainWindow`, conservez un booléen `is_modified = False` passant à `True` lors de la réception de
      `drawing_changed`.
- **Barre d'état (`QStatusBar`) :**
    - Initialisez la barre d'état et affichez-y en continu l'outil sélectionné, l'épaisseur courante et les coordonnées
      de la souris sous la forme : `"Outil : Pinceau | Épaisseur : 3px | Position : (X, Y)"`.
- **Menu Fichier & Enregistrement d'image :**
    - Ajoutez un menu « Fichier » avec les actions :
        - « Nouveau dessin » (`Ctrl+N`) : réinitialise le canevas après confirmation si des modifications non
          enregistrées existent.
        - « Enregistrer sous... » (`Ctrl+S`) : ouvre `QFileDialog.getSaveFileName` avec les filtres pour images PNG et
          JPEG.
        - « Quitter » (`Ctrl+Q`).
    - Lors de l'enregistrement, appelez `self.canvas.pixmap.save(file_path)` et repassez `is_modified` à `False`.
- **Interception de fermeture (`closeEvent`) :**
    - Surchargez `closeEvent(self, event)`.
    - Si `is_modified` est vrai, affichez un message de confirmation avec `QMessageBox.question` avertissant
      l'utilisateur que des modifications non enregistrées existent.
    - Appelez `event.accept()` pour quitter ou `event.ignore()` pour annuler la fermeture.

---

**Défi bonus :**

- Ajoutez une action « Ouvrir une image... » permettant de charger une image existante du disque sur le canevas avec
  `pixmap.load()`.
- Implémentez un mode « Rectangle » ou « Cercle » en dessinant une forme temporaire dans `paintEvent` pendant le
  déplacement, puis en la fixant sur le pixmap lors du `mouseReleaseEvent`.

---

**Instructions :**

- Pour chaque partie, commencez à partir du fichier de l'étape précédente et complétez les méthodes.
- Testez votre dessin après chaque étape pour vérifier la fluidité des tracés et la bonne synchronisation des widgets.
- Conservez vos différentes versions dans des fichiers séparés : `dessin1.py`, `dessin2.py`, `dessin3.py`, `dessin4.py`,
  `dessin5.py`.

---

??? info "Exemple de solution pour la Partie 1"

    ```python title="dessin1.py"
    import sys
    from PySide6.QtWidgets import QApplication, QMainWindow, QWidget
    from PySide6.QtCore import Qt, QPoint
    from PySide6.QtGui import QPainter, QPen, QColor, QPixmap


    class CanvasWidget(QWidget):
        """Widget de dessin personnalisé gérant les événements de la souris."""
        def __init__(self, parent=None):
            super().__init__(parent)
            self.setFixedSize(600, 400)

            # Création d'un pixmap blanc sur lequel dessiner
            self.pixmap = QPixmap(self.size())
            self.pixmap.fill(Qt.GlobalColor.white)

            # Propriétés du tracé
            self.pen_color = QColor("black")
            self.pen_width = 3
            self.last_point = None

        def paintEvent(self, event):
            """Dessine le pixmap sur la surface du widget."""
            painter = QPainter(self)
            painter.drawPixmap(0, 0, self.pixmap)

        def mousePressEvent(self, event):
            """Enregistre le point de départ lors du clic gauche."""
            if event.button() == Qt.MouseButton.LeftButton:
                self.last_point = event.position().toPoint()

        def mouseMoveEvent(self, event):
            """Trace une ligne continue tant que le bouton gauche est maintenu."""
            if (event.buttons() & Qt.MouseButton.LeftButton) and self.last_point is not None:
                painter = QPainter(self.pixmap)
                pen = QPen(
                    self.pen_color,
                    self.pen_width,
                    Qt.PenStyle.SolidLine,
                    Qt.PenCapStyle.RoundCap,
                    Qt.PenJoinStyle.RoundJoin
                )
                painter.setPen(pen)

                current_point = event.position().toPoint()
                painter.drawLine(self.last_point, current_point)
                painter.end()

                self.last_point = current_point
                self.update()  # Demande le rafraîchissement du widget

        def mouseReleaseEvent(self, event):
            """Réinitialise le point de tracé lorsque le clic est relâché."""
            if event.button() == Qt.MouseButton.LeftButton:
                self.last_point = None


    class MainWindow(QMainWindow):
        def __init__(self):
            super().__init__()
            self.setWindowTitle("Ardoise de dessin")

            self.canvas = CanvasWidget()
            self.setCentralWidget(self.canvas)


    if __name__ == "__main__":
        app = QApplication(sys.argv)
        window = MainWindow()
        window.show()
        sys.exit(app.exec())
    ```

??? info "Exemple de solution pour la Partie 2"

    ```python title="dessin2.py"
    import sys
    from PySide6.QtWidgets import (QApplication, QMainWindow, QWidget,
                                   QVBoxLayout, QHBoxLayout, QLabel,
                                   QSlider, QSpinBox)
    from PySide6.QtCore import Qt, QPoint
    from PySide6.QtGui import QPainter, QPen, QColor, QPixmap


    class CanvasWidget(QWidget):
        """Widget de dessin personnalisé gérant les événements de la souris."""
        def __init__(self, parent=None):
            super().__init__(parent)
            self.setFixedSize(600, 400)

            # Création d'un pixmap blanc sur lequel dessiner
            self.pixmap = QPixmap(self.size())
            self.pixmap.fill(Qt.GlobalColor.white)

            # Propriétés du tracé
            self.pen_color = QColor("black")
            self.pen_width = 3
            self.last_point = None

        def set_pen_width(self, width):
            """Modifie l'épaisseur du pinceau."""
            self.pen_width = width

        def paintEvent(self, event):
            """Dessine le pixmap sur la surface du widget."""
            painter = QPainter(self)
            painter.drawPixmap(0, 0, self.pixmap)

        def mousePressEvent(self, event):
            """Enregistre le point de départ lors du clic gauche."""
            if event.button() == Qt.MouseButton.LeftButton:
                self.last_point = event.position().toPoint()

        def mouseMoveEvent(self, event):
            """Trace une ligne continue tant que le bouton gauche est maintenu."""
            if (event.buttons() & Qt.MouseButton.LeftButton) and self.last_point is not None:
                painter = QPainter(self.pixmap)
                pen = QPen(
                    self.pen_color,
                    self.pen_width,
                    Qt.PenStyle.SolidLine,
                    Qt.PenCapStyle.RoundCap,
                    Qt.PenJoinStyle.RoundJoin
                )
                painter.setPen(pen)

                current_point = event.position().toPoint()
                painter.drawLine(self.last_point, current_point)
                painter.end()

                self.last_point = current_point
                self.update()

        def mouseReleaseEvent(self, event):
            """Réinitialise le point de tracé lorsque le clic est relâché."""
            if event.button() == Qt.MouseButton.LeftButton:
                self.last_point = None


    class MainWindow(QMainWindow):
        def __init__(self):
            super().__init__()
            self.setWindowTitle("Ardoise de dessin")

            # Widget central et layout principal
            central_widget = QWidget()
            layout = QVBoxLayout()

            # Canevas de dessin
            self.canvas = CanvasWidget()

            # Barre de contrôle de l'épaisseur
            control_layout = QHBoxLayout()
            control_layout.addWidget(QLabel("Épaisseur :"))

            self.width_slider = QSlider(Qt.Orientation.Horizontal)
            self.width_slider.setRange(1, 30)
            self.width_slider.setValue(3)

            self.width_spinbox = QSpinBox()
            self.width_spinbox.setRange(1, 30)
            self.width_spinbox.setValue(3)

            # Synchronisation entre le Slider et le SpinBox
            self.width_slider.valueChanged.connect(self.width_spinbox.setValue)
            self.width_spinbox.valueChanged.connect(self.width_slider.setValue)

            # Connexion avec le canevas
            self.width_slider.valueChanged.connect(self.canvas.set_pen_width)

            control_layout.addWidget(self.width_slider)
            control_layout.addWidget(self.width_spinbox)
            control_layout.addStretch()

            layout.addLayout(control_layout)
            layout.addWidget(self.canvas)

            central_widget.setLayout(layout)
            self.setCentralWidget(central_widget)


    if __name__ == "__main__":
        app = QApplication(sys.argv)
        window = MainWindow()
        window.show()
        sys.exit(app.exec())
    ```

??? info "Exemple de solution pour la Partie 3"

    ```python title="dessin3.py"
    import sys
    from PySide6.QtWidgets import (QApplication, QMainWindow, QWidget,
                                   QVBoxLayout, QHBoxLayout, QLabel,
                                   QSlider, QSpinBox, QPushButton, QColorDialog)
    from PySide6.QtCore import Qt, QPoint
    from PySide6.QtGui import QPainter, QPen, QColor, QPixmap


    class CanvasWidget(QWidget):
        """Widget de dessin personnalisé gérant les événements de la souris."""
        def __init__(self, parent=None):
            super().__init__(parent)
            self.setFixedSize(600, 400)

            # Création d'un pixmap blanc sur lequel dessiner
            self.pixmap = QPixmap(self.size())
            self.pixmap.fill(Qt.GlobalColor.white)

            # Propriétés du tracé
            self.pen_color = QColor("black")
            self.pen_width = 3
            self.last_point = None

        def set_pen_width(self, width):
            """Modifie l'épaisseur du pinceau."""
            self.pen_width = width

        def set_pen_color(self, color):
            """Modifie la couleur du pinceau."""
            self.pen_color = color

        def paintEvent(self, event):
            """Dessine le pixmap sur la surface du widget."""
            painter = QPainter(self)
            painter.drawPixmap(0, 0, self.pixmap)

        def mousePressEvent(self, event):
            """Enregistre le point de départ lors du clic gauche."""
            if event.button() == Qt.MouseButton.LeftButton:
                self.last_point = event.position().toPoint()

        def mouseMoveEvent(self, event):
            """Trace une ligne continue tant que le bouton gauche est maintenu."""
            if (event.buttons() & Qt.MouseButton.LeftButton) and self.last_point is not None:
                painter = QPainter(self.pixmap)
                pen = QPen(
                    self.pen_color,
                    self.pen_width,
                    Qt.PenStyle.SolidLine,
                    Qt.PenCapStyle.RoundCap,
                    Qt.PenJoinStyle.RoundJoin
                )
                painter.setPen(pen)

                current_point = event.position().toPoint()
                painter.drawLine(self.last_point, current_point)
                painter.end()

                self.last_point = current_point
                self.update()

        def mouseReleaseEvent(self, event):
            """Réinitialise le point de tracé lorsque le clic est relâché."""
            if event.button() == Qt.MouseButton.LeftButton:
                self.last_point = None


    class MainWindow(QMainWindow):
        def __init__(self):
            super().__init__()
            self.setWindowTitle("Ardoise de dessin")

            # Widget central et layout principal
            central_widget = QWidget()
            layout = QVBoxLayout()

            # Canevas de dessin
            self.canvas = CanvasWidget()

            # Barre de contrôle (épaisseur et couleur)
            control_layout = QHBoxLayout()
            control_layout.addWidget(QLabel("Épaisseur :"))

            self.width_slider = QSlider(Qt.Orientation.Horizontal)
            self.width_slider.setRange(1, 30)
            self.width_slider.setValue(3)

            self.width_spinbox = QSpinBox()
            self.width_spinbox.setRange(1, 30)
            self.width_spinbox.setValue(3)

            # Synchronisation slider / spinbox
            self.width_slider.valueChanged.connect(self.width_spinbox.setValue)
            self.width_spinbox.valueChanged.connect(self.width_slider.setValue)
            self.width_slider.valueChanged.connect(self.canvas.set_pen_width)

            control_layout.addWidget(self.width_slider)
            control_layout.addWidget(self.width_spinbox)

            # Contrôles de sélection de couleur
            control_layout.addSpacing(15)
            self.color_button = QPushButton("Couleur...")
            self.color_button.clicked.connect(self.choose_color)
            control_layout.addWidget(self.color_button)

            # Aperçu de la couleur sélectionnée
            self.color_sample = QLabel()
            self.color_sample.setFixedSize(24, 24)
            self.color_sample.setStyleSheet(
                f"background-color: {self.canvas.pen_color.name()}; border: 1px solid #333;"
            )
            control_layout.addWidget(self.color_sample)

            control_layout.addStretch()

            layout.addLayout(control_layout)
            layout.addWidget(self.canvas)

            central_widget.setLayout(layout)
            self.setCentralWidget(central_widget)

        def choose_color(self):
            """Ouvre une boîte de dialogue standard pour sélectionner une couleur."""
            color = QColorDialog.getColor(self.canvas.pen_color, self, "Choisir la couleur du pinceau")
            if color.isValid():
                self.canvas.set_pen_color(color)
                self.color_sample.setStyleSheet(
                    f"background-color: {color.name()}; border: 1px solid #333;"
                )


    if __name__ == "__main__":
        app = QApplication(sys.argv)
        window = MainWindow()
        window.show()
        sys.exit(app.exec())
    ```

??? info "Exemple de solution pour la Partie 4"

    ```python title="dessin4.py"
    import sys
    from PySide6.QtWidgets import (QApplication, QMainWindow, QWidget,
                                   QVBoxLayout, QHBoxLayout, QLabel,
                                   QSlider, QSpinBox, QPushButton, QColorDialog)
    from PySide6.QtCore import Qt, QPoint
    from PySide6.QtGui import (QPainter, QPen, QColor, QPixmap,
                               QAction, QActionGroup)


    class CanvasWidget(QWidget):
        """Widget de dessin personnalisé gérant les événements de la souris."""
        def __init__(self, parent=None):
            super().__init__(parent)
            self.setFixedSize(600, 400)

            # Création d'un pixmap blanc sur lequel dessiner
            self.pixmap = QPixmap(self.size())
            self.pixmap.fill(Qt.GlobalColor.white)

            # Propriétés du tracé
            self.pen_color = QColor("black")
            self.pen_width = 3
            self.mode = "pen"  # "pen" ou "eraser"
            self.last_point = None

        def set_pen_width(self, width):
            """Modifie l'épaisseur du pinceau."""
            self.pen_width = width

        def set_pen_color(self, color):
            """Modifie la couleur du pinceau."""
            self.pen_color = color

        def set_mode(self, mode):
            """Définit le mode d'outil ('pen' ou 'eraser')."""
            self.mode = mode

        def clear_canvas(self):
            """Efface tout le contenu du canevas en le repeignant en blanc."""
            self.pixmap.fill(Qt.GlobalColor.white)
            self.update()

        def paintEvent(self, event):
            """Dessine le pixmap sur la surface du widget."""
            painter = QPainter(self)
            painter.drawPixmap(0, 0, self.pixmap)

        def mousePressEvent(self, event):
            """Enregistre le point de départ lors du clic gauche."""
            if event.button() == Qt.MouseButton.LeftButton:
                self.last_point = event.position().toPoint()

        def mouseMoveEvent(self, event):
            """Trace une ligne continue tant que le bouton gauche est maintenu."""
            if (event.buttons() & Qt.MouseButton.LeftButton) and self.last_point is not None:
                painter = QPainter(self.pixmap)

                # Couleur selon le mode actif
                draw_color = Qt.GlobalColor.white if self.mode == "eraser" else self.pen_color
                pen = QPen(
                    draw_color,
                    self.pen_width,
                    Qt.PenStyle.SolidLine,
                    Qt.PenCapStyle.RoundCap,
                    Qt.PenJoinStyle.RoundJoin
                )
                painter.setPen(pen)

                current_point = event.position().toPoint()
                painter.drawLine(self.last_point, current_point)
                painter.end()

                self.last_point = current_point
                self.update()

        def mouseReleaseEvent(self, event):
            """Réinitialise le point de tracé lorsque le clic est relâché."""
            if event.button() == Qt.MouseButton.LeftButton:
                self.last_point = None


    class MainWindow(QMainWindow):
        def __init__(self):
            super().__init__()
            self.setWindowTitle("Ardoise de dessin")

            # Canevas de dessin
            self.canvas = CanvasWidget()

            # Barre d'outils
            self.create_tool_bar()

            # Widget central et layout principal
            central_widget = QWidget()
            layout = QVBoxLayout()

            # Barre de contrôle (épaisseur et couleur)
            control_layout = QHBoxLayout()
            control_layout.addWidget(QLabel("Épaisseur :"))

            self.width_slider = QSlider(Qt.Orientation.Horizontal)
            self.width_slider.setRange(1, 30)
            self.width_slider.setValue(3)

            self.width_spinbox = QSpinBox()
            self.width_spinbox.setRange(1, 30)
            self.width_spinbox.setValue(3)

            # Synchronisation slider / spinbox
            self.width_slider.valueChanged.connect(self.width_spinbox.setValue)
            self.width_spinbox.valueChanged.connect(self.width_slider.setValue)
            self.width_slider.valueChanged.connect(self.canvas.set_pen_width)

            control_layout.addWidget(self.width_slider)
            control_layout.addWidget(self.width_spinbox)

            # Contrôles de sélection de couleur
            control_layout.addSpacing(15)
            self.color_button = QPushButton("Couleur...")
            self.color_button.clicked.connect(self.choose_color)
            control_layout.addWidget(self.color_button)

            # Aperçu de la couleur sélectionnée
            self.color_sample = QLabel()
            self.color_sample.setFixedSize(24, 24)
            self.color_sample.setStyleSheet(
                f"background-color: {self.canvas.pen_color.name()}; border: 1px solid #333;"
            )
            control_layout.addWidget(self.color_sample)

            control_layout.addStretch()

            layout.addLayout(control_layout)
            layout.addWidget(self.canvas)

            central_widget.setLayout(layout)
            self.setCentralWidget(central_widget)

        def create_tool_bar(self):
            """Crée la barre d'outils avec les modes Pinceau, Gomme et Effacer."""
            toolbar = self.addToolBar("Outils")

            tool_group = QActionGroup(self)

            self.pen_action = QAction("Pinceau", self)
            self.pen_action.setCheckable(True)
            self.pen_action.setChecked(True)
            self.pen_action.triggered.connect(lambda: self.canvas.set_mode("pen"))
            tool_group.addAction(self.pen_action)
            toolbar.addAction(self.pen_action)

            self.eraser_action = QAction("Gomme", self)
            self.eraser_action.setCheckable(True)
            self.eraser_action.triggered.connect(lambda: self.canvas.set_mode("eraser"))
            tool_group.addAction(self.eraser_action)
            toolbar.addAction(self.eraser_action)

            toolbar.addSeparator()

            clear_action = QAction("Effacer tout", self)
            clear_action.triggered.connect(self.canvas.clear_canvas)
            toolbar.addAction(clear_action)

        def choose_color(self):
            """Ouvre une boîte de dialogue standard pour sélectionner une couleur."""
            color = QColorDialog.getColor(self.canvas.pen_color, self, "Choisir la couleur du pinceau")
            if color.isValid():
                self.canvas.set_pen_color(color)
                self.color_sample.setStyleSheet(
                    f"background-color: {color.name()}; border: 1px solid #333;"
                )
                # Revenir automatiquement au mode pinceau si on était en gomme
                self.pen_action.setChecked(True)
                self.canvas.set_mode("pen")


    if __name__ == "__main__":
        app = QApplication(sys.argv)
        window = MainWindow()
        window.show()
        sys.exit(app.exec())
    ```

??? info "Exemple de solution pour la Partie 5"

    ```python title="dessin5.py"
    import sys
    from PySide6.QtWidgets import (QApplication, QMainWindow, QWidget,
                                   QVBoxLayout, QHBoxLayout, QLabel,
                                   QSlider, QSpinBox, QPushButton, QColorDialog,
                                   QFileDialog, QMessageBox)
    from PySide6.QtCore import Qt, QPoint, Signal
    from PySide6.QtGui import (QPainter, QPen, QColor, QPixmap,
                               QAction, QActionGroup, QKeySequence)


    class CanvasWidget(QWidget):
        """Widget de dessin personnalisé gérant les événements de la souris."""
        drawing_changed = Signal()
        mouse_moved = Signal(QPoint)

        def __init__(self, parent=None):
            super().__init__(parent)
            self.setFixedSize(600, 400)
            self.setMouseTracking(True)  # Suivre les mouvements même sans clic

            # Création d'un pixmap blanc sur lequel dessiner
            self.pixmap = QPixmap(self.size())
            self.pixmap.fill(Qt.GlobalColor.white)

            # Propriétés du tracé
            self.pen_color = QColor("black")
            self.pen_width = 3
            self.mode = "pen"  # "pen" ou "eraser"
            self.last_point = None

        def set_pen_width(self, width):
            """Modifie l'épaisseur du pinceau."""
            self.pen_width = width

        def set_pen_color(self, color):
            """Modifie la couleur du pinceau."""
            self.pen_color = color

        def set_mode(self, mode):
            """Définit le mode d'outil ('pen' ou 'eraser')."""
            self.mode = mode

        def clear_canvas(self):
            """Efface tout le contenu du canevas en le repeignant en blanc."""
            self.pixmap.fill(Qt.GlobalColor.white)
            self.update()
            self.drawing_changed.emit()

        def paintEvent(self, event):
            """Dessine le pixmap sur la surface du widget."""
            painter = QPainter(self)
            painter.drawPixmap(0, 0, self.pixmap)

        def mousePressEvent(self, event):
            """Enregistre le point de départ lors du clic gauche."""
            if event.button() == Qt.MouseButton.LeftButton:
                self.last_point = event.position().toPoint()

        def mouseMoveEvent(self, event):
            """Met à jour la position du curseur et trace si le bouton gauche est enfoncé."""
            current_point = event.position().toPoint()
            self.mouse_moved.emit(current_point)

            if (event.buttons() & Qt.MouseButton.LeftButton) and self.last_point is not None:
                painter = QPainter(self.pixmap)

                # Couleur selon le mode actif
                draw_color = Qt.GlobalColor.white if self.mode == "eraser" else self.pen_color
                pen = QPen(
                    draw_color,
                    self.pen_width,
                    Qt.PenStyle.SolidLine,
                    Qt.PenCapStyle.RoundCap,
                    Qt.PenJoinStyle.RoundJoin
                )
                painter.setPen(pen)

                painter.drawLine(self.last_point, current_point)
                painter.end()

                self.last_point = current_point
                self.update()
                self.drawing_changed.emit()

        def mouseReleaseEvent(self, event):
            """Réinitialise le point de tracé lorsque le clic est relâché."""
            if event.button() == Qt.MouseButton.LeftButton:
                self.last_point = None


    class MainWindow(QMainWindow):
        def __init__(self):
            super().__init__()
            self.setWindowTitle("Ardoise de dessin")
            self.is_modified = False

            # Canevas de dessin
            self.canvas = CanvasWidget()
            self.canvas.drawing_changed.connect(self.on_drawing_changed)
            self.canvas.mouse_moved.connect(self.on_mouse_moved)

            # Menus, barre d'outils et barre d'état
            self.create_menu_bar()
            self.create_tool_bar()
            self.statusBar()

            # Widget central et layout principal
            central_widget = QWidget()
            layout = QVBoxLayout()

            # Barre de contrôle (épaisseur et couleur)
            control_layout = QHBoxLayout()
            control_layout.addWidget(QLabel("Épaisseur :"))

            self.width_slider = QSlider(Qt.Orientation.Horizontal)
            self.width_slider.setRange(1, 30)
            self.width_slider.setValue(3)

            self.width_spinbox = QSpinBox()
            self.width_spinbox.setRange(1, 30)
            self.width_spinbox.setValue(3)

            # Synchronisation slider / spinbox
            self.width_slider.valueChanged.connect(self.width_spinbox.setValue)
            self.width_spinbox.valueChanged.connect(self.width_slider.setValue)
            self.width_slider.valueChanged.connect(self.canvas.set_pen_width)
            self.width_slider.valueChanged.connect(self.update_status_message)

            control_layout.addWidget(self.width_slider)
            control_layout.addWidget(self.width_spinbox)

            # Contrôles de sélection de couleur
            control_layout.addSpacing(15)
            self.color_button = QPushButton("Couleur...")
            self.color_button.clicked.connect(self.choose_color)
            control_layout.addWidget(self.color_button)

            # Aperçu de la couleur sélectionnée
            self.color_sample = QLabel()
            self.color_sample.setFixedSize(24, 24)
            self.color_sample.setStyleSheet(
                f"background-color: {self.canvas.pen_color.name()}; border: 1px solid #333;"
            )
            control_layout.addWidget(self.color_sample)

            control_layout.addStretch()

            layout.addLayout(control_layout)
            layout.addWidget(self.canvas)

            central_widget.setLayout(layout)
            self.setCentralWidget(central_widget)

            self.cursor_pos = QPoint(0, 0)
            self.update_status_message()

        def create_menu_bar(self):
            """Crée la barre de menus avec les actions Fichier."""
            menubar = self.menuBar()
            file_menu = menubar.addMenu("Fichier")

            new_action = QAction("Nouveau dessin", self)
            new_action.setShortcut(QKeySequence.StandardKey.New)
            new_action.triggered.connect(self.new_drawing)
            file_menu.addAction(new_action)

            save_action = QAction("Enregistrer sous...", self)
            save_action.setShortcut(QKeySequence.StandardKey.Save)
            save_action.triggered.connect(self.save_image)
            file_menu.addAction(save_action)

            file_menu.addSeparator()

            quit_action = QAction("Quitter", self)
            quit_action.setShortcut(QKeySequence.StandardKey.Quit)
            quit_action.triggered.connect(self.close)
            file_menu.addAction(quit_action)

        def create_tool_bar(self):
            """Crée la barre d'outils avec les modes Pinceau, Gomme et Effacer."""
            toolbar = self.addToolBar("Outils")

            tool_group = QActionGroup(self)

            self.pen_action = QAction("Pinceau", self)
            self.pen_action.setCheckable(True)
            self.pen_action.setChecked(True)
            self.pen_action.triggered.connect(lambda: self.set_tool_mode("pen"))
            tool_group.addAction(self.pen_action)
            toolbar.addAction(self.pen_action)

            self.eraser_action = QAction("Gomme", self)
            self.eraser_action.setCheckable(True)
            self.eraser_action.triggered.connect(lambda: self.set_tool_mode("eraser"))
            tool_group.addAction(self.eraser_action)
            toolbar.addAction(self.eraser_action)

            toolbar.addSeparator()

            clear_action = QAction("Effacer tout", self)
            clear_action.triggered.connect(self.canvas.clear_canvas)
            toolbar.addAction(clear_action)

        def set_tool_mode(self, mode):
            """Modifie le mode de tracé et met à jour l'affichage."""
            self.canvas.set_mode(mode)
            self.update_status_message()

        def choose_color(self):
            """Ouvre une boîte de dialogue standard pour sélectionner une couleur."""
            color = QColorDialog.getColor(self.canvas.pen_color, self, "Choisir la couleur du pinceau")
            if color.isValid():
                self.canvas.set_pen_color(color)
                self.color_sample.setStyleSheet(
                    f"background-color: {color.name()}; border: 1px solid #333;"
                )
                self.pen_action.setChecked(True)
                self.set_tool_mode("pen")

        def on_drawing_changed(self):
            """Marque l'image comme modifiée."""
            self.is_modified = True

        def on_mouse_moved(self, point):
            """Met à jour les coordonnées affichées dans la barre d'état."""
            self.cursor_pos = point
            self.update_status_message()

        def update_status_message(self):
            """Affiche les informations d'outil et de position dans la barre d'état."""
            tool_name = "Gomme" if self.canvas.mode == "eraser" else "Pinceau"
            width = self.canvas.pen_width
            x, y = self.cursor_pos.x(), self.cursor_pos.y()
            self.statusBar().showMessage(
                f"Outil : {tool_name} | Épaisseur : {width}px | Position : ({x}, {y})"
            )

        def new_drawing(self):
            """Réinitialise le canevas après confirmation si modifié."""
            if self.is_modified:
                reply = QMessageBox.question(
                    self,
                    "Nouveau dessin",
                    "Le dessin actuel n'est pas enregistré. Voulez-vous vraiment le réinitialiser ?",
                    QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
                    QMessageBox.StandardButton.No
                )
                if reply != QMessageBox.StandardButton.Yes:
                    return

            self.canvas.clear_canvas()
            self.is_modified = False

        def save_image(self):
            """Exporte le dessin sous forme de fichier image (PNG, JPG)."""
            file_path, _ = QFileDialog.getSaveFileName(
                self,
                "Enregistrer le dessin",
                "mon_dessin.png",
                "Images PNG (*.png);;Images JPEG (*.jpg *.jpeg);;Tous les fichiers (*)"
            )
            if not file_path:
                return False

            if self.canvas.pixmap.save(file_path):
                self.is_modified = False
                QMessageBox.information(self, "Succès", "Image enregistrée avec succès !")
                return True
            else:
                QMessageBox.critical(self, "Erreur", "Impossible d'enregistrer l'image.")
                return False

        def closeEvent(self, event):
            """Demande confirmation avant fermeture si le dessin contient des modifications non enregistrées."""
            if self.is_modified:
                reply = QMessageBox.question(
                    self,
                    "Quitter",
                    "Votre dessin contient des modifications non enregistrées.\nVoulez-vous vraiment quitter sans enregistrer ?",
                    QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
                    QMessageBox.StandardButton.No
                )
                if reply == QMessageBox.StandardButton.Yes:
                    event.accept()
                else:
                    event.ignore()
            else:
                event.accept()


    if __name__ == "__main__":
        app = QApplication(sys.argv)
        window = MainWindow()
        window.show()
        sys.exit(app.exec())
    ```

---

Cet exercice met en valeur le dessin graphique 2D avec `QPainter`, le traitement réactif des événements de souris,
la synchronisation de widgets interactifs, l'utilisation de boîtes de dialogue de sélection et l'implémentation de
barres
d'outils et d'état.
