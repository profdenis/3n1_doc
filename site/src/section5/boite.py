from typing import TypeVar, Generic

T = TypeVar('T')  # Paramètre de type (comme <T> en Java)


class Boite(Generic[T]):  # Classe générique
    def __init__(self) -> None:
        self.contenu: T | None = None

    def mettre(self, item: T) -> None:
        self.contenu = item

    def obtenir(self) -> T | None:
        return self.contenu


# Utilisation :
boite_de_strings: Boite[str] = Boite()
boite_de_strings.mettre("Hello")
message: str | None = boite_de_strings.obtenir()  # Type connu : str ou None
print(message)  # Affiche "Hello"