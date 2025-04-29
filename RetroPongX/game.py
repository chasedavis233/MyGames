
import pygame
import sys

# Initialize pygame
pygame.init()

# Screen setup
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.RESIZABLE)
pygame.display.set_caption("RetroPongX")

# Colors
WHITE = (255, 255, 255)
CYAN = (0, 255, 255)
MAGENTA = (255, 0, 255)
BALL_COLOR = (255, 255, 0)

# Paddle settings
PADDLE_WIDTH, PADDLE_HEIGHT = 15, 100
BALL_SIZE = 20

# Velocities
PADDLE_SPEED = 6
ball_speed_x, ball_speed_y = 5, 5

# Scores
left_score = 0
right_score = 0

# Fonts
font = pygame.font.SysFont('Arial', 30)
big_font = pygame.font.SysFont('Arial', 50)

# Game states
game_mode = None  # None, '1P', '2P'
difficulty = None

# Create paddles and ball
def reset_positions():
    global left_paddle, right_paddle, ball
    left_paddle = pygame.Rect(20, HEIGHT//2 - PADDLE_HEIGHT//2, PADDLE_WIDTH, PADDLE_HEIGHT)
    right_paddle = pygame.Rect(WIDTH - 35, HEIGHT//2 - PADDLE_HEIGHT//2, PADDLE_WIDTH, PADDLE_HEIGHT)
    ball = pygame.Rect(WIDTH//2 - BALL_SIZE//2, HEIGHT//2 - BALL_SIZE//2, BALL_SIZE, BALL_SIZE)

reset_positions()

# Main loop
clock = pygame.time.Clock()
running = True

left_vel = 0
right_vel = 0

while running:
    screen.fill((20, 20, 20))
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if game_mode is None:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1:
                    game_mode = '1P'
                if event.key == pygame.K_2:
                    game_mode = '2P'
        elif game_mode == '1P' and difficulty is None:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_e:
                    difficulty = "easy"
                if event.key == pygame.K_m:
                    difficulty = "medium"
                if event.key == pygame.K_h:
                    difficulty = "hard"
                if event.key == pygame.K_i:
                    difficulty = "impossible"
        else:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_w:
                    left_vel = -PADDLE_SPEED
                if event.key == pygame.K_s:
                    left_vel = PADDLE_SPEED
                if event.key == pygame.K_UP:
                    right_vel = -PADDLE_SPEED
                if event.key == pygame.K_DOWN:
                    right_vel = PADDLE_SPEED
            if event.type == pygame.KEYUP:
                if event.key in [pygame.K_w, pygame.K_s]:
                    left_vel = 0
                if event.key in [pygame.K_UP, pygame.K_DOWN]:
                    right_vel = 0
            if event.type == pygame.VIDEORESIZE:
                WIDTH, HEIGHT = event.w, event.h
                screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.RESIZABLE)
                reset_positions()

    # Start Screens
    if game_mode is None:
        title = big_font.render("RetroPongX", True, WHITE)
        mode1 = font.render("Press 1 for 1 Player", True, CYAN)
        mode2 = font.render("Press 2 for 2 Players", True, CYAN)
        screen.blit(title, (WIDTH//2 - title.get_width()//2, HEIGHT//4))
        screen.blit(mode1, (WIDTH//2 - mode1.get_width()//2, HEIGHT//2))
        screen.blit(mode2, (WIDTH//2 - mode2.get_width()//2, HEIGHT//2 + 50))
    elif game_mode == '1P' and difficulty is None:
        choose = font.render("Choose Difficulty:", True, WHITE)
        easy = font.render("E - Easy", True, CYAN)
        medium = font.render("M - Medium", True, CYAN)
        hard = font.render("H - Hard", True, CYAN)
        impossible = font.render("I - Impossible", True, CYAN)
        screen.blit(choose, (WIDTH//2 - choose.get_width()//2, HEIGHT//4))
        screen.blit(easy, (WIDTH//2 - easy.get_width()//2, HEIGHT//2 - 60))
        screen.blit(medium, (WIDTH//2 - medium.get_width()//2, HEIGHT//2 - 20))
        screen.blit(hard, (WIDTH//2 - hard.get_width()//2, HEIGHT//2 + 20))
        screen.blit(impossible, (WIDTH//2 - impossible.get_width()//2, HEIGHT//2 + 60))
    else:
        # Game play
        left_paddle.y += left_vel
        right_paddle.y += right_vel

        # AI controls for 1P
        if game_mode == '1P':
            ai_speed = 4
            if difficulty == "easy":
                ai_speed = 2
            elif difficulty == "medium":
                ai_speed = 4
            elif difficulty == "hard":
                ai_speed = 6
            elif difficulty == "impossible":
                ai_speed = 9

            if ball.centery < right_paddle.centery:
                right_paddle.y -= ai_speed
            if ball.centery > right_paddle.centery:
                right_paddle.y += ai_speed

        # Boundaries
        left_paddle.y = max(0, min(HEIGHT - PADDLE_HEIGHT, left_paddle.y))
        right_paddle.y = max(0, min(HEIGHT - PADDLE_HEIGHT, right_paddle.y))

        # Ball movement
        ball.x += ball_speed_x
        ball.y += ball_speed_y

        if ball.top <= 0 or ball.bottom >= HEIGHT:
            ball_speed_y *= -1

        if ball.colliderect(left_paddle) or ball.colliderect(right_paddle):
            ball_speed_x *= -1

        if ball.left <= 0:
            right_score += 1
            reset_positions()
        if ball.right >= WIDTH:
            left_score += 1
            reset_positions()

        # Draw everything
        pygame.draw.rect(screen, CYAN, left_paddle)
        pygame.draw.rect(screen, MAGENTA, right_paddle)
        pygame.draw.ellipse(screen, BALL_COLOR, ball)
        pygame.draw.aaline(screen, WHITE, (WIDTH//2, 0), (WIDTH//2, HEIGHT))

        left_text = font.render(str(left_score), True, WHITE)
        right_text = font.render(str(right_score), True, WHITE)
        screen.blit(left_text, (WIDTH//4, 20))
        screen.blit(right_text, (WIDTH*3//4, 20))

    pygame.display.update()
    clock.tick(60)

pygame.quit()
sys.exit()
