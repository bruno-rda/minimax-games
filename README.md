# Minimax Games

## Introduction

This repository contains an implementation of several classic board games, including Tic Tac Toe, Connect 4 and Classic Dominoes. The code structure is designed to be modular and extensible, allowing new games and functionality to be added easily. It uses an object-oriented approach to represent games and players, and a negamax algorithm with alpha-beta pruning is implemented for optimal decision-making in the games.

In addition to the implementation in Python modules, a Jupyter notebook (`game_notebook.ipynb`) is included that provides practical examples and demonstrations of how to use the different classes and functionalities of the project.

## Project Structure

The project is organized in several folders and files:

- **games/**: Contains game implementations and base classes:
  - **games/base.py**: Defines the `Game` base class, which represents a board game with board, turns, and game logic.
  - **games/tictactoe.py**: Tic Tac Toe game implementation.
  - **games/connect4.py**: Connect 4 game implementation.
  - **games/dominoes.py**: Classic Dominoes game implementation.
- **players/**: Contains player implementations and base classes:
  - **players/base.py**: Defines the `Player` base class, which represents players in the games.
  - **players/tictactoe.py**: Tic Tac Toe player implementations (human and AI).
  - **players/connect4.py**: Connect 4 player implementations (human and AI).
  - **players/dominoes.py**: Dominoes player implementations (human and AI).
- **solver.py**: Implements the negamax algorithm with alpha-beta pruning for optimal move calculation.
- **runner.py**: Provides a game runner function to play games between players.
- **game_notebook.ipynb**: A Jupyter notebook containing examples of how to create and play the different games implemented, as well as demonstrations of the negamax algorithm.
- **tests.ipynb**: A Jupyter notebook containing tests and benchmarks for the different games and algorithms.


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

### Negamax Algorithm

The negamax algorithm is used to calculate the best possible move given a game state. This algorithm evaluates all possible moves and their outcomes, choosing the move that maximizes the probability of winning. The algorithm was implemented with alpha-beta pruning and has a cache to store the upper and lower bounds of the evaluated nodes, which optimizes the search process. The implementation includes immediate win detection and forced loss evaluation for enhanced performance.

### User Interface

The game can be played through the console, where players can enter their moves. The AI can also be used as an opponent, providing a challenging gaming experience.

## Requirements

- Python 3.8 or higher
- Jupyter Notebook (for interactive examples and tests)

## Installation

1. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

## How to Run the Project

To run the project, ensure you have Python installed on your system. If you want to explore the interactive examples, you will also need to have Jupyter Notebook installed. Then, follow these steps:

1. **Clone the repository:**
   ```bash
   git clone https://github.com/bruno-rda/minimax-games.git
   cd minimax-games
   ```

2. **To run the games directly from the console:**
   ```python
   from games import TicTacToe
   from players import TicTacToePlayer, TicTacToeAI
   from runner import play

   game = TicTacToe()
   player = TicTacToePlayer()
   ai = TicTacToeAI('AI')
   play(game, player, ai)
   ```
   You can adapt this example to play other implemented games by importing the corresponding game and player classes.