import random
import sys
import pygame

# 1. Initialisation de Pygame
pygame.init()

# Dimensions de la fenêtre
LARGEUR, HAUTEUR = 800, 600
FENETRE = pygame.display.set_mode((LARGEUR, HAUTEUR))
pygame.display.set_caption("Pygame - Carré Joueur et Carré Aléatoire Autonome")

# Horloge pour réguler le taux de rafraîchissement
horloge = pygame.time.Clock()
FPS = 60

# Couleurs (R, V, B)
COULEUR_FOND = (30, 30, 30)
COULEUR_JOUEUR = (70, 130, 180)    # Bleu acier
COULEUR_AUTONOME = (220, 80, 80)   # Rouge corail

# --- Propriétés du joueur (contrôlé au clavier) ---
taille_joueur = 50
joueur_x = (LARGEUR - taille_joueur) // 4
joueur_y = (HAUTEUR - taille_joueur) // 2
vitesse_joueur = 5

# --- Propriétés de l'élément autonome (déplacement au hasard) ---
taille_autonome = 40
autonome_x = (LARGEUR - taille_autonome) * 3 // 4
autonome_y = (HAUTEUR - taille_autonome) // 2
vitesse_auto_x = random.choice([-4, -3, 3, 4])
vitesse_auto_y = random.choice([-4, -3, 3, 4])

# Minuteur pour changer la trajectoire aléatoirement de temps en temps
compteur_changement = 0
INTERVALLE_CHANGEMENT = 90  # Environ toutes les 1.5 secondes (à 60 FPS)

# Boucle principale du jeu
en_cours = True
while en_cours:
    # --- 1. Gestion des événements ---
    for evenement in pygame.event.get():
        if evenement.type == pygame.QUIT:
            en_cours = False

    # --- 2. Mise à jour du carré Joueur (clavier) ---
    touches = pygame.key.get_pressed()
    if touches[pygame.K_LEFT]:
        joueur_x -= vitesse_joueur
    if touches[pygame.K_RIGHT]:
        joueur_x += vitesse_joueur
    if touches[pygame.K_UP]:
        joueur_y -= vitesse_joueur
    if touches[pygame.K_DOWN]:
        joueur_y += vitesse_joueur

    # Garder le joueur dans l'écran
    joueur_x = max(0, min(LARGEUR - taille_joueur, joueur_x))
    joueur_y = max(0, min(HAUTEUR - taille_joueur, joueur_y))

    # --- 3. Mise à jour du carré Autonome (hasard et rebonds) ---
    autonome_x += vitesse_auto_x
    autonome_y += vitesse_auto_y

    # Rebond sur les bords horizontaux (gauche / droite)
    if autonome_x <= 0:
        autonome_x = 0
        vitesse_auto_x = abs(vitesse_auto_x)
    elif autonome_x >= LARGEUR - taille_autonome:
        autonome_x = LARGEUR - taille_autonome
        vitesse_auto_x = -abs(vitesse_auto_x)

    # Rebond sur les bords verticaux (haut / bas)
    if autonome_y <= 0:
        autonome_y = 0
        vitesse_auto_y = abs(vitesse_auto_y)
    elif autonome_y >= HAUTEUR - taille_autonome:
        autonome_y = HAUTEUR - taille_autonome
        vitesse_auto_y = -abs(vitesse_auto_y)

    # Changement aléatoire périodique de direction
    compteur_changement += 1
    if compteur_changement >= INTERVALLE_CHANGEMENT:
        compteur_changement = 0
        vitesse_auto_x = random.randint(-5, 5)
        vitesse_auto_y = random.randint(-5, 5)
        # Éviter que le carré ne s'immobilise complètement
        if vitesse_auto_x == 0 and vitesse_auto_y == 0:
            vitesse_auto_x = 3

    # --- 4. Dessin / Rendu ---
    FENETRE.fill(COULEUR_FOND)

    # Dessin du joueur
    pygame.draw.rect(FENETRE, COULEUR_JOUEUR, (joueur_x, joueur_y, taille_joueur, taille_joueur))
    # Dessin du carré autonome
    pygame.draw.rect(FENETRE, COULEUR_AUTONOME, (autonome_x, autonome_y, taille_autonome, taille_autonome))

    # --- 5. Rafraîchissement et régulation ---
    pygame.display.flip()
    horloge.tick(FPS)

# Fermeture propre
pygame.quit()
sys.exit()
