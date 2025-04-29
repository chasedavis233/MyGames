import pygame
import sys
import random

# Initialize
pygame.init()

# Screen
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.RESIZABLE)
pygame.display.set_caption("PowerBounce - Brick Breaker")

# Colors
WHITE = (255, 255, 255)
BALL_COLOR = (255, 255, 0)
PADDLE_COLOR = (0, 255, 255)
BG_COLOR = (20, 20, 20)

# Paddle
PADDLE_WIDTH, PADDLE_HEIGHT = 120, 15
paddle = pygame.Rect(WIDTH//2 - PADDLE_WIDTH//2, HEIGHT - 40, PADDLE_WIDTH, PADDLE_HEIGHT)

# Ball
BALL_RADIUS = 10
ball = pygame.Rect(WIDTH//2, HEIGHT//2, BALL_RADIUS * 2, BALL_RADIUS * 2)
ball_dx, ball_dy = 5, -5

# Bricks
brick_rows = 5
brick_cols = 8
brick_width = WIDTH // brick_cols
brick_height = 30
bricks = []

def create_bricks():
    global bricks
    bricks = []
    for row in range(brick_rows):
        for col in range(brick_cols):
            rect = pygame.Rect(col * brick_width + 5, row * brick_height + 5, brick_width - 10, brick_height - 10)
            color = [random.randint(100, 255) for _ in range(3)]
            bricks.append((rect, color))

create_bricks()

# Clock
clock = pygame.time.Clock()

running = True
while running:
    screen.fill(BG_COLOR)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.VIDEORESIZE:
            WIDTH, HEIGHT = event.w, event.h
            screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.RESIZABLE)
            paddle.y = HEIGHT - 40
            create_bricks()

    # Paddle follows mouse
    mouse_x = pygame.mouse.get_pos()[0]
    paddle.x = mouse_x - PADDLE_WIDTH // 2
    paddle.x = max(0, min(WIDTH - PADDLE_WIDTH, paddle.x))

    # Ball movement
    ball.x += ball_dx
    ball.y += ball_dy

    # Wall collisions
    if ball.left <= 0 or ball.right >= WIDTH:
        ball_dx *= -1
    if ball.top <= 0:
        ball_dy *= -1
    if ball.bottom >= HEIGHT:
        ball.x, ball.y = WIDTH // 2, HEIGHT // 2
        ball_dx, ball_dy = 5, -5
        create_bricks()

    # Paddle collision
    if ball.colliderect(paddle):
        ball_dy *= -1
        ball.y = paddle.y - BALL_RADIUS * 2

    # Brick collisions
    for brick in bricks[:]:
        rect, color = brick
        if ball.colliderect(rect):
            bricks.remove(brick)
            ball_dy *= -1
            break

    # Draw paddle
    pygame.draw.rect(screen, PADDLE_COLOR, paddle)

    # Draw ball
    pygame.draw.ellipse(screen, BALL_COLOR, ball)

    # Draw bricks
    for brick, color in bricks:
        pygame.draw.rect(screen, color, brick)

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
sys.exit()
