import pygame
import sys
import random

# Initialize
pygame.init()

CELL_SIZE = 30
GRID_WIDTH = 20
GRID_HEIGHT = 20
WIDTH = CELL_SIZE * GRID_WIDTH
HEIGHT = CELL_SIZE * GRID_HEIGHT

screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.RESIZABLE)
pygame.display.set_caption("MazeMuncher")

clock = pygame.time.Clock()

# Colors
BLACK = (0, 0, 0)
WALL_COLOR = (33, 33, 255)
PACMAN_COLOR = (255, 255, 0)
GHOST_COLOR = (255, 0, 0)
PELLET_COLOR = (255, 182, 193)

# Maze Layout (1=wall, 0=empty)
maze = [[0 for _ in range(GRID_WIDTH)] for _ in range(GRID_HEIGHT)]

# Simple auto-generated walls (you can customize!)
for i in range(GRID_WIDTH):
    maze[0][i] = 1
    maze[GRID_HEIGHT-1][i] = 1
for i in range(GRID_HEIGHT):
    maze[i][0] = 1
    maze[i][GRID_WIDTH-1] = 1
for i in range(2, GRID_WIDTH-2, 4):
    for j in range(2, GRID_HEIGHT-2, 4):
        maze[j][i] = 1

# Player
player_pos = [1, 1]
player_dir = [0, 0]

# Ghosts
ghosts = [[GRID_WIDTH-2, GRID_HEIGHT-2]]
ghost_dir = [[0, 0]]

# Pellets
pellets = []
for y in range(GRID_HEIGHT):
    for x in range(GRID_WIDTH):
        if maze[y][x] == 0 and not (x == 1 and y == 1):
            pellets.append([x, y])

# Score
score = 0
font = pygame.font.SysFont('Arial', 30)

# Functions
def move_entity(pos, dir):
    new_x = pos[0] + dir[0]
    new_y = pos[1] + dir[1]
    if maze[new_y][new_x] == 0:
        return [new_x, new_y]
    return pos

running = True
while running:
    screen.fill(BLACK)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.VIDEORESIZE:
            WIDTH, HEIGHT = event.w, event.h
            CELL_SIZE = min(WIDTH // GRID_WIDTH, HEIGHT // GRID_HEIGHT)
            screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.RESIZABLE)
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                player_dir = [-1, 0]
            if event.key == pygame.K_RIGHT:
                player_dir = [1, 0]
            if event.key == pygame.K_UP:
                player_dir = [0, -1]
            if event.key == pygame.K_DOWN:
                player_dir = [0, 1]

    # Move player
    player_pos = move_entity(player_pos, player_dir)

    # Eat pellets
    if player_pos in pellets:
        pellets.remove(player_pos)
        score += 10

    # Move ghosts randomly
    for idx, g in enumerate(ghosts):
        if random.randint(0, 100) < 10:
            ghost_dir[idx] = random.choice([[-1,0],[1,0],[0,-1],[0,1]])
        ghosts[idx] = move_entity(g, ghost_dir[idx])

    # Collision with ghosts
    for g in ghosts:
        if player_pos == g:
            running = False

    # Win condition
    if not pellets:
        running = False

    # Draw maze
    for y in range(GRID_HEIGHT):
        for x in range(GRID_WIDTH):
            if maze[y][x] == 1:
                pygame.draw.rect(screen, WALL_COLOR, (x*CELL_SIZE, y*CELL_SIZE, CELL_SIZE, CELL_SIZE))

    # Draw pellets
    for p in pellets:
        pygame.draw.circle(screen, PELLET_COLOR, (p[0]*CELL_SIZE+CELL_SIZE//2, p[1]*CELL_SIZE+CELL_SIZE//2), CELL_SIZE//6)

    # Draw player
    pygame.draw.circle(screen, PACMAN_COLOR, (player_pos[0]*CELL_SIZE+CELL_SIZE//2, player_pos[1]*CELL_SIZE+CELL_SIZE//2), CELL_SIZE//2-2)

    # Draw ghosts
    for g in ghosts:
        pygame.draw.circle(screen, GHOST_COLOR, (g[0]*CELL_SIZE+CELL_SIZE//2, g[1]*CELL_SIZE+CELL_SIZE//2), CELL_SIZE//2-2)

    # Draw score
    score_surface = font.render(f"Score: {score}", True, (255, 255, 255))
    screen.blit(score_surface, (10, 10))

    pygame.display.update()
    clock.tick(10)

pygame.quit()
sys.exit()
