import json


class ReprMixin:
    """Fournit un __repr__ lisible à partir des attributs de l'objet."""

    def __repr__(self):
        attributs = ", ".join(f"{nom}={valeur!r}" for nom, valeur in vars(self).items())
        return f"{type(self).__name__}({attributs})"


class JsonMixin:
    """Ajoute to_json(). Exige que les attributs de l'objet soient sérialisables."""

    def to_json(self):
        return json.dumps(vars(self), ensure_ascii=False)


class Livre(JsonMixin):
    def __init__(self, titre, auteur):
        self.titre = titre
        self.auteur = auteur


print(Livre("Dune", "Frank Herbert").to_json())


# {"titre": "Dune", "auteur": "Frank Herbert"}

class Produit(ReprMixin, JsonMixin):
    def __init__(self, nom, prix):
        self.nom = nom
        self.prix = prix

    def _cle(self):  # exigence de ComparableMixin
        return self.prix


clavier = Produit("Clavier", 49.99)
souris = Produit("Souris", 24.50)

print(clavier)  # Produit(nom='Clavier', prix=49.99)
print(souris.to_json())  # {"nom": "Souris", "prix": 24.5}
print(Produit.__mro__)
# (Produit, ReprMixin, JsonMixin, ComparableMixin, object)
