<div align="center">
  <img src="https://github.com/user-attachments/assets/8b4bec90-cd7a-48f6-bd48-e874c8b06198" alt="output" width="150"/>
  <h1>A* Pac-Bot</h1>
  <p><strong>Overview:</strong></p>
  <p>A* Pac-Bot is an AI-based maze navigation game inspired by the classic Pac-Man. The project implements a multi-agent system where Pac-Man and ghosts use the A* Search algorithm for pathfinding and coordination. The game evaluates AI performance based on heuristics, efficiency, and adaptability in dynamically generated mazes.</p>
</div>

## Features:
- **A Star Search Algorithm**: Efficient pathfinding for Pac-Man and ghost agents.
- **Multi-Agent System**: Ghosts coordinate to chase Pac-Man, combining competitive and cooperative AI.
- **Mutliple Levels**: Create unique environments for testing AI performance.
- **Performance Metrics**: Evaluate path efficiency, based on elapsed time and food consumed.
- **Visualization**: Real-time visualization of AI controlled movements and interactions using Pygame.

## Implementation:
- **Programming Language**: Python 3
- **Game Development**: Pygame library
- **Algorithm**: A* Search for pathfinding and decision-making
- **Environment**: Grid-based maze with dynamic obstacles and partially observable states

## Team:
- **Victor Vu**: Team Leader; A* implementation, performance evaluation, game testing, documentation.
- **Cristian Gomez**: AI Engineer; game design, maze generation, documentation.
- **Alexander Hermenegildo**: AI Engineer; multi-agent implementation, competitive AI, documentation.
- **Jesus Fierro**: AI Engineer; cooperative AI, debugging, food system design, documentation.

## Instructions:
```
python3 pacman.py
```

## Requirements:
- pygame-ce
- heapq
- random
