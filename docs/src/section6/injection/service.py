try:
    from .personne import Personne
    from .lecteurs import LecteurPersonnes
except (ImportError, ValueError):
    from personne import Personne
    from lecteurs import LecteurPersonnes


class GestionnairePersonnes:
    """
    Service métier de haut niveau.
    Il ignore totalement d'où viennent les données (CSV, JSON, SQLite, API, Mémoire).
    Il dépend UNIQUEMENT du contrat abstrait LecteurPersonnes (Principe DIP).
    La dépendance concrète lui est INJECTÉE lors de son instanciation (Injection par constructeur).
    """

    def __init__(self, source: LecteurPersonnes):
        self._source = source

    def lister_personnes(self) -> list[Personne]:
        """Récupère l'ensemble des personnes via la source injectée."""
        return self._source.charger_personnes()

    def filtrer_par_age_min(self, age_min: int) -> list[Personne]:
        """Logique métier : retourne les personnes ayant au moins l'âge spécifié."""
        return [p for p in self.lister_personnes() if p.age >= age_min]

    def trouver_par_courriel(self, courriel: str) -> Personne | None:
        """Logique métier : recherche une personne par son adresse courriel."""
        for p in self.lister_personnes():
            if p.courriel.lower() == courriel.lower():
                return p
        return None

    def calculer_age_moyen(self) -> float:
        """Logique métier : calcule l'âge moyen du groupe."""
        personnes = self.lister_personnes()
        if not personnes:
            return 0.0
        return sum(p.age for p in personnes) / len(personnes)

    def afficher_rapport(self) -> None:
        """Affiche un résumé console des personnes et statistiques."""
        personnes = self.lister_personnes()
        nom_source = self._source.__class__.__name__
        print(f"=== Rapport des personnes (Source : {nom_source}) ===")
        print(f"Total personnes : {len(personnes)}")
        for p in personnes:
            print(f"  - {p}")
        if personnes:
            print(f"Âge moyen : {self.calculer_age_moyen():.1f} ans")
        print()
