from .base import Player
from games.dominoes import Dominoes
from solver import Solver
from typing import Optional

class DominoesPlayer(Player):
    n_instances = 0
    def __init__(self, name: Optional[str] = None):
        DominoesPlayer.n_instances += 1

        super().__init__(
            name or f'Player {DominoesPlayer.n_instances}'
        )

    def choose_move(self, game: Dominoes) -> int:
        game.display_legal_moves()
        move = input('Select a tile [1-28]: ')
        assert move.lstrip('-').isdigit(), 'Only digits are allowed'
        return int(move)
    

class DominoesAI(Player):
    def __init__(
        self, 
        name: Optional[str] = None,
        verbose: bool = False,
        max_depth: int = 10
    ):
        super().__init__(name or 'Dominoes AI')
        self.solver = Solver(
            verbose=verbose, 
            max_depth=max_depth
        )

    def choose_move(self, game: Dominoes) -> int:
        game.display_legal_moves()
        return self.solver.get_best_move(game)