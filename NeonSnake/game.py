import pygame
import sys
import random

# Initialize pygame
pygame.init()

# Screen setup
WIDTH, HEIGHT = 600, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.RESIZABLE)
pygame.display.set_caption("NeonSnake")

# Colors
BACKGROUND_COLOR = (10, 10, 10)
SNAKE_COLOR = (0, 255, 0)
FOOD_COLOR = (255, 0, 255)
GRID_COLOR = (40, 40, 40)

# Snake settings
cell_size = 20
snake = [(100, 100), (80, 100), (60, 100)]
snake_dir = (cell_size, 0)

# Food settings
food = (random.randrange(0, WIDTH // cell_size) * cell_size,
        random.randrange(0, HEIGHT // cell_size) * cell_size)

# Clock
clock = pygame.time.Clock()

# Score
score = 0
font = pygame.font.SysFont('Arial', 30)

# Draw the grid
def draw_grid():
    for x in range(0, WIDTH, cell_size):
        pygame.draw.line(screen, GRID_COLOR, (x, 0), (x, HEIGHT))
    for y in range(0, HEIGHT, cell_size):
        pygame.draw.line(screen, GRID_COLOR, (0, y), (WIDTH, y))

# Main game loop
running = True
while running:
    screen.fill(BACKGROUND_COLOR)
    draw_grid()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP and snake_dir[1] == 0:
                snake_dir = (0, -cell_size)
            if event.key == pygame.K_DOWN and snake_dir[1] == 0:
                snake_dir = (0, cell_size)
            if event.key == pygame.K_LEFT and snake_dir[0] == 0:
                snake_dir = (-cell_size, 0)
            if event.key == pygame.K_RIGHT and snake_dir[0] == 0:
                snake_dir = (cell_size, 0)

        if event.type == pygame.VIDEORESIZE:
            WIDTH, HEIGHT = event.w, event.h
            screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.RESIZABLE)

    # Move snake
    new_head = (snake[0][0] + snake_dir[0], snake[0][1] + snake_dir[1])
    snake = [new_head] + snake[:-1]

    # Check collisions
    if new_head in snake[1:] or \
       new_head[0] < 0 or new_head[1] < 0 or \
       new_head[0] >= WIDTH or new_head[1] >= HEIGHT:
        running = False

    # Check food collision
    if new_head == food:
        snake.append(snake[-1])
        food = (random.randrange(0, WIDTH // cell_size) * cell_size,
                random.randrange(0, HEIGHT // cell_size) * cell_size)
        score += 1

    # Draw snake
    for block in snake:
        pygame.draw.rect(screen, SNAKE_COLOR, pygame.Rect(block[0], block[1], cell_size - 2, cell_size - 2))

    # Draw food
    pygame.draw.rect(screen, FOOD_COLOR, pygame.Rect(food[0], food[1], cell_size - 2, cell_size - 2))

    # Draw score
    score_surface = font.render(f"Score: {score}", True, (255, 255, 255))
    screen.blit(score_surface, (10, 10))

    pygame.display.update()
    clock.tick(10)

pygame.quit()
sys.exit()
