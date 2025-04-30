# FIX AI

import pygame
import sys
import random

# Initialize
pygame.init()

# Screen setup
CELL_SIZE = 30
COLS = 10
ROWS = 20
WIDTH = COLS * CELL_SIZE
HEIGHT = ROWS * CELL_SIZE
screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.RESIZABLE)
pygame.display.set_caption("ColorStack - Tetris")

clock = pygame.time.Clock()

# Colors
BACKGROUND = (10, 10, 10)
GRID_COLOR = (40, 40, 40)
colors = [
    (0, 255, 255),
    (255, 255, 0),
    (128, 0, 128),
    (0, 255, 0),
    (255, 0, 0),
    (255, 165, 0),
    (0, 0, 255),
]

# Shapes
shapes = [
    [[1, 1, 1, 1]],
    [[1, 1], [1, 1]],
    [[0, 1, 0], [1, 1, 1]],
    [[1, 0, 0], [1, 1, 1]],
    [[0, 0, 1], [1, 1, 1]],
    [[1, 1, 0], [0, 1, 1]],
    [[0, 1, 1], [1, 1, 0]],
]

# Board
board = [[0 for _ in range(COLS)] for _ in range(ROWS)]

class Piece:
    def __init__(self, shape, color):
        self.shape = shape
        self.color = color
        self.x = COLS // 2 - len(shape[0]) // 2
        self.y = 0

    def rotate(self):
        self.shape = [list(row) for row in zip(*self.shape[::-1])]

def valid(piece, dx=0, dy=0):
    for y, row in enumerate(piece.shape):
        for x, cell in enumerate(row):
            if cell:
                new_x = piece.x + x + dx
                new_y = piece.y + y + dy
                if new_x < 0 or new_x >= COLS or new_y >= ROWS:
                    return False
                if new_y >= 0 and board[new_y][new_x]:
                    return False
    return True

def place(piece):
    for y, row in enumerate(piece.shape):
        for x, cell in enumerate(row):
            if cell:
                board[piece.y + y][piece.x + x] = piece.color

def clear_lines():
    lines_cleared = 0
    for i in range(ROWS-1, -1, -1):
        if 0 not in board[i]:
            del board[i]
            board.insert(0, [0 for _ in range(COLS)])
            lines_cleared += 1
    return lines_cleared

# New piece
current_piece = Piece(random.choice(shapes), random.choice(colors))
fall_time = 0
fall_speed = 500  # milliseconds
score = 0
font = pygame.font.SysFont('Arial', 30)

running = True
while running:
    dt = clock.tick(60)
    fall_time += dt

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.VIDEORESIZE:
            WIDTH, HEIGHT = event.w, event.h
            CELL_SIZE = min(WIDTH // COLS, HEIGHT // ROWS)
            screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.RESIZABLE)
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                if valid(current_piece, dx=-1):
                    current_piece.x -= 1
            if event.key == pygame.K_RIGHT:
                if valid(current_piece, dx=1):
                    current_piece.x += 1
            if event.key == pygame.K_DOWN:
                if valid(current_piece, dy=1):
                    current_piece.y += 1
            if event.key == pygame.K_UP:
                rotated = Piece([list(row) for row in zip(*current_piece.shape[::-1])], current_piece.color)
                rotated.x, rotated.y = current_piece.x, current_piece.y
                if valid(rotated):
                    current_piece.rotate()
            if event.key == pygame.K_SPACE:
                while valid(current_piece, dy=1):
                    current_piece.y += 1
                place(current_piece)
                score += clear_lines()
                current_piece = Piece(random.choice(shapes), random.choice(colors))
                if not valid(current_piece):
                    running = False

    if fall_time > fall_speed:
        fall_time = 0
        if valid(current_piece, dy=1):
            current_piece.y += 1
        else:
            place(current_piece)
            score += clear_lines()
            current_piece = Piece(random.choice(shapes), random.choice(colors))
            if not valid(current_piece):
                running = False

    # Draw
    screen.fill(BACKGROUND)

    # Draw board
    for y in range(ROWS):
        for x in range(COLS):
            if board[y][x]:
                pygame.draw.rect(screen, board[y][x],
                                 (x * CELL_SIZE, y * CELL_SIZE, CELL_SIZE - 2, CELL_SIZE - 2))

    # Draw current piece
    for y, row in enumerate(current_piece.shape):
        for x, cell in enumerate(row):
            if cell:
                pygame.draw.rect(screen, current_piece.color,
                                 ((current_piece.x + x) * CELL_SIZE, (current_piece.y + y) * CELL_SIZE, CELL_SIZE - 2, CELL_SIZE - 2))

    # Draw grid
    for x in range(COLS):
        pygame.draw.line(screen, GRID_COLOR, (x * CELL_SIZE, 0), (x * CELL_SIZE, HEIGHT))
    for y in range(ROWS):
        pygame.draw.line(screen, GRID_COLOR, (0, y * CELL_SIZE), (WIDTH, y * CELL_SIZE))

    # Draw score
    score_surface = font.render(f"Score: {score}", True, (255, 255, 255))
    screen.blit(score_surface, (10, 10))

    pygame.display.update()

pygame.quit()
sys.exit()
