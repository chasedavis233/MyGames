
import pygame
import sys
import random
import os

# Initialize pygame
pygame.init()

# Screen setup
WIDTH, HEIGHT = 600, 500
screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.RESIZABLE)
pygame.display.set_caption("NeonClash")

# Load assets
def load_image(name):
    path = os.path.join("assets", name)
    if os.path.exists(path):
        return pygame.image.load(path)
    else:
        surf = pygame.Surface((100, 100))
        surf.fill((255, 0, 0))  # Red fallback
        return surf

rock_img = load_image("rock.png")
paper_img = load_image("paper.png")
scissors_img = load_image("scissors.png")

background_color = (10, 10, 30)

choices = ["Rock", "Paper", "Scissors"]
choice_images = {"Rock": rock_img, "Paper": paper_img, "Scissors": scissors_img}

# Fonts
font = pygame.font.SysFont('Arial', 30)

# Clock
clock = pygame.time.Clock()

# Game variables
player_choice = None
ai_choice = None
clash_animation = False
clash_counter = 0
result = None

# Main game loop
running = True

while running:
    screen.fill(background_color)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.MOUSEBUTTONDOWN and not clash_animation:
            x, y = pygame.mouse.get_pos()
            # Detect clicks
            if 50 <= x <= 150 and 200 <= y <= 300:
                player_choice = "Rock"
            if 225 <= x <= 325 and 200 <= y <= 300:
                player_choice = "Paper"
            if 400 <= x <= 500 and 200 <= y <= 300:
                player_choice = "Scissors"
            if player_choice:
                ai_choice = random.choice(choices)
                clash_animation = True
                clash_counter = 0

        if event.type == pygame.VIDEORESIZE:
            WIDTH, HEIGHT = event.w, event.h
            screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.RESIZABLE)

    # Animated Background (simple color waves)
    color_shift = (pygame.time.get_ticks() // 10) % 255
    screen.fill((color_shift, 20, 60))

    if clash_animation:
        clash_counter += 1
        # Animate the clash
        if clash_counter < 30:
            screen.blit(pygame.transform.scale(choice_images[player_choice], (150, 150)), (WIDTH//4 - 75, HEIGHT//2 - 75))
            screen.blit(pygame.transform.scale(choice_images[ai_choice], (150, 150)), (3*WIDTH//4 - 75, HEIGHT//2 - 75))
        else:
            # Show result
            if (player_choice == ai_choice):
                result = "Tie!"
            elif (player_choice == "Rock" and ai_choice == "Scissors") or \
                 (player_choice == "Paper" and ai_choice == "Rock") or \
                 (player_choice == "Scissors" and ai_choice == "Paper"):
                result = "You Win!"
            else:
                result = "You Lose!"

            result_surface = font.render(result, True, (255, 255, 255))
            screen.blit(result_surface, (WIDTH//2 - result_surface.get_width()//2, HEIGHT//2 - result_surface.get_height()//2))

            # Reset after showing result
            if clash_counter > 100:
                clash_animation = False
                player_choice = None
                ai_choice = None
                result = None

    else:
        # Draw choice buttons
        screen.blit(pygame.transform.scale(rock_img, (100, 100)), (50, 200))
        screen.blit(pygame.transform.scale(paper_img, (100, 100)), (225, 200))
        screen.blit(pygame.transform.scale(scissors_img, (100, 100)), (400, 200))

    title = font.render("Choose Rock, Paper, or Scissors!", True, (255, 255, 255))
    screen.blit(title, (WIDTH//2 - title.get_width()//2, 50))

    pygame.display.update()
    clock.tick(60)

pygame.quit()
sys.exit()
