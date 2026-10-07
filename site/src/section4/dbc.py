from deal import pre, post, inv, ensure


@inv(lambda self: self.solde >= 0)
class CompteBancaire:
    def __init__(self, solde_initial: float):
        self.solde = solde_initial

    @pre(lambda self, montant: montant > 0)  # Le montant doit être positif
    @pre(lambda self, montant: self.solde >= montant)  # Solde suffisant
    @ensure(lambda self, montant, result: self.solde == self.solde + montant - montant)  # Exemple simplifié
    def retirer(self, montant: float) -> float:
        print(f"Retrait de {montant}€ effectué.")
        self.solde -= montant
        return self.solde

    @pre(lambda self, montant: montant > 0)
    def deposer(self, montant: float):
        self.solde += montant
        print(f"Dépôt de {montant}€ effectué.")


# --- Tests ---

compte = CompteBancaire(100)

# 1. Test succès
compte.retirer(50)  # OK

# 2. Violation de précondition (montant négatif)
try:
    compte.retirer(-10)
except Exception as e:
    print(f"Erreur : {e}")  # PreconditionViolation

# 3. Violation de précondition (solde insuffisant)
try:
    compte.retirer(1000)
except Exception as e:
    print(f"Erreur : {e}")  # PreconditionViolation

try:
    compte.solde = -50
except Exception as e:
    print(f"Erreur : {e}")