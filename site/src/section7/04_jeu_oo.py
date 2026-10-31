"""Exemple d'architecture orientée objet avec Pygame.

Ce script reproduit le comportement de l'exemple de collision précédent
(03_collision.py), mais selon une conception orientée objet modulaire,
extensible et maintenable.
"""

import random
import sys
import pygame


class ElementJeu:
    """Classe de base représentant un élément géométrique dans l'espace 2D du jeu."""

    def __init__(self, x: float, y: float, taille: int, couleur: tuple[int, int, int], limites: tuple[int, int]):
        self.x = x
        self.y = y
        self.taille = taille
        self.couleur = couleur
        self.largeur_ecran, self.hauteur_ecran = limites

    @property
    def rect(self) -> pygame.Rect:
        """Retourne le rectangle de délimitation (Hitbox) de l'élément."""
        return pygame.Rect(int(self.x), int(self.y), self.taille, self.taille)

    def dessiner(self, surface: pygame.Surface) -> None:
        """Affiche le carré sur la surface spécifiée."""
        pygame.draw.rect(surface, self.couleur, self.rect)

    def touche(self, autre: "ElementJeu") -> bool:
        """Détecte si cet élément entre en collision avec un autre élément."""
        return self.rect.colliderect(autre.rect)

    def restreindre_a_ecran(self) -> None:
        """Maintient l'élément à l'intérieur des bordures de la fenêtre."""
        self.x = max(0.0, min(float(self.largeur_ecran - self.taille), self.x))
        self.y = max(0.0, min(float(self.hauteur_ecran - self.taille), self.y))


class Joueur(ElementJeu):
    """Représente le carré contrôlé par l'utilisateur au clavier."""

    def __init__(
        self,
        x: float,
        y: float,
        taille: int = 50,
        couleur: tuple[int, int, int] = (70, 130, 180),
        limites: tuple[int, int] = (800, 600),
        vitesse: float = 5.0,
    ):
        super().__init__(x, y, taille, couleur, limites)
        self.vitesse = vitesse

    def mise_a_jour(self, touches: pygame.key.ScancodeWrapper) -> None:
        """Met à jour la position du joueur en fonction des touches pressées."""
        if touches[pygame.K_LEFT]:
            self.x -= self.vitesse
        if touches[pygame.K_RIGHT]:
            self.x += self.vitesse
        if touches[pygame.K_UP]:
            self.y -= self.vitesse
        if touches[pygame.K_DOWN]:
            self.y += self.vitesse

        self.restreindre_a_ecran()


class CarreAutonome(ElementJeu):
    """Représente un obstacle autonome doté d'une vitesse et d'un comportement aléatoire."""

    def __init__(
        self,
        x: float,
        y: float,
        taille: int = 40,
        couleur: tuple[int, int, int] = (220, 80, 80),
        limites: tuple[int, int] = (800, 600),
        intervalle_changement: int = 90,
    ):
        super().__init__(x, y, taille, couleur, limites)
        self.vx = float(random.choice([-4, -3, 3, 4]))
        self.vy = float(random.choice([-4, -3, 3, 4]))
        self.compteur = 0
        self.intervalle_changement = intervalle_changement

    def mise_a_jour(self) -> None:
        """Déplace le carré, gère les rebonds sur les murs et varie périodiquement la trajectoire."""
        # Déplacement
        self.x += self.vx
        self.y += self.vy

        # Rebonds sur les bordures horizontales
        if self.x <= 0:
            self.x = 0
            self.vx = abs(self.vx)
        elif self.x >= self.largeur_ecran - self.taille:
            self.x = float(self.largeur_ecran - self.taille)
            self.vx = -abs(self.vx)

        # Rebonds sur les bordures verticales
        if self.y <= 0:
            self.y = 0
            self.vy = abs(self.vy)
        elif self.y >= self.hauteur_ecran - self.taille:
            self.y = float(self.hauteur_ecran - self.taille)
            self.vy = -abs(self.vy)

        # Changement périodique de direction
        self.compteur += 1
        if self.compteur >= self.intervalle_changement:
            self.compteur = 0
            self.vx = float(random.randint(-5, 5))
            self.vy = float(random.randint(-5, 5))
            if self.vx == 0 and self.vy == 0:
                self.vx = 3.0


class Jeu:
    """Moteur principal orchestrant la boucle de jeu, les entités et l'affichage."""

    COULEUR_FOND = (30, 30, 30)
    COULEUR_TEXTE = (255, 255, 255)
    COULEUR_GAMEOVER = (230, 50, 50)

    def __init__(self, largeur: int = 800, hauteur: int = 600, fps: int = 60):
        pygame.init()
        self.largeur = largeur
        self.hauteur = hauteur
        self.fps = fps

        self.fenetre = pygame.display.set_mode((self.largeur, self.hauteur))
        pygame.display.set_caption("Pygame - Version Orientée Objet")
        self.horloge = pygame.time.Clock()

        # Polices
        self.police_titre = pygame.font.Font(None, 64)
        self.police_sous_titre = pygame.font.Font(None, 32)

        # Entités
        limites = (self.largeur, self.hauteur)
        self.joueur = Joueur(
            x=(self.largeur - 50) // 4,
            y=(self.hauteur - 50) // 2,
            taille=50,
            limites=limites,
        )
        self.autonome = CarreAutonome(
            x=(self.largeur - 40) * 3 // 4,
            y=(self.hauteur - 40) // 2,
            taille=40,
            limites=limites,
        )

        # État du jeu
        self.en_cours = True
        self.partie_terminee = False

    def gerer_evenements(self) -> None:
        """Traite les événements de la file Pygame."""
        for evenement in pygame.event.get():
            if evenement.type == pygame.QUIT:
                self.en_cours = False
            elif evenement.type == pygame.KEYDOWN:
                if evenement.key == pygame.K_ESCAPE:
                    self.en_cours = False

    def mettre_a_jour(self) -> None:
        """Met à jour l'état logique de la partie."""
        if self.partie_terminee:
            return

        touches = pygame.key.get_pressed()
        self.joueur.mise_a_jour(touches)
        self.autonome.mise_a_jour()

        if self.joueur.touche(self.autonome):
            self.partie_terminee = True

    def dessiner_game_over(self) -> None:
        """Affiche les messages de fin de partie à l'écran."""
        surface_titre = self.police_titre.render("GAME OVER", True, self.COULEUR_GAMEOVER)
        rect_titre = surface_titre.get_rect(center=(self.largeur // 2, self.hauteur // 2 - 30))
        self.fenetre.blit(surface_titre, rect_titre)

        surface_instruction = self.police_sous_titre.render(
            "Appuyez sur ESC pour quitter", True, self.COULEUR_TEXTE
        )
        rect_instruction = surface_instruction.get_rect(center=(self.largeur // 2, self.hauteur // 2 + 30))
        self.fenetre.blit(surface_instruction, rect_instruction)

    def dessiner(self) -> None:
        """Effectue le rendu graphique complet d'une trame."""
        self.fenetre.fill(self.COULEUR_FOND)

        # Dessin des entités
        self.joueur.dessiner(self.fenetre)
        self.autonome.dessiner(self.fenetre)

        if self.partie_terminee:
            self.dessiner_game_over()

        pygame.display.flip()

    def executer(self) -> None:
        """Lance et maintient la boucle principale du jeu."""
        while self.en_cours:
            self.gerer_evenements()
            self.mettre_a_jour()
            self.dessiner()
            self.horloge.tick(self.fps)

        pygame.quit()
        sys.exit()


if __name__ == "__main__":
    jeu = Jeu()
    jeu.executer()
