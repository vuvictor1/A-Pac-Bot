# ============================================================================
# Authors: Victor Vu, Cristian Gomez, Alexander Hermenegildo & Jesus Fierro
# File: pacbot.py
# Description: This file contains the main game loop and logic for the game.
# ============================================================================
import pygame
import heapq
import random
from collections import deque

pygame.init()  # initializes all imported pygame modules
pygame.font.init()  # initializes the font module

# ==== Initialize Game settings ===========================================================
#
# =================================================================================================

# Set font for text and timer
font = pygame.font.SysFont("Arial", 36)  # font object for rendering text
metrics_font = pygame.font.SysFont("Arial", 20) # smaller font for the timer

steps_taken = 0 # initialize the steps counter for Pacman
food_eaten = 0  # initialize the counter for food pellets eaten

# Menu
MENU = True
selected_level = 0  # 0 = Beginner, 1 = Intermediate, 2 = Advanced
levels = ["Beginner Ghost - DFS", "Intermediate Ghost - BFS", "Advanced Ghost - A*"]
selected_bot = 0
algorithm = ["A*", "BFS", "DFS"]

# Game duration
game_duration = 60

# Screen dimensions
WIDTH, HEIGHT = 800, 600  # Updated dimensions
TILE_SIZE = 20

# Reserve a metrics area at the bottom of the screen
METRICS_HEIGHT = 50  # Height of the metrics area

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
YELLOW = (255, 255, 0)
RED = (255, 102, 102)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)
DARK_GRAY = (50, 50, 50)

screen = pygame.display.set_mode(  # creates a window of the specified size
    (WIDTH, HEIGHT)
)
pygame.display.set_caption("Pac-Bot A* Search")  # sets the window title
clock = pygame.time.Clock()  # clock object to control the frame rate

# Create a grid/map size
ROWS, COLS = (HEIGHT - METRICS_HEIGHT) // TILE_SIZE, WIDTH // TILE_SIZE
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

center_row = ROWS // 2
center_col = COLS // 2
ghost_box = [ # Central ghost box with exits
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
        ):  # ensure food is not in a wall or duplicate
            food.append(pos)
    return food

enemies = [ # Update the enemies list to spawn in the center box
    [center_row - 2, center_col],
    [center_row + 2, center_col],
    [center_row, center_col - 2],
    [center_row, center_col + 2],
]

DIRECTIONS = [(0, 1), (1, 0), (0, -1), (-1, 0)]  # directions: right, down, left, up

# Define additional path costs for tiles adjacent to some pellets
additional_costs = {}

def update_costs_based_on_ghosts(): # Update path costs based only on proximity to ghosts
    global additional_costs
    additional_costs = {}  # Reset additional costs

    for row in range(ROWS):
        for col in range(COLS):
            if [row, col] not in walls:  # Skip walls
                # Calculate the minimum distance to any ghost
                min_distance = min(
                    abs(row - ghost[0]) + abs(col - ghost[1]) for ghost in enemies
                )
                # Assign a cost inversely proportional to the distance
                # Closer to ghosts = higher cost
                if min_distance <= 3:  # Example: within 3 tiles of a ghost
                    additional_costs[(row, col)] = 10 - min_distance  # Cost: 9, 8, 7

def update_costs_based_on_ghosts_and_food(food): # Update path costs based on proximity to ghosts and food
    global additional_costs
    new_costs = {}  # Temporary dictionary to calculate new costs

    # Add costs based on ghost proximity
    for row in range(ROWS):
        for col in range(COLS):
            if [row, col] not in walls:  # Skip walls
                # Calculate the minimum distance to any ghost
                min_distance = min(
                    abs(row - ghost[0]) + abs(col - ghost[1]) for ghost in enemies
                )
                # Assign a cost inversely proportional to the distance
                # Closer to ghosts = higher cost
                if min_distance <= 3:  # Example: within 3 tiles of a ghost
                    new_costs[(row, col)] = max(1, 10 - min_distance)

    additional_costs = new_costs  # Update the global additional costs

# ==== Search Algorithms ==========================================================================
#
# =================================================================================================

# Calculate the heuristic
def heuristic(a, b):  # Calculate the Manhattan distance between two points
    return abs(a[0] - b[0]) + abs(a[1] - b[1])

# A* search algorithm to find the shortest path from start to goal
def a_star_search(
    start, goal
):  
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
                # Calculate the additional cost for the neighbor
                additional_cost = additional_costs.get(neighbor, 0)
                tentative_g_score = g_score[current] + 1 + additional_cost

                if neighbor not in g_score or tentative_g_score < g_score[neighbor]:
                    came_from[neighbor] = current
                    g_score[neighbor] = tentative_g_score
                    f_score[neighbor] = tentative_g_score + heuristic(neighbor, goal)
                    heapq.heappush(open_set, (f_score[neighbor], neighbor))
    return []

def dfs(start, goal): # DFS algo lvl0 to find a path from start to goal
    stack = [tuple(start)]  # starting point on the stack
    came_from = {tuple(start): None}  # tracking the path
    
    while stack:
        current = stack.pop()  # get the most recently added node (LIFO)
        
        if current == tuple(goal):
            path = []
            while current:
                path.append(list(current))
                current = came_from[current]
            path.reverse()
            return path[1:]  # return the path skipping the starting point
        
        # Randomize directions to make ghost movement less predictable
        directions_copy = DIRECTIONS.copy()
        random.shuffle(directions_copy)
        
        for d in directions_copy: # Move in all directions
            neighbor = (current[0] + d[0], current[1] + d[1])
            
            if (
                0 <= neighbor[0] < ROWS
                and 0 <= neighbor[1] < COLS
                and list(neighbor) not in walls
                and neighbor not in came_from
            ):
                came_from[neighbor] = current
                stack.append(neighbor)
    
    return []  # no path found

def bfs(start, goal): # BFS algorithm lvl1 to find the shortest path from start to goal
    queue = deque([tuple(start)])     #starting point in the queue
    came_from = {tuple(start): None}  # Keeping track

    while queue:
        current = queue.popleft() # get the next place to check

        if current == tuple(goal):  
            path = []               #storing the path taken
            while current:
                path.append(list(current))      # adding each step to opath
                current = came_from[current]    # move to previous step
            path.reverse()                      # put path in the right order
            return path[1:]                     # return path skipping the starting point

        for d in DIRECTIONS: # Move in all directions
            neighbor = (current[0] + d[0], current[1] + d[1])

            if (
                0 <= neighbor[0] < ROWS             
                and 0 <= neighbor[1] < COLS        # ensure it's inside, grid both col and row
                and list(neighbor) not in walls # ensure it's not a wall
                and neighbor not in came_from   
            ):
                came_from[neighbor] = current
                queue.append(neighbor)
    return []  # no path found

# ==== Drawing and Visualization ==========================================================
#
# =========================================================================================
def draw_grid():  # Draw the grid with walls and additional cost tiles
    for row in range(ROWS):
        for col in range(COLS):
            rect = pygame.Rect(col * TILE_SIZE, row * TILE_SIZE, TILE_SIZE, TILE_SIZE)
            if [row, col] in walls:
                pygame.draw.rect(  # Draw walls as dark gray rectangles
                    screen, DARK_GRAY, rect
                )
            elif [row, col] in enemies:  # Skip drawing tiles over ghosts
                continue
            elif (row, col) in additional_costs:  # Highlight tiles with additional costs
                cost = additional_costs[(row, col)]
                # Create a transparent surface for the tile
                tile_surface = pygame.Surface((TILE_SIZE, TILE_SIZE), pygame.SRCALPHA)
                # Assign colors based on cost
                if cost == 9:  # High cost (dangerous, adjacent to ghosts)
                    color = (255, 102, 102, 100)  # Light red with transparency
                elif cost == 8:  # Moderate cost (2 tiles away from ghosts)
                    color = (255, 255, 102, 100)  # Light yellow with transparency
                elif cost == 7:  # Low cost (3 tiles away from ghosts)
                    color = (102, 255, 102, 100)  # Light green with transparency
                tile_surface.fill(color)  # Fill the surface with the transparent color
                screen.blit(tile_surface, rect.topleft)  # Blit the surface onto the screen
            else:
                pygame.draw.rect(screen, BLUE, rect, 1)  # Draw grid lines in blue

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

def draw_timer():  # Function to draw the timer and time remaining on the screen
    elapsed_time = (pygame.time.get_ticks() - start_time) // 1000  # convert to seconds
    remaining_time = max(0, game_duration - elapsed_time)  # calculate remaining time
    timer_text = metrics_font.render(f"Time: {elapsed_time}s", True, WHITE)
    remaining_text = metrics_font.render(f"Time Remaining: {remaining_time}s", True, WHITE)
    screen.blit(timer_text, (20, HEIGHT - METRICS_HEIGHT + 10))  # display timer in metrics area
    screen.blit(remaining_text, (250, HEIGHT - METRICS_HEIGHT + 10))  # display remaining time

def draw_food_eaten():  # Function to display the number of food pellets eaten
    food_text = metrics_font.render(f"Food Eaten: {food_eaten}", True, WHITE)
    screen.blit(food_text, (500, HEIGHT - METRICS_HEIGHT + 10))  # display in metrics area

def draw_steps_taken():  # Function to display the number of steps Pacman has taken
    steps_text = metrics_font.render(f"Steps Taken: {steps_taken}", True, WHITE)
    screen.blit(steps_text, (20, HEIGHT - METRICS_HEIGHT + 10))  # display in metrics area

def draw_metrics():  # Function to display both steps taken and time remaining
    global steps_taken
    elapsed_time = (pygame.time.get_ticks() - start_time) // 1000  # convert to seconds
    remaining_time = max(0, game_duration - elapsed_time)  # calculate remaining time

    # Render steps taken
    steps_text = metrics_font.render(f"Steps Taken: {steps_taken}", True, WHITE)
    screen.blit(steps_text, (20, HEIGHT - METRICS_HEIGHT + 10))  # display steps in metrics area

    # Render time remaining
    time_text = metrics_font.render(f"Time Remaining: {remaining_time}s", True, WHITE)
    screen.blit(time_text, (250, HEIGHT - METRICS_HEIGHT + 10))  # display time in metrics area
    
    # Render food eaten
    food_text = metrics_font.render(f"Food Eaten: {food_eaten}", True, WHITE)
    screen.blit(food_text, (500, HEIGHT - METRICS_HEIGHT + 10))  # display in metrics area
    
    # Render algorithm info to the right of food eaten
    algo_text = metrics_font.render(f"Pacman: {algorithm[selected_bot]}", True, YELLOW)
    screen.blit(algo_text, (650, HEIGHT - METRICS_HEIGHT + 10))  # aligned with other metrics

def draw_menu(): # Draw the menu for selecting levels
    screen.fill(BLACK)
    title_font = pygame.font.SysFont("Arial", 48)
    option_font = pygame.font.SysFont("Arial", 32)
    title = title_font.render("PAC-BOT - A*", True, YELLOW) 
    screen.blit(title, (WIDTH // 2 - title.get_width() // 2, 50)) 

    for i, level_name in enumerate(levels): # Display level names
        color = GREEN if i == selected_level else WHITE
        text = option_font.render(f"Level {i}: {level_name}", True, color)
        screen.blit(text, (WIDTH // 2 - text.get_width() // 2, 150 + i * 90))

    prompt = metrics_font.render("Use: Up/Down Arrows to choose Lvl. Enter to start.", True, WHITE)
    screen.blit(prompt, (WIDTH // 2 - prompt.get_width() // 2, HEIGHT - 180)) 
    prompt2 = metrics_font.render("Left/Right Arrows to choose Pac-bot AI.", True, WHITE)
    screen.blit(prompt2, (WIDTH // 2 - prompt2.get_width() // 2, HEIGHT - 140)) 

    # Added to make it more clear which algorithm Pacman is using
    pac_algo_text = metrics_font.render(f"Pacman will use {algorithm[selected_bot]} algorithm", True, YELLOW)
    screen.blit(pac_algo_text, (WIDTH // 2 - pac_algo_text.get_width() // 2, HEIGHT - 100))
    algo_label = option_font.render("Pac-Bot AI: " + algorithm[selected_bot], True, RED)
    screen.blit(algo_label, (WIDTH // 2 - algo_label.get_width() // 2, 100))
    pygame.display.flip() # update the display

# ==== Movement/Collision logic ===================================================================
#
# =================================================================================================
def move_pacman_with_a_star(target):  # Move Pacman using A* to reach the target
    global steps_taken
    path = a_star_search(pacman_pos, target)
    if path:
        pacman_pos[0], pacman_pos[1] = path[0]  # move to the next position in the path
        steps_taken += 1  # increment the steps counter

def move_pacman_with_algorithm(target): # Move Pacman using the selected algorithm
    global steps_taken
    if selected_bot == 0:  # A*
        path = a_star_search(pacman_pos, target)
    elif selected_bot == 1:  # BFS
        path = bfs(pacman_pos, target)
    elif selected_bot == 2:  # DFS
        path = dfs(pacman_pos, target)
    
    if path:
        pacman_pos[0], pacman_pos[1] = path[0]  # move to the next position in the path
        steps_taken += 1  # increment the steps counter

def move_enemy_with_bfs(enemy, target):  # Move a single enemy using BFS
    path = bfs(enemy, target)
    if path:
        return path[0]  # return the next position in the path
    return enemy  # if no path is found, stay in the same position

def move_enemy_with_dfs(enemy, target):  # Move a single enemy using DFS
    path = dfs(enemy, target)
    if path:
        return path[0]  # return the next position in the path
    return enemy  # if no path is found, stay in the same position

def move_enemy_with_a_star(enemy, target):  # Move a single enemy using A*
    path = a_star_search(enemy, target)
    if path:
        return path[0]  # return the next position in the path
    return enemy  # if no path is found, stay in the same position

def check_collision_with_enemies(): # Check for collision with enemies
    for enemy in enemies:
        if pacman_pos[0] == enemy[0] and pacman_pos[1] == enemy[1]: # Check if pacman and enemy are in the same position
            return True  # Collision detected
    return False  # No collision

def move_enemies():  # Move enemies based on the selected level
    for i, enemy in enumerate(enemies): 
        if selected_level == 0:  # Beginner: DFS
            new_pos = move_enemy_with_dfs(enemy, pacman_pos)
            enemies[i] = [new_pos[0], new_pos[1]]
        elif selected_level == 1:  # Intermediate: BFS
            new_pos = move_enemy_with_bfs(enemy, pacman_pos)
            enemies[i] = [new_pos[0], new_pos[1]]
        elif selected_level == 2:  # Advanced: A*
            new_pos = move_enemy_with_a_star(enemy, pacman_pos)
            enemies[i] = [new_pos[0], new_pos[1]]

def show_game_over():  # Show game over screen
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

    waiting = True
    while waiting: # Wait for the user to press ESC or close the game
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                pygame.quit()
                exit()

start_time = pygame.time.get_ticks() # intialize the start time

# ==== Main Game Loop =============================================================================
#
# =================================================================================================
if __name__ == "__main__":
    running = True

    while MENU:
        draw_menu()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    selected_level = (selected_level - 1) % len(levels)
                if event.key == pygame.K_DOWN:
                    selected_level = (selected_level + 1) % len(levels)
                if event.key == pygame.K_RETURN:
                    MENU = False
                if event.key == pygame.K_LEFT:
                    selected_bot = (selected_bot - 1) % len(algorithm)
                if event.key == pygame.K_RIGHT:
                    selected_bot = (selected_bot + 1) % len(algorithm)

    # Initialize food after the menu loop
    food_count = 3
    food = generate_food(food_count)

    while running:
        screen.fill(BLACK)
        draw_grid()
        draw_pacman()
        draw_food()
        draw_enemies()
        draw_metrics()
        draw_food_eaten()

        # Update costs based on ghost proximity
        update_costs_based_on_ghosts_and_food(food)

        if food:
            move_pacman_with_algorithm(food[0])
        move_enemies()

        if check_collision_with_enemies():
            show_game_over()
            running = False

        for powerup in food[:]:
            if pacman_pos == powerup:
                food.remove(powerup)
                food_eaten += 1

        if not food:
            food = generate_food(food_count)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        pygame.display.flip()
        clock.tick(5)
        elapsed_time = (pygame.time.get_ticks() - start_time) // 1000
        if elapsed_time > game_duration:
            show_game_over()
            running = False

    pygame.quit()
