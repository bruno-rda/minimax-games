# Minimax Games

## Introduction

This repository contains an implementation of several classic board games, including Tic Tac Toe, Connect 4 and Classic Dominoes. The code structure is designed to be modular and extensible, allowing new games and functionality to be added easily. It uses an object-oriented approach to represent games and players, and a minimax algorithm is implemented for decision-making in the games.

In addition to the implementation in Python modules, a Jupyter notebook (`game_notebook.ipynb`) is included that provides practical examples and demonstrations of how to use the different classes and functionalities of the project.

## Project Structure

The project is organized in several folders and files:

- **game/game.py**: Defines the `Game` class, which represents a board game, considering board, turns, and game logic.
- **game/player.py**: Defines the `Player` class, which represents the players in the games.
- **game/minimax.py**: Implements the minimax algorithm, which is used to calculate the best possible move in games.
- **game/board_games/**: Contains game-specific implementations, such as Tic Tac Toe, Connect 4 and Dominoes.
- **game_notebook.ipynb**: A Jupyter notebook containing examples of how to create and play the different games implemented, as well as demonstrations of the use of the minimax algorithm.
- **benchmarks.ipynb**: A Jupyter notebook containing examples of how to run the minimax algorithm with different games and configurations.


## Features

### Implemented Games

1. **Tic Tac Toe**:
   - Two players take turns placing their symbols on a 3x3 board.
   - The first player to align three of their symbols in a row, column or diagonal wins.

2. **Connect 4**:
   - Two players take turns dropping their pieces into a 7x6 grid.
   - The objective is to align four pieces in a row, either horizontally, vertically or diagonally.

3. **Classic Dominoes**:
   - Players place tiles on a board, trying to match the numbers on the ends of the tiles.
   - The game can be played in single player or team mode.

### Minimax Algorithm

The minimax algorithm is used to calculate the best possible move given a game state. This algorithm evaluates all possible moves and their outcomes, choosing the move that maximizes the probability of winning. The algorithm was implemented with alpha-beta pruning and has a cache to store the upper and lower bounds of the evaluated nodes, which optimizes the search process.

### User Interface

The game can be played through the console, where players can enter their moves. The AI can also be used as an opponent, providing a challenging gaming experience.

## How to Run the Project

To run the project, ensure you have Python installed on your system. If you want to explore the interactive examples, you will also need to have Jupyter Notebook installed. Then, follow these steps:

1. **Clone the repository:**
   ```bash
   git clone https://github.com/bruno-rda/minimax-games.git
   cd minimax-games
   ```

2. **To run the games directly from the console:**
   ```python
   from game.board_games import TicTacToe, TicTacToePlayer, TicTacToeAI

   game = TicTacToe()
   player = TicTacToePlayer()
   ai = TicTacToeAI('AI')
   game.play(player, ai)
   ```
   You can adapt this example to play other implemented games.

3. **To explore the examples in the notebook:**
   ```bash
   jupyter notebook game_notebook.ipynb
   ```
   This will open the notebook in your browser, where you can run the code cells and see examples of how to use the different classes and features of the project, including the creation of games and the use of human players and AI based on the minimax algorithm.