from deal import pre, post, inv


@inv(lambda self: self._solde >= 0)  # Invariant : solde toujours ≥ 0
class CompteBancaire:
    def __init__(self, titulaire: str, solde_initial: float = 0.0):
        self._solde = solde_initial
        self.titulaire = titulaire


    @pre(lambda self, montant: montant > 0)  # Précondition : montant positif
    def deposer(self, montant: float):
        """Dépose un montant sur le compte."""
        self._solde += montant

    @pre(lambda self, montant: 0 < montant <= self._solde, exception=ValueError)  # Précondition
    def retirer(self, montant: float):
        """Retire un montant du compte. Lève ValueError si solde insuffisant."""
        self._solde -= montant

    @property
    @post(lambda result: result >= 0)  # Postcondition
    def solde(self) -> float:
        """Retourne le solde actuel."""
        return self._solde