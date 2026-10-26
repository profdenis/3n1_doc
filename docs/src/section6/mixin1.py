from typing import Protocol, Any

# 1. Le PROTOCOLE : Il définit ce que le Mixin exige de la classe hôte.
# On ne dit pas que l'objet EST un "HasName", on dit qu'il doit avoir l'attribut "name".
class HasName(Protocol):
    name: str

# 2. LE MIXIN : Il implémente une stratégie de comparaison spécifique.
# Il est petit, a une seule responsabilité et n'est pas instancié seul.
class NameComparatorMixin:
    """Ajoute la capacité de se comparer par nom."""

    def compare_to_name(self, other: HasName) -> int:
        # Le Mixin utilise l'attribut 'name' de l'instance (self)
        # et de l'autre objet (other), garantis par le Protocol.
        if self.name < other.name:
            return -1
        if self.name > other.name:
            return 1
        return 0

# 3. LES CLASSES MÉTIER : Elles sont totalement indépendantes au départ.
class User:
    def __init__(self, name: str, user_id: int):
        self.name = name
        self.user_id = user_id

class Product:
    def __init__(self, name: str, price: float):
        self.name = name
        self.price = price

# 4. L'APPLICATION : On "injecte" la capacité via l'héritage multiple.
class SortableUser(NameComparatorMixin, User):
    pass

class SortableProduct(NameComparatorMixin, Product):
    pass

# --- Test ---
u = SortableUser("Alice", 1)
p = SortableProduct("Bob", 10.5)

print(u.compare_to_name(p))  # Résultat : -1 (Alice < Bob)
