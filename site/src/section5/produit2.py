from typing import Any, Protocol, runtime_checkable

@runtime_checkable
class HasCle(Protocol):
    """
    Protocole qui définit l'exigence structurelle :
    toute classe compatible doit avoir une méthode _cle().
    """
    def _cle(self) -> Any:
        ...

class ComparableMixin:
    """
    Fournit <, <=, > et >=.
    L'exigence de la méthode _cle() est désormais gérée par le protocole HasCle.
    """

    def __lt__(self: HasCle, other: Any) -> bool:
        if not isinstance(other, HasCle):
            return NotImplemented
        # On considère que 'self' possède _cle() car c'est le contrat du mixin
        return self._cle() < other._cle()

    def __le__(self: HasCle, other: Any) -> bool:
        if not isinstance(other, HasCle):
            return NotImplemented
        return self._cle() <= other._cle()

    def __gt__(self: HasCle, other: Any) -> bool:
        if not isinstance(other, HasCle):
            return NotImplemented
        return self._cle() > other._cle()

    def __ge__(self: HasCle, other: Any) -> bool:
        if not isinstance(other, HasCle):
            return NotImplemented
        return self._cle() >= other._cle()



# CAS 1 : Utilisation correcte
class Produit(ComparableMixin):
    def __init__(self, nom: str, prix: int):
        self.nom = nom
        self.prix = prix

    def _cle(self) -> int:
        return self.prix


p1 = Produit("Café", 5)
p2 = Produit("Thé", 3)

print(p1 > p2)  # True (5 > 3)
print(p1 < p2)  # False

# CAS 2 : Comparaison avec un objet incompatible (ex: un entier)
# print(p1 < 10)  # Lèvera AttributeError : TypeError: '<' not supported between instances of 'Produit' and 'int'


# CAS 3 : Classe qui oublie _cle()
class MauvaiseClasse(ComparableMixin):
    pass


m = MauvaiseClasse()
m < m  # -> Lèvera une TypeError: '<' not supported between instances of 'MauvaiseClasse' and 'MauvaiseClasse'
