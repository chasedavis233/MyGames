## FIX CONTACT 

import pygame
import sys
import math
import random

# Initialize
pygame.init()
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.RESIZABLE)
pygame.display.set_caption("Meteor Rush")

clock = pygame.time.Clock()

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
SHIP_COLOR = (0, 255, 255)
BULLET_COLOR = (255, 255, 0)
ASTEROID_COLOR = (200, 100, 100)

# Ship
ship_pos = [WIDTH // 2, HEIGHT // 2]
ship_angle = 0
ship_speed = [0, 0]
ship_thrust = 0.2

# Bullets
bullets = []

# Asteroids
asteroids = []

def create_asteroid():
    while True:
        x = random.randint(0, WIDTH)
        y = random.randint(0, HEIGHT)
        if math.hypot(x - ship_pos[0], y - ship_pos[1]) > 100:
            break
    angle = random.uniform(0, 2 * math.pi)
    speed = random.uniform(1, 2)
    return [[x, y], [math.cos(angle)*speed, math.sin(angle)*speed]]

for _ in range(6):
    asteroids.append(create_asteroid())

# Draw functions
def draw_ship(pos, angle):
    sin_a = math.sin(angle)
    cos_a = math.cos(angle)
    points = [
        (pos[0] + 15*cos_a, pos[1] + 15*sin_a),
        (pos[0] - 10*cos_a + 7*sin_a, pos[1] - 10*sin_a - 7*cos_a),
        (pos[0] - 10*cos_a - 7*sin_a, pos[1] - 10*sin_a + 7*cos_a),
    ]
    pygame.draw.polygon(screen, SHIP_COLOR, points)

def wrap(pos):
    pos[0] %= WIDTH
    pos[1] %= HEIGHT
    return pos

# Game loop
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
    if keys[pygame.K_LEFT]:
        ship_angle -= 0.07
    if keys[pygame.K_RIGHT]:
        ship_angle += 0.07
    if keys[pygame.K_UP]:
        ship_speed[0] += ship_thrust * math.cos(ship_angle)
        ship_speed[1] += ship_thrust * math.sin(ship_angle)
    if keys[pygame.K_SPACE]:
        if len(bullets) == 0 or pygame.time.get_ticks() - bullets[-1][2] > 300:
            dx = math.cos(ship_angle) * 8
            dy = math.sin(ship_angle) * 8
            bullets.append([[ship_pos[0], ship_pos[1]], [dx, dy], pygame.time.get_ticks()])

    # Update ship
    ship_pos[0] += ship_speed[0]
    ship_pos[1] += ship_speed[1]
    ship_pos = wrap(ship_pos)

    # Draw ship
    draw_ship(ship_pos, ship_angle)

    # Update bullets
    new_bullets = []
    for b in bullets:
        b[0][0] += b[1][0]
        b[0][1] += b[1][1]
        if 0 <= b[0][0] <= WIDTH and 0 <= b[0][1] <= HEIGHT:
            pygame.draw.circle(screen, BULLET_COLOR, (int(b[0][0]), int(b[0][1])), 4)
            new_bullets.append(b)
    bullets = new_bullets

    # Update asteroids
    for a in asteroids:
        a[0][0] += a[1][0]
        a[0][1] += a[1][1]
        a[0] = wrap(a[0])
        pygame.draw.circle(screen, ASTEROID_COLOR, (int(a[0][0]), int(a[0][1])), 30)

    # Collision detection
    new_asteroids = []
    for a in asteroids:
        hit = False
        for b in bullets:
            if math.hypot(a[0][0] - b[0][0], a[0][1] - b[0][1]) < 30:
                hit = True
                break
        if not hit:
            new_asteroids.append(a)
    asteroids = new_asteroids

    # Refill asteroids
    while len(asteroids) < 6:
        asteroids.append(create_asteroid())

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
sys.exit()
