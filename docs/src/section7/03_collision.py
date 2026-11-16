import random
import sys
import pygame

# 1. Initialisation de Pygame et du module de polices
pygame.init()

# Dimensions de la fenêtre
LARGEUR, HAUTEUR = 800, 600
FENETRE = pygame.display.set_mode((LARGEUR, HAUTEUR))
pygame.display.set_caption("Pygame - Détection de collision et Game Over")

# Horloge pour réguler le taux de rafraîchissement
horloge = pygame.time.Clock()
FPS = 60

# Couleurs (R, V, B)
COULEUR_FOND = (30, 30, 30)
COULEUR_JOUEUR = (70, 130, 180)    # Bleu acier
COULEUR_AUTONOME = (220, 80, 80)   # Rouge corail
COULEUR_TEXTE = (255, 255, 255)    # Blanc
COULEUR_GAMEOVER = (230, 50, 50)   # Rouge vif

# Polices pour les messages de fin de partie
police_titre = pygame.font.Font(None, 64)
police_sous_titre = pygame.font.Font(None, 32)

# --- Propriétés du joueur (contrôlé au clavier) ---
taille_joueur = 50
joueur_x = (LARGEUR - taille_joueur) // 4
joueur_y = (HAUTEUR - taille_joueur) // 2
vitesse_joueur = 5

# --- Propriétés du carré autonome ---
taille_autonome = 40
autonome_x = (LARGEUR - taille_autonome) * 3 // 4
autonome_y = (HAUTEUR - taille_autonome) // 2
vitesse_auto_x = random.choice([-4, -3, 3, 4])
vitesse_auto_y = random.choice([-4, -3, 3, 4])

compteur_changement = 0
INTERVALLE_CHANGEMENT = 90

# État du jeu
en_cours = True
partie_terminee = False

# Boucle principale du jeu
while en_cours:
    # --- 1. Gestion des événements ---
    for evenement in pygame.event.get():
        if evenement.type == pygame.QUIT:
            en_cours = False
        elif evenement.type == pygame.KEYDOWN and partie_terminee:
            # Quitter avec la touche Échap (ESC)
            if evenement.key == pygame.K_ESCAPE:
                en_cours = False

    # --- 2. Mise à jour de la logique si la partie est active ---
    if not partie_terminee:
        # Déplacement du joueur au clavier
        touches = pygame.key.get_pressed()
        if touches[pygame.K_LEFT]:
            joueur_x -= vitesse_joueur
        if touches[pygame.K_RIGHT]:
            joueur_x += vitesse_joueur
        if touches[pygame.K_UP]:
            joueur_y -= vitesse_joueur
        if touches[pygame.K_DOWN]:
            joueur_y += vitesse_joueur

        # Limites de l'écran pour le joueur
        joueur_x = max(0, min(LARGEUR - taille_joueur, joueur_x))
        joueur_y = max(0, min(HAUTEUR - taille_joueur, joueur_y))

        # Déplacement et rebonds du carré autonome
        autonome_x += vitesse_auto_x
        autonome_y += vitesse_auto_y

        if autonome_x <= 0:
            autonome_x = 0
            vitesse_auto_x = abs(vitesse_auto_x)
        elif autonome_x >= LARGEUR - taille_autonome:
            autonome_x = LARGEUR - taille_autonome
            vitesse_auto_x = -abs(vitesse_auto_x)

        if autonome_y <= 0:
            autonome_y = 0
            vitesse_auto_y = abs(vitesse_auto_y)
        elif autonome_y >= HAUTEUR - taille_autonome:
            autonome_y = HAUTEUR - taille_autonome
            vitesse_auto_y = -abs(vitesse_auto_y)

        # Changement de direction aléatoire périodique
        compteur_changement += 1
        if compteur_changement >= INTERVALLE_CHANGEMENT:
            compteur_changement = 0
            vitesse_auto_x = random.randint(-5, 5)
            vitesse_auto_y = random.randint(-5, 5)
            if vitesse_auto_x == 0 and vitesse_auto_y == 0:
                vitesse_auto_x = 3

        # Détection des collisions avec pygame.Rect
        rect_joueur = pygame.Rect(joueur_x, joueur_y, taille_joueur, taille_joueur)
        rect_autonome = pygame.Rect(autonome_x, autonome_y, taille_autonome, taille_autonome)

        if rect_joueur.colliderect(rect_autonome):
            partie_terminee = True

    # --- 3. Dessin / Rendu ---
    FENETRE.fill(COULEUR_FOND)

    # Dessin des deux carrés
    pygame.draw.rect(FENETRE, COULEUR_JOUEUR, (joueur_x, joueur_y, taille_joueur, taille_joueur))
    pygame.draw.rect(FENETRE, COULEUR_AUTONOME, (autonome_x, autonome_y, taille_autonome, taille_autonome))

    # Affichage de l'écran Game Over si collision
    if partie_terminee:
        # Message principal
        surface_titre = police_titre.render("GAME OVER", True, COULEUR_GAMEOVER)
        rect_titre = surface_titre.get_rect(center=(LARGEUR // 2, HAUTEUR // 2 - 30))
        FENETRE.blit(surface_titre, rect_titre)

        # Message d'instruction
        surface_instruction = police_sous_titre.render("Appuyez sur ESC pour quitter", True, COULEUR_TEXTE)
        rect_instruction = surface_instruction.get_rect(center=(LARGEUR // 2, HAUTEUR // 2 + 30))
        FENETRE.blit(surface_instruction, rect_instruction)

    # --- 4. Rafraîchissement et régulation ---
    pygame.display.flip()
    horloge.tick(FPS)

# Fermeture propre
pygame.quit()
sys.exit()
