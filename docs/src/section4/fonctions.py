def additionner(a, b):
    return a + b


def diviser(a, b):
    if b == 0:
        raise ValueError("Le diviseur ne peut pas être nul.")
    if a < 0:
        raise ValueError("Le dividende doit être positif.")
    return a / b


def verifier_age(age):
    if age < 0:
        raise ValueError("L'âge ne peut pas être négatif.")
    if age > 150:
        raise ValueError("L'âge est trop élevé.")
    return True
