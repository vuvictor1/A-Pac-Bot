# Authors: Victor Vu, Christian Gomez, Alexander Hermenegildo & Jesus Fierro
# File: pacbot.py
# Description: This file contains the main game loop and logic for the game.
import pygame
import heapq
import random

pygame.init()  # initializes all imported pygame modules
pygame.font.init()  # initializes the font module

#Menu
MENU = True
selected_level = 0  # 0 = Beginner, 1 = Intermediate, 2 = Advanced
levels = ["Beginner", "Intermediate", "Advanced"]

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
walls = [] # list to store wall positions

for col in range(COLS): # Border walls
    walls.append([0, col])
    walls.append([ROWS - 1, col])
for row in range(ROWS):
    walls.append([row, 0])
    walls.append([row, COLS - 1])

for row in range(2, ROWS - 2): # Vertical corridors
    if row % 4 != 0:
        walls.append([row, COLS // 4])
        walls.append([row, COLS // 2])
        walls.append([row, 3 * COLS // 4])

for col in range(2, COLS - 2): # Horizontal corridors
    if col % 5 != 0:
        walls.append([ROWS // 4, col])
        walls.append([ROWS // 2, col])
        walls.append([3 * ROWS // 4, col])

# Central ghost box with exits
center_row = ROWS // 2
center_col = COLS // 2
ghost_box = [
    [center_row - 1, center_col - 1], [center_row - 1, center_col],
    [center_row + 1, center_col - 1], [center_row + 1, center_col],
    [center_row, center_col + 1], [center_row, center_col - 1]
]
walls += ghost_box # add ghost box to walls

for row in range(5, ROWS - 5): # Add barriers to the left and right sides
    if row % 6 == 0:
        walls.append([row, 2])
        walls.append([row, COLS - 3])


def generate_food(num_food):  # Generate food in valid positions
    food = []
    while len(food) < num_food:
        pos = [random.randint(0, ROWS - 1), random.randint(0, COLS - 1)]
        if (
            pos not in walls and pos not in food
        ):  # ensure power-up is not in a wall or duplicate
            food.append(pos)
    return food


enemies = [ # Update the enemies list to spawn in the center box
    [center_row - 2, center_col],
    [center_row + 2, center_col],
    [center_row, center_col - 2],
    [center_row, center_col + 2],
]

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


def draw_food():  # Draw food
    for powerup in food:
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


def move_pacman_with_a_star(target):  # Move Pacman using A* to reach the target
    path = a_star_search(pacman_pos, target)
    if path:
        pacman_pos[0], pacman_pos[1] = path[0]  # move to the next position in the path


def move_enemies_randomly():  # Move enemies randomly
    for i, enemy in enumerate(enemies):
        possible_moves = [
            (enemy[0] + d[0], enemy[1] + d[1])
            for d in DIRECTIONS
            if 0 <= enemy[0] + d[0] < ROWS
            and 0 <= enemy[1] + d[1] < COLS
            and [enemy[0] + d[0], enemy[1] + d[1]] not in walls
        ]
        if possible_moves:
            new_pos = random.choice(possible_moves)
            enemies[i] = [new_pos[0], new_pos[1]]


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


start_time = pygame.time.get_ticks() # intialize the start time
metrics_font = pygame.font.SysFont("Arial", 20) # smaller font for the timer

def draw_timer():  # Function to draw the timer and time remaining on the screen
    elapsed_time = (pygame.time.get_ticks() - start_time) // 1000  # convert to seconds
    remaining_time = max(0, game_duration - elapsed_time)  # calculate remaining time
    timer_text = metrics_font.render(f"Time: {elapsed_time}s", True, WHITE)
    remaining_text = metrics_font.render(f"Time Remaining: {remaining_time}s", True, WHITE)
    screen.blit(timer_text, (20, HEIGHT - 21))  # display timer at the bottom left
    screen.blit(remaining_text, (250, HEIGHT - 21))  # display remaining time to the right of food eaten

food_eaten = 0  # initialize the counter for food pellets eaten

def draw_food_eaten():  # Function to display the number of food pellets eaten
    food_text = metrics_font.render(f"Food Eaten: {food_eaten}", True, WHITE)
    screen.blit(food_text, (115, HEIGHT - 21))  # display right of timer

def draw_menu(): # Draw the menu for selecting levels
    screen.fill(BLACK)
    title_font = pygame.font.SysFont("Arial", 48)
    option_font = pygame.font.SysFont("Arial", 32)

    title = title_font.render("PAC-BOT", True, YELLOW) 
    screen.blit(title, (WIDTH // 2 - title.get_width() // 2, 50)) 

    for i, level_name in enumerate(levels): # Display level names
        color = GREEN if i == selected_level else WHITE
        text = option_font.render(f"Level {i + 1}: {level_name}", True, color)
        screen.blit(text, (WIDTH // 2 - text.get_width() // 2, 150 + i * 50))

    prompt = metrics_font.render("Use Up/Down Arrows to choose, Enter to start", True, WHITE)
    screen.blit(prompt, (WIDTH // 2 - prompt.get_width() // 2, HEIGHT - 40)) 

    pygame.display.flip() # update the display


# Main game loop
running = True
game_duration = 60

while MENU:  # Menu loop
    draw_menu()
    for event in pygame.event.get():  # Check for events
        if event.type == pygame.QUIT:  # Close the game
            pygame.quit()
            exit()
        if event.type == pygame.KEYDOWN:  # Check for key presses
            if event.key == pygame.K_UP:
                selected_level = (selected_level - 1) % len(levels)
            if event.key == pygame.K_DOWN:
                selected_level = (selected_level + 1) % len(levels)
            if event.key == pygame.K_RETURN:
                MENU = False  # exit menu and start the game

# Initialize food after the menu loop
if selected_level == 0:  # Beginner
    ghost_speed = 1
    food_count = 2
elif selected_level == 1:  # Intermediate
    ghost_speed = 2
    food_count = 3
else:  # Advanced
    ghost_speed = 3
    food_count = 4

food = generate_food(food_count)  # Generate initial food based on the selected level

while running:  # Main game loop
    screen.fill(BLACK)
    draw_grid()
    draw_pacman()
    draw_food()
    draw_enemies()
    draw_timer()  # draw the timer
    draw_food_eaten()  # draw the food eaten counter

    if food:  # Move Pacman toward the first power-up (or any target)
        move_pacman_with_a_star(food[0])  # pacman targets the first power-up

    move_enemies_randomly()  # ghosts move randomly

    if pacman_pos in enemies:  # Check for collision with enemies
        show_game_over()

    for powerup in food[:]:  # Check for collision with food
        if pacman_pos == powerup:
            food.remove(powerup)  # remove the power-up if Pacman collects it
            food_eaten += 1  # increment the food eaten counter

    if not food:  # Check if all food pellets are eaten
        food = generate_food(food_count)  # Respawn food based on the selected level

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    pygame.display.flip()  # update the display
    clock.tick(5)  # set the frame rate to 5 FPS to slow down the game
    elapsed_time = (pygame.time.get_ticks() - start_time) // 1000
    if elapsed_time > game_duration:  # Check if the game duration is over 60s
        show_game_over()  # show the game over screen
        running = False  # exit the main game loop

pygame.quit()