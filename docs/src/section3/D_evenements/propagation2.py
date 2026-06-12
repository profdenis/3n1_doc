import sys
from PySide6.QtWidgets import QApplication, QWidget, QVBoxLayout, QLineEdit, QLabel
from PySide6.QtCore import QObject, QEvent

class BinaryInputFilter(QObject):
    def eventFilter(self, obj, event):
        # Filtrer les appuis sur les touches pour tous les widgets
        if event.type() == QEvent.Type.KeyPress:
            # Ne filtrer que les widgets QLineEdit
            if isinstance(obj, QLineEdit):
                text = event.text()
                if text and text not in ('0', '1'):
                    # Bloquer l'événement (ne pas le laisser atteindre le widget)
                    return True
        # Permettre le traitement normal
        return False

app = QApplication(sys.argv)

# Installer le filtre sur l'instance de l'application
binary_filter = BinaryInputFilter()
app.installEventFilter(binary_filter)

window = QWidget()
layout = QVBoxLayout(window)
layout.addWidget(QLabel("Seuls '0' et '1' sont autorisés :"))
layout.addWidget(QLineEdit())
layout.addWidget(QLineEdit())
window.show()

sys.exit(app.exec())

