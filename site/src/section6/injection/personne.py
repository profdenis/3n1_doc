from dataclasses import dataclass


@dataclass
class Personne:
    """Représentation d'une personne dans le domaine métier."""
    id: int
    nom: str
    prenom: str
    age: int
    courriel: str

    def __str__(self) -> str:
        return f"[{self.id}] {self.prenom} {self.nom}, {self.age} ans ({self.courriel})"
