from PySide6.QtCore import QObject, Signal

class Counter(QObject):
    valueChanged = Signal(int)  # Définir un signal personnalisé

    def __init__(self):
        super().__init__()
        self._value = 0

    def increment(self):
        self._value += 1
        self.valueChanged.emit(self._value)  # Émettre le signal

def handle_value(value):
    print(f"Valeur du compteur : {value}")

counter = Counter()
counter.valueChanged.connect(handle_value)
counter.increment()  # Sortie : Valeur du compteur : 1
