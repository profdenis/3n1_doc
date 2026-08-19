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
            print("MainFrame : événement MouseButtonPress (reçu de l'enfant)")
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
