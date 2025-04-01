# Authors: Victor Vu, Christian Gomez, Alexander Hermenegildo & Jesus Fierro
# File: pacbot.py
# Description: This file contains the main game loop and logic for the game.
import pygame
import heapq
import random

pygame.init()  # initializes all imported pygame modules
pygame.font.init()  # initializes the font module

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

screen = pygame.display.set_mode(  # creates a window of the specified size
    (WIDTH, HEIGHT)
)

pygame.display.set_caption("Pac-Bot A* Search")  # sets the window title
clock = pygame.time.Clock()  # clock object to control the frame rate

# Create a grid
ROWS, COLS = HEIGHT // TILE_SIZE, WIDTH // TILE_SIZE
grid = [[0 for _ in range(COLS)] for _ in range(ROWS)]
pacman_pos = [1, 1]  # pacman position

walls = [  # Define walls
    [2, 2], [2, 3], [2, 4], [2, 5], [2, 6], [3, 6], [4, 6], [5, 6], [6, 6],
    [6, 5], [6, 4], [6, 3], [6, 2], [8, 2], [8, 3], [8, 4], [8, 5], [8, 6],
    [9, 6], [10, 6], [11, 6], [12, 6], [12, 5], [12, 4], [12, 3], [12, 2],
    [14, 2], [14, 3], [14, 4], [14, 5], [14, 6], [15, 6], [16, 6], [17, 6],
    [18, 6], [18, 8], [17, 8], [16, 8], [15, 8], [14, 8], [13, 8], [12, 8],
    [11, 8], [10, 8], [9, 8], [8, 8], [7, 8], [6, 8], [5, 8], [4, 8], [3, 8],
    [2, 8], [2, 10], [3, 10], [4, 10], [5, 10], [6, 10], [7, 10], [8, 10],
    [9, 10], [10, 10], [11, 10], [12, 10], [13, 10], [14, 10], [15, 10],
    [16, 10], [17, 10], [18, 10], [18, 12], [17, 12], [16, 12], [15, 12],
    [14, 12], [13, 12], [12, 12], [11, 12], [10, 12], [9, 12], [8, 12],
    [7, 12], [6, 12], [5, 12], [4, 12], [3, 12], [2, 12], [2, 14], [3, 14],
    [4, 14], [5, 14], [6, 14], [7, 14], [8, 14], [9, 14], [10, 14], [11, 14],
    [12, 14], [13, 14], [14, 14], [15, 14], [16, 14], [17, 14], [18, 14],
]


def generate_powerups(num_powerups):  # Generate power-ups in valid positions
    powerups = []
    while len(powerups) < num_powerups:
        pos = [random.randint(0, ROWS - 1), random.randint(0, COLS - 1)]
        if (
            pos not in walls and pos not in powerups
        ):  # ensure power-up is not in a wall or duplicate
            powerups.append(pos)
    return powerups


powerups = generate_powerups(3)  # generate 3 power-ups
enemies = [[15, 15], [8, 8]]  # enemy positions
DIRECTIONS = [(0, 1), (1, 0), (0, -1), (-1, 0)]  # directions: right, down, left, up
font = pygame.font.SysFont("Arial", 36)  # font object for rendering text


def heuristic(a, b):  # Calculate the Manhattan distance between two points
    return abs(a[0] - b[0]) + abs(a[1] - b[1])


def a_star_search(
    start, goal
):  # A* search algorithm to find the shortest path from start to goal
    open_set = []
    heapq.heappush(open_set, (0, tuple(start)))  # convert start to tuple
    came_from = {}
    g_score = {tuple(start): 0}  # convert start to tuple
    f_score = {tuple(start): heuristic(start, goal)}  # convert start to tuple

    while open_set:  # Pop the node with the lowest f_score
        _, current = heapq.heappop(open_set)

        if current == tuple(goal):  # Convert goal to tuple
            path = []
            while current in came_from:
                path.append(list(current))  # convert tuple back to list for path
                current = came_from[current]
            path.reverse()
            return path

        for direction in DIRECTIONS:  # Check all possible directions
            neighbor = (
                current[0] + direction[0],
                current[1] + direction[1],
            )  # use tuple

            if (  # Check if neighbor is within bounds and not a wall
                0 <= neighbor[0] < ROWS
                and 0 <= neighbor[1] < COLS
                and list(neighbor) not in walls
            ):
                tentative_g_score = g_score[current] + 1

                if neighbor not in g_score or tentative_g_score < g_score[neighbor]:
                    came_from[neighbor] = current
                    g_score[neighbor] = tentative_g_score
                    f_score[neighbor] = tentative_g_score + heuristic(neighbor, goal)
                    heapq.heappush(open_set, (f_score[neighbor], neighbor))

    return []


def draw_grid():  # Draw the grid with walls
    for row in range(ROWS):
        for col in range(COLS):
            rect = pygame.Rect(col * TILE_SIZE, row * TILE_SIZE, TILE_SIZE, TILE_SIZE)
            if [row, col] in walls:
                pygame.draw.rect(  # draw walls as dark gray rectangles
                    screen, DARK_GRAY, rect
                )
            else:
                pygame.draw.rect(screen, BLUE, rect, 1)  # draw grid lines in blue


def draw_pacman():  # Draw Pacman
    pygame.draw.circle(
        screen,
        YELLOW,
        (
            pacman_pos[1] * TILE_SIZE + TILE_SIZE // 2,
            pacman_pos[0] * TILE_SIZE + TILE_SIZE // 2,
        ),
        TILE_SIZE // 2,
    )


def draw_powerups():  # Draw power-ups
    for powerup in powerups:
        pygame.draw.circle(
            screen,
            GREEN,
            (
                powerup[1] * TILE_SIZE + TILE_SIZE // 2,
                powerup[0] * TILE_SIZE + TILE_SIZE // 2,
            ),
            TILE_SIZE // 4,
        )


def draw_enemies():  # Draw enemies
    for enemy in enemies:
        pygame.draw.circle(
            screen,
            RED,
            (
                enemy[1] * TILE_SIZE + TILE_SIZE // 2,
                enemy[0] * TILE_SIZE + TILE_SIZE // 2,
            ),
            TILE_SIZE // 2,
        )


def move_pacman_randomly():  # Move Pacman randomly
    possible_moves = [
        (pacman_pos[0] + d[0], pacman_pos[1] + d[1])
        for d in DIRECTIONS
        if 0 <= pacman_pos[0] + d[0] < ROWS
        and 0 <= pacman_pos[1] + d[1] < COLS
        and [pacman_pos[0] + d[0], pacman_pos[1] + d[1]] not in walls
    ]
    if possible_moves:
        new_pos = random.choice(possible_moves)
        pacman_pos[0], pacman_pos[1] = new_pos[0], new_pos[1]


def move_enemies_with_a_star():  # Move enemies using A* to chase Pacman
    for i, enemy in enumerate(enemies):
        path = a_star_search(enemy, pacman_pos)
        if path:
            enemies[i] = path[0]  # move to the next position in the path


def show_game_over():  # Show game over screen
    # Fill the screen with a semi-transparent overlay
    overlay = pygame.Surface((WIDTH, HEIGHT))
    overlay.set_alpha(200)  # set transparency
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

    pygame.display.flip()  # update the display

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

    if pacman_pos in enemies:  # Check for collision with enemies
        show_game_over()

    for event in pygame.event.get():  # Check for collision with power-ups
        if event.type == pygame.QUIT:
            running = False

    pygame.display.flip()
    clock.tick(5)  # set the frame rate to 5 FPS to slow down the game

pygame.quit()