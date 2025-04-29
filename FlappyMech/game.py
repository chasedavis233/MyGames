
import pygame
import sys
import random
import os

# Initialize pygame
pygame.init()

# Screen setup
WIDTH, HEIGHT = 500, 700
screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.RESIZABLE)
pygame.display.set_caption("FlappyMech")

# Load assets
def load_image(name, fallback_color):
    path = os.path.join("assets", name)
    if os.path.exists(path):
        return pygame.image.load(path)
    else:
        surf = pygame.Surface((50, 50))
        surf.fill(fallback_color)
        return surf

bird_img = load_image("bird.png", (255, 0, 0))
bg_img = load_image("background.png", (135, 206, 250))

# Bird settings
bird = pygame.Rect(100, HEIGHT//2, 40, 40)
gravity = 0.5
bird_movement = 0

# Pipes
pipe_width = 80
pipe_height = 500
gap = 200
pipe_color = (34, 139, 34)
pipes = []

# Clock
clock = pygame.time.Clock()

# Font
font = pygame.font.SysFont('Arial', 40)

# Score
score = 0

# Game state
game_active = False

# Functions
def create_pipe():
    y_pos = random.randint(150, HEIGHT - 150)
    top = pygame.Rect(WIDTH, y_pos - gap - pipe_height, pipe_width, pipe_height)
    bottom = pygame.Rect(WIDTH, y_pos, pipe_width, pipe_height)
    return top, bottom

def move_pipes(pipes):
    for pipe in pipes:
        pipe.x -= 5
    return [pipe for pipe in pipes if pipe.right > 0]

def draw_pipes(pipes):
    for pipe in pipes:
        pygame.draw.rect(screen, pipe_color, pipe)

# Main game loop
running = True
SPAWNPIPE = pygame.USEREVENT
pygame.time.set_timer(SPAWNPIPE, 1500)

while running:
    screen.fill((0, 0, 0))

    # Background
    if bg_img:
        scaled_bg = pygame.transform.scale(bg_img, (WIDTH, HEIGHT))
        screen.blit(scaled_bg, (0, 0))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                if not game_active:
                    # Start game
                    game_active = True
                    pipes.clear()
                    bird.y = HEIGHT // 2
                    bird_movement = 0
                    score = 0
                else:
                    bird_movement = 0
                    bird_movement -= 10

        if event.type == SPAWNPIPE and game_active:
            pipes.extend(create_pipe())

        if event.type == pygame.VIDEORESIZE:
            WIDTH, HEIGHT = event.w, event.h
            screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.RESIZABLE)

    if game_active:
        # Bird movement
        bird_movement += gravity
        bird.y += int(bird_movement)

        # Draw bird
        scaled_bird = pygame.transform.scale(bird_img, (bird.width, bird.height))
        screen.blit(scaled_bird, (bird.x, bird.y))

        # Pipes
        pipes = move_pipes(pipes)
        draw_pipes(pipes)

        # Collision
        for pipe in pipes:
            if bird.colliderect(pipe):
                game_active = False
        if bird.top <= 0 or bird.bottom >= HEIGHT:
            game_active = False

        # Score
        for pipe in pipes:
            if pipe.centerx == bird.centerx:
                score += 0.5  # Top and bottom pipes both counted

        score_surface = font.render(str(int(score)), True, (255, 255, 255))
        screen.blit(score_surface, (WIDTH//2 - score_surface.get_width()//2, 20))

    else:
        # Start screen
        start_surface = font.render("Press SPACE to Start", True, (255, 255, 255))
        screen.blit(start_surface, (WIDTH//2 - start_surface.get_width()//2, HEIGHT//2 - 50))

    pygame.display.update()
    clock.tick(60)

pygame.quit()
sys.exit()
