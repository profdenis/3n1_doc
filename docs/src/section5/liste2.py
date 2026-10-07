from typing import TypeVar, List

T = TypeVar('T')


def premier_element(liste: List[T]) -> T:
    return liste[0]


# Utilisation :
noms: List[str] = ["Alice", "Bob"]
premier_nom: str = premier_element(noms)  # Type connu : str
print(premier_nom)  # Affiche "Alice"