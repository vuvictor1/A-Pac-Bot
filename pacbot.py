# Authors: Victor Vu, Christian Gomez, Alexander Hermenegildo & Jesus Fierro
# File: pacbot.py
# Description: This file contains the main game loop and logic for the game.
import pygame
import heapq
import random

# Initialize pygame
pygame.init()

# Add this line to initialize fonts
pygame.font.init()

# Screen dimensions
WIDTH, HEIGHT = 600, 400
TILE_SIZE = 20

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
YELLOW = (255, 255, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)
DARK_GRAY = (50, 50, 50)

# Initialize screen
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Pac-Man with A* Search")

# Clock for controlling frame rate
clock = pygame.time.Clock()

# Create a grid
ROWS, COLS = HEIGHT // TILE_SIZE, WIDTH // TILE_SIZE
grid = [[0 for _ in range(COLS)] for _ in range(ROWS)]

# Pac-Man and power-up positions
pacman_pos = [1, 1]
powerups = [[10, 15], [5, 8], [18, 25]]

# Add walls (list of [row, col] positions)
walls = [[3, 3], [3, 4], [3, 5], [10, 10], [10, 11], [10, 12]]

# Add enemies (list of [row, col] positions)
enemies = [[15, 15], [8, 8]]

# Directions for movement
DIRECTIONS = [(0, 1), (1, 0), (0, -1), (-1, 0)]

# Define a font and size
font = pygame.font.SysFont("Arial", 36)

def heuristic(a, b):
    """Heuristic function for A* (Manhattan distance)."""
    return abs(a[0] - b[0]) + abs(a[1] - b[1])


def a_star_search(start, goal):
    """A* search algorithm."""
    open_set = []
    heapq.heappush(open_set, (0, tuple(start)))  # Convert start to tuple
    came_from = {}
    g_score = {tuple(start): 0}  # Convert start to tuple
    f_score = {tuple(start): heuristic(start, goal)}  # Convert start to tuple

    while open_set:
        _, current = heapq.heappop(open_set)

        if current == tuple(goal):  # Convert goal to tuple
            path = []
            while current in came_from:
                path.append(list(current))  # Convert tuple back to list for path
                current = came_from[current]
            path.reverse()
            return path

        for direction in DIRECTIONS:
            neighbor = (current[0] + direction[0], current[1] + direction[1])  # Use tuple

            if 0 <= neighbor[0] < ROWS and 0 <= neighbor[1] < COLS and list(neighbor) not in walls:
                tentative_g_score = g_score[current] + 1

                if neighbor not in g_score or tentative_g_score < g_score[neighbor]:
                    came_from[neighbor] = current
                    g_score[neighbor] = tentative_g_score
                    f_score[neighbor] = tentative_g_score + heuristic(neighbor, goal)
                    heapq.heappush(open_set, (f_score[neighbor], neighbor))

    return []


def draw_grid():
    """Draw the grid with walls."""
    for row in range(ROWS):
        for col in range(COLS):
            rect = pygame.Rect(col * TILE_SIZE, row * TILE_SIZE, TILE_SIZE, TILE_SIZE)
            if [row, col] in walls:
                pygame.draw.rect(screen, DARK_GRAY, rect)  # Draw walls as dark gray rectangles
            else:
                pygame.draw.rect(screen, BLUE, rect, 1)  # Draw grid lines in blue


def draw_pacman():
    """Draw Pac-Man."""
    pygame.draw.circle(
        screen,
        YELLOW,
        (pacman_pos[1] * TILE_SIZE + TILE_SIZE // 2, pacman_pos[0] * TILE_SIZE + TILE_SIZE // 2),
        TILE_SIZE // 2,
    )


def draw_powerups():
    """Draw power-ups."""
    for powerup in powerups:
        pygame.draw.circle(
            screen,
            GREEN,
            (powerup[1] * TILE_SIZE + TILE_SIZE // 2, powerup[0] * TILE_SIZE + TILE_SIZE // 2),
            TILE_SIZE // 4,
        )


def draw_enemies():
    """Draw enemies."""
    for enemy in enemies:
        pygame.draw.circle(
            screen,
            RED,
            (enemy[1] * TILE_SIZE + TILE_SIZE // 2, enemy[0] * TILE_SIZE + TILE_SIZE // 2),
            TILE_SIZE // 2,
        )


def move_pacman_randomly():
    """Move Pac-Man randomly."""
    possible_moves = [
        (pacman_pos[0] + d[0], pacman_pos[1] + d[1]) for d in DIRECTIONS
        if 0 <= pacman_pos[0] + d[0] < ROWS and 0 <= pacman_pos[1] + d[1] < COLS and [pacman_pos[0] + d[0], pacman_pos[1] + d[1]] not in walls
    ]
    if possible_moves:
        new_pos = random.choice(possible_moves)
        pacman_pos[0], pacman_pos[1] = new_pos[0], new_pos[1]


def move_enemies_with_a_star():
    """Move enemies using A* to chase Pac-Man."""
    for i, enemy in enumerate(enemies):
        path = a_star_search(enemy, pacman_pos)
        if path:
            enemies[i] = path[0]  # Move to the next position in the path


def show_game_over():
    """Display 'Game Over' message on the screen."""
    # Fill the screen with a semi-transparent overlay
    overlay = pygame.Surface((WIDTH, HEIGHT))
    overlay.set_alpha(200)  # Set transparency
    overlay.fill(BLACK)
    screen.blit(overlay, (0, 0))

    # Render the "Game Over" text
    text = font.render("GAME OVER", True, RED)
    text_rect = text.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 20))
    screen.blit(text, text_rect)

    # Render a smaller message below
    subtext = pygame.font.SysFont("Arial", 24).render("Press ESC to Quit", True, WHITE)
    subtext_rect = subtext.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 20))
    screen.blit(subtext, subtext_rect)

    pygame.display.flip()

    # Wait for the user to press ESC or close the game
    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                pygame.quit()
                exit()


# Main game loop
running = True
while running:
    screen.fill(BLACK)
    draw_grid()
    draw_pacman()
    draw_powerups()
    draw_enemies()

    move_pacman_randomly()
    move_enemies_with_a_star()

    # Check for collision with enemies
    if pacman_pos in enemies:
        show_game_over()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    pygame.display.flip()
    clock.tick(5)

pygame.quit()