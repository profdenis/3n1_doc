from typing import Protocol, Any, runtime_checkable, cast
from functools import total_ordering


# 1. Le PROTOCOLE avec @runtime_checkable
# Indispensable pour que isinstance(obj, KeyProvider) fonctionne à l'exécution
@runtime_checkable
class KeyProvider(Protocol):
    @property
    def key(self) -> Any:
        ...


# 2. Le MIXIN "Expert"
@total_ordering
class KeyComparisonMixin:
    """Ajoute la capacité de comparaison standard via la propriété 'key'."""

    def __eq__(self, other: Any) -> bool:
        # On vérifie que 'other' respecte le contrat
        if not isinstance(other, KeyProvider):
            return NotImplemented

        # On vérifie que 'self' respecte le contrat (Type Narrowing)
        # Cette étape est magique : elle sécurise le runtime ET
        # elle "rassure" mypy que self.key existe.
        if not isinstance(self, KeyProvider):
            return NotImplemented

        return self.key == other.key

    def __lt__(self, other: Any) -> bool:
        if not isinstance(other, KeyProvider) or not isinstance(self, KeyProvider):
            return NotImplemented
        return self.key < other.key


# 3. LES CLASSES MÉTIER (Inchangées)
class Utilisateur:
    def __init__(self, id_num: int, nom: str):
        self.id_num = id_num
        self.nom = nom

    @property
    def key(self) -> int:
        return self.id_num


class Produit:
    def __init__(self, reference: str, prix: float):
        self.reference = reference
        self.prix = prix

    @property
    def key(self) -> float:
        return self.prix


# 4. L'APPLICATION
class SortableUser(KeyComparisonMixin, Utilisateur):
    pass


class SortableProduct(KeyComparisonMixin, Produit):
    pass


# --- Test ---
u = SortableUser(10, "Alice")
p = SortableProduct("ABC", 49.99)

print(f"u < p ? {u < p}")  # False
print(f"u == p ? {u == p}")  # False
print(f"u < u ? {u < u}")  # False
