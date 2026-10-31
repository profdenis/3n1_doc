from typing import Protocol, Any


# 1. Le PROTOCOLE : Définit une "interface de propriété"
# On exige que l'objet possède une propriété 'key'
class KeyProvider(Protocol):
    @property
    def key(self) -> Any:
        """Retourne la valeur servant de critère de comparaison."""
        ...


# 2. LE MIXIN : Un comparateur universel de propriétés
class KeyComparatorMixin:
    """Ajoute la capacité de se comparer via une propriété 'key'."""

    def compare_to_key(self: KeyProvider, other: KeyProvider) -> int:
        # On accède à 'key' comme un attribut (grâce au protocole)
        # Le Mixin ne sait pas ce qu'est la clé, il sait juste qu'elle est comparable
        val1 = self.key
        val2 = other.key

        if val1 < val2:
            return -1
        if val1 > val2:
            return 1
        return 0


# 3. LES CLASSES MÉTIER : Elles implémentent la propriété 'key'
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


# 4. L'APPLICATION : L'héritage multiple injecte la capacité de comparaison
class SortableUser(KeyComparatorMixin, Utilisateur):
    pass


class SortableProduct(KeyComparatorMixin, Produit):
    pass


# --- Test ---
u = SortableUser(10, "Alice")
p = SortableProduct("ABC", 49.99)

# La comparaison est possible même entre des types différents si les clés le permettent
print(f"Comparaison (10 vs 49.99) : {u.compare_to_key(p)}")
