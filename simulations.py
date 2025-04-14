# File: simulations.py
# Description: This file contains the simulation logic for the Pac-Bot game.
import csv
import pygame
import memory_tracker
from pacbot import (
    pacman_pos,
    generate_food,
    update_costs_based_on_ghosts_and_food,
    bfs,
    dfs,
    a_star_search,
    ROWS,
    COLS,
    algorithm,
    levels,
    center_row,
    center_col,
    game_duration,
)

pygame.display.set_mode((1, 1))


def simulation(pac_algo_index, ghost_algo_index, simulation_runs=50):
    results = []

    for run in range(simulation_runs):
        pacman_pos[:] = [1, 1]
        steps_taken = 0
        food_eaten = 0
        food = generate_food(3)
        update_costs_based_on_ghosts_and_food(food)

        enemies = [
            [center_row - 2, center_col],
            [center_row + 2, center_col],
            [center_row, center_col - 2],
            [center_row, center_col + 2],
        ]

        memory_tracker.start_tracking()
        start_time = pygame.time.get_ticks()
        ghost_move_counter = 0
        ghost_move_delay = 3
        elapsed_time = 0
        game_over = False

        while not game_over:
            # Move Pacman
            if food:
                if pac_algo_index == 0:
                    path = a_star_search(pacman_pos, food[0])
                elif pac_algo_index == 1:
                    path = bfs(pacman_pos, food[0])
                elif pac_algo_index == 2:
                    path = dfs(pacman_pos, food[0])
                if path:
                    pacman_pos[0], pacman_pos[1] = path[0]
                    steps_taken += 1
            

            # Move Ghosts
            ghost_move_counter += 1
            if ghost_move_counter >= ghost_move_delay:
                for i, enemy in enumerate(enemies):
                    if ghost_algo_index == 0:
                        path = dfs(enemy, pacman_pos)
                    elif ghost_algo_index == 1:
                        path = bfs(enemy, pacman_pos)
                    elif ghost_algo_index == 2:
                        path = a_star_search(enemy, pacman_pos)
                    if path:
                        enemies[i] = path[0]
                ghost_move_counter = 0

            # Check collision
            for enemy in enemies:
                if pacman_pos == enemy:
                    game_over = True

            # Check food collection
            for f in food[:]:
                if pacman_pos == f:
                    food.remove(f)
                    food_eaten += 1
                    update_costs_based_on_ghosts_and_food(food)

            # Respawn food
            if not food:
                food = generate_food(3)
                update_costs_based_on_ghosts_and_food(food)

            # Time check
            elapsed_time = (pygame.time.get_ticks() - start_time) // 1000
            if elapsed_time >= game_duration:
                game_over = True
        
        current_memory, peak_memory = memory_tracker.get_memory_usage()
        memory_tracker.stop_tracking()

        results.append(
            {
                "Pac-Bot AI": algorithm[pac_algo_index],
                "Ghost AI": levels[ghost_algo_index].split(" - ")[-1],
                "Steps Taken": steps_taken,
                "Food Eaten": food_eaten,
                "Time Survived": elapsed_time,
                "RAM (KB)": current_memory,
                "Peak RAM (KB)": peak_memory
            }
        )

    return results


if __name__ == "__main__":
    all_results = []
    print(
        "Running 50 simulations for each Pac-Bot algorithm vs Ghost AI combinations..."
    )

    for pac in range(3):
        for ghost in range(3):
            combo_name = f"{algorithm[pac]} vs {levels[ghost].split(' - ')[-1]}"
            print(f"> Simulating {combo_name}...")
            sim_results = simulation(pac, ghost, simulation_runs=50)
            all_results.extend(sim_results)

    # Save the output to a file
    with open("Results.csv", "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=all_results[0].keys())
        writer.writeheader()
        writer.writerows(all_results)

    print("✅ Simulation complete. Results saved to Results.csv")
