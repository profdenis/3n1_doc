from typing import TypeVar, Generic, List

T = TypeVar('T')


class Pile(Generic[T]):
    def __init__(self) -> None:
        self._elements: List[T] = []

    def empiler(self, item: T) -> None:
        self._elements.append(item)

    def depiler(self) -> T:
        return self._elements.pop()


# Test :
pile_de_entiers: Pile[int] = Pile()
pile_de_entiers.empiler(1)
pile_de_entiers.empiler(2)
print(pile_de_entiers.depiler())  # Affiche 2

pile_de_strings: Pile[str] = Pile()
pile_de_strings.empiler("A")
pile_de_strings.empiler("B")
print(pile_de_strings.depiler())  # Affiche "B"