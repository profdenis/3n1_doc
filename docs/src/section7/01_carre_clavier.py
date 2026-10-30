import sys
import pygame

# 1. Initialisation de Pygame
pygame.init()

# Dimensions de la fenêtre
LARGEUR, HAUTEUR = 800, 600
FENETRE = pygame.display.set_mode((LARGEUR, HAUTEUR))
pygame.display.set_caption("Introduction Pygame - Déplacement au clavier")

# Horloge pour réguler le nombre d'images par seconde (FPS)
horloge = pygame.time.Clock()
FPS = 60

# Couleurs (R, V, B)
COULEUR_FOND = (30, 30, 30)
COULEUR_CARRE = (70, 130, 180)  # Bleu acier

# Propriétés du carré du joueur
taille_carre = 50
x = (LARGEUR - taille_carre) // 2
y = (HAUTEUR - taille_carre) // 2
vitesse = 5

# Boucle principale du jeu
en_cours = True
while en_cours:
    # --- 1. Gestion des événements ---
    for evenement in pygame.event.get():
        if evenement.type == pygame.QUIT:
            en_cours = False

    # --- 2. Mise à jour de l'état (déplacement) ---
    touches = pygame.key.get_pressed()
    if touches[pygame.K_LEFT]:
        x -= vitesse
    if touches[pygame.K_RIGHT]:
        x += vitesse
    if touches[pygame.K_UP]:
        y -= vitesse
    if touches[pygame.K_DOWN]:
        y += vitesse

    # Garder le carré dans les limites de l'écran
    x = max(0, min(LARGEUR - taille_carre, x))
    y = max(0, min(HAUTEUR - taille_carre, y))

    # --- 3. Dessin / Rendu ---
    FENETRE.fill(COULEUR_FOND)
    pygame.draw.rect(FENETRE, COULEUR_CARRE, (x, y, taille_carre, taille_carre))

    # --- 4. Rafraîchissement de l'affichage et régulation ---
    pygame.display.flip()
    horloge.tick(FPS)

# Fermeture propre de Pygame
pygame.quit()
sys.exit()
