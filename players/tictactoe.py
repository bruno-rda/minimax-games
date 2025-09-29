from .base import Player
from games.tictactoe import TicTacToe
from solver import Solver
from typing import Optional

class TicTacToePlayer(Player):
    n_instances = 0
    def __init__(self, name: Optional[str] = None):
        TicTacToePlayer.n_instances += 1

        super().__init__(
            name or f'Player {TicTacToePlayer.n_instances}'
        )

    def choose_move(self, game: TicTacToe) -> int:
        move = input('Select box [0-8]: ')
        assert move.isdigit(), 'Only digits are allowed'
        return int(move)


class TicTacToeAI(Player):
    def __init__(
        self, 
        name: Optional[str] = None,
        verbose: bool = False
    ):
        super().__init__(name or 'TicTacToe AI')
        self.solver = Solver(verbose=verbose)

    def choose_move(self, game: TicTacToe) -> int:
        return self.solver.get_best_move(game)