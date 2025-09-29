from .base import Player
from games.connect4 import Connect4
from solver import Solver
from typing import Optional

class Connect4Player(Player):
    n_instances = 0
    def __init__(self, name: Optional[str] = None):
        Connect4Player.n_instances += 1

        super().__init__(
            name or f'Player {Connect4Player.n_instances}'
        )

    def choose_move(self, game: Connect4) -> int:
        move = input('Select a column [0-6]: ')
        assert move.isdigit(), 'Only digits are allowed'
        return int(move)


class Connect4AI(Player):
    def __init__(
        self, 
        name: Optional[str] = None,
        verbose: bool = False,
        max_depth: int = 10
    ):
        super().__init__(name or 'Connect4 AI')
        self.solver = Solver(
            verbose=verbose, 
            max_depth=max_depth
        )

    def choose_move(self, game: Connect4) -> int:
        return self.solver.get_best_move(game)