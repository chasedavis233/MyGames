## FIX SHOOTING

import pygame
import sys
import random

# Initialize
pygame.init()
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.RESIZABLE)
pygame.display.set_caption("Alien Blaster")

clock = pygame.time.Clock()

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
PLAYER_COLOR = (0, 255, 255)
BULLET_COLOR = (255, 255, 0)
ALIEN_COLOR = (255, 0, 255)

# Player
player = pygame.Rect(WIDTH//2 - 25, HEIGHT - 60, 50, 20)
player_speed = 7
bullets = []

# Aliens
aliens = []
alien_rows = 5
alien_cols = 10
alien_width = 40
alien_height = 30
alien_dx = 2
alien_dy = 10

for row in range(alien_rows):
    for col in range(alien_cols):
        aliens.append(pygame.Rect(col * 60 + 50, row * 50 + 30, alien_width, alien_height))

alien_direction = 1
alien_bullets = []

# Score
score = 0
font = pygame.font.SysFont('Arial', 30)

# Main game loop
running = True
while running:
    screen.fill(BLACK)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.VIDEORESIZE:
            WIDTH, HEIGHT = event.w, event.h
            screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.RESIZABLE)

    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT] and player.left > 0:
        player.x -= player_speed
    if keys[pygame.K_RIGHT] and player.right < WIDTH:
        player.x += player_speed
    if keys[pygame.K_SPACE]:
        if len(bullets) == 0 or pygame.time.get_ticks() - bullets[-1][2] > 300:
            bullets.append([pygame.Rect(player.centerx - 2, player.top, 4, 10), pygame.time.get_ticks()])

    # Move bullets
    for b in bullets[:]:
        b[0].y -= 8
        if b[0].bottom < 0:
            bullets.remove(b)

    # Move aliens
    move_down = False
    for alien in aliens:
        alien.x += alien_dx * alien_direction
        if alien.left <= 0 or alien.right >= WIDTH:
            move_down = True
    if move_down:
        alien_direction *= -1
        for alien in aliens:
            alien.y += alien_dy

    # Random alien shooting
    if random.randint(0, 100) < 2 and aliens:
        shooter = random.choice(aliens)
        alien_bullets.append(pygame.Rect(shooter.centerx, shooter.bottom, 4, 10))

    # Move alien bullets
    for ab in alien_bullets[:]:
        ab.y += 5
        if ab.top > HEIGHT:
            alien_bullets.remove(ab)

    # Collision: player bullets vs aliens
    for bullet in bullets[:]:
        for alien in aliens[:]:
            if bullet[0].colliderect(alien):
                bullets.remove(bullet)
                aliens.remove(alien)
                score += 100
                break

    # Collision: alien bullets vs player
    for ab in alien_bullets:
        if ab.colliderect(player):
            running = False

    # Draw player
    pygame.draw.rect(screen, PLAYER_COLOR, player)

    # Draw bullets
    for b in bullets:
        pygame.draw.rect(screen, BULLET_COLOR, b[0])

    # Draw aliens
    for alien in aliens:
        pygame.draw.rect(screen, ALIEN_COLOR, alien)

    # Draw alien bullets
    for ab in alien_bullets:
        pygame.draw.rect(screen, WHITE, ab)

    # Score
    score_surface = font.render(f"Score: {score}", True, WHITE)
    screen.blit(score_surface, (10, 10))

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
sys.exit()
