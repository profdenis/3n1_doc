from typing import Protocol, Any, runtime_checkable
from functools import total_ordering

@runtime_checkable
class KeyProvider(Protocol):
    @property
    def key(self) -> Any:
        ...

@total_ordering
class KeyComparisonMixin:
    """Ajoute la capacité de comparaison via la propriété 'key'."""

    def __eq__(self, other: Any) -> bool:
        # On ignore l'erreur car mypy ne voit pas 'key' dans KeyComparisonMixin,
        # mais nous savons que l'héritage multiple l'apportera au runtime.
        # On utilise [attr-defined] pour être précis et ne pas masquer d'autres erreurs.
        return self.key == other.key  # type: ignore[attr-defined]

    def __lt__(self, other: Any) -> bool:
        return self.key < other.key  # type: ignore[attr-defined]

# --- Le reste du code reste identique ---
class Utilisateur:
    def __init__(self, id_num: int):
        self.id_num = id_num
    @property
    def key(self) -> int:
        return self.id_num

class SortableUser(KeyComparisonMixin, Utilisateur):
    pass

u = SortableUser(10)
print(u == u) # True
