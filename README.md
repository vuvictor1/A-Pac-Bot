# A* Pac-Bot

<div align="center">
  <img src="https://github.com/user-attachments/assets/8b4bec90-cd7a-48f6-bd48-e874c8b06198" alt="output" width="150"/>
</div>

## Overview
Pac-Bot AI is a game that explores AI navigation through a grid-based maze environment. Inspired by the classic Pac-Man, the game features a player-controlled Pac-Man searching for food while being chased by four ghost agents. The project incorporates a fully AI-controlled multi-agent system where entities use the A* Search algorithm for pathfinding, leveraging heuristics and path costs for efficiency. Path costs are adapted as a proximity system in A* for Pac-bot to avoid ghosts. Additionally, the project implements BFS and DFS algorithms to provide comparison metrics for evaluating performance and efficiency.

## Features
- **Search Algorithms**: Implements A*, BFS, and DFS for efficient pathfinding.
- **Multi-Agent System**: 1 Pac-Bot AI vs 4 Ghost AIs.
- **Multiple Levels**: Test different algorithm combinations.
- **Food System**: Randomly positioned respawnable food pellets in valid spaces.
- **Cost Proximity**: Path costs placed adjacent to ghosts, being costly for A* Pac-bot pathfind near it.
- **Performance Metrics**: Evaluates steps taken, time, food consumed and ram usage.
- **Game Simulator**: Simulate 50 games per AI matchup for metrics collection. 

## Interaction: How to Play
1. **Menu Navigation:**
   - Use the **Up/Down Arrow Keys** to select a difficulty level.
   - Use the **Left/Right Arrow Keys** to select the Pac-Bot AI algorithm (A*, BFS, or DFS).
   - Press **Enter** to start the game.

2. **Observations:**
   - Pac-Bot (yellow circle) will automatically navigate the maze to collect food (green circles) while avoiding ghosts (red circles).
   - The ghosts use different algorithms (DFS, BFS, or A*) to chase Pac-Bot, depending on the selected difficulty level.

4. **Game Over:**
   - The game ends if Pac-Bot collides with a ghost or the timer runs out.
   - Press **ESC** to quit the game after it ends.

5. **Metrics:**
   - During gameplay, the following metrics are displayed at the bottom of the screen:
     - **Steps Taken:** Number of steps Pac-Bot has moved.
     - **Time Left:** Remaining time in seconds.
     - **Food Eaten:** Number of food pellets collected.
     - **Ram Used:** Current memory usage.

## Code Layout
- `pacbot.py`: Main game file that initializes and runs the game. Generates the maze layout,
creates 1 pac-bot and 4 ghosts. Handles the algorithmic implementation of A*, BFS, and DFS.
Also performs some metrics for steps taken, time, ram usage, and food count. 
- `memory_tracker.py`: Measure ram usage metrics. 
- `simulations.py`: Contains a simulator to simulate the game 50 times each per matchup, totaling 450 games. 

## Run Instructions
1. **Install Python 3**:
   - Ensure Python 3 is installed.
2. **Install Required Libraries: Pygame-ce**:
   - Run the following command:
     ```bash
     pip3 install pygame-ce
     ```
3. **Running the Game**:
   - Execute the following command in source directory:
     ```bash
     python3 pacbot.py
     ```
4. **Running the Simulator**:
  - Use the following command:
  ```bash
  python3 simulations.py
  ```

## Requirements
- Python 3.x
- Libraries: (Only pygame-ce needs to be installed. The rest are standard libraries that should be imported.)
  - `pygame-ce`
  - `heapq`
  - `random`
  - `deque`
  - `tracemalloc`
  - `csv` 

## Data
No additional data files are necessary to run Pac-Bot AI.
Though the simulations.py file does generate a results.csv file that provides some useful insights
on Pac-Bot AI's metrics. 
