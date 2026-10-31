from typing import Protocol, Any, runtime_checkable
from functools import total_ordering


# 1. Le PROTOCOLE : On définit ce qu'est un objet "comparable par clé"
@runtime_checkable
class KeyProvider(Protocol):
    @property
    def key(self) -> Any:
        ...


# 2. LE MIXIN : On utilise @total_ordering pour une implémentation propre
@total_ordering
class KeyComparisonMixin:
    """Ajoute la capacité de comparaison standard via la propriété 'key'."""

    def __eq__(self: KeyProvider, other: Any) -> bool:
        if not isinstance(other, KeyProvider):
            return NotImplemented  # Indique à Python qu'il ne sait pas comparer
        return self.key == other.key

    def __lt__(self: KeyProvider, other: Any) -> bool:
        if not isinstance(other, KeyProvider):
            return NotImplemented
        return self.key < other.key


# 3. LES CLASSES MÉTIER : Elles restent simples et focalisées sur la donnée
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


# 4. L'APPLICATION : L'héritage multiple injecte les dunders standards
class SortableUser(KeyComparisonMixin, Utilisateur):
    pass


class SortableProduct(KeyComparisonMixin, Produit):
    pass


# --- Test de l'élégance Pythonique ---
u1 = SortableUser(10, "Alice")
u2 = SortableUser(20, "Bob")
p1 = SortableProduct("A", 15.0)

print(f"u1 < u2 ? {u1 < u2}")  # True (10 < 20)
print(f"u1 == u2 ? {u1 == u2}")  # False (10 == 20)
print(f"u1 > u2 ? {u1 > u2}")  # False
print(f"u1 <= u2 ? {u1 <= u2}")  # True (généré par total_ordering)
print(f"u1 == p1 ? {u1 == p1}")  # False (10 == 15.0, mais gère le type grâce à l'isinstance)
