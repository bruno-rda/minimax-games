import random
from collections import deque
from game import Game, Player, get_best_move

ALL_DOMINOES = [
    (i, j)
    for i in range(7)
    for j in range(i, 7)
]

DOMINO_INDEX = {
    key: value 
    for value, key in enumerate(ALL_DOMINOES, start=1)
}

class Dominoes(Game):
    def __init__(
        self, 
        single: bool = False,
        tiles=None
    ):
        super().__init__()
        self.n_players = 2 if single else 4
        self.symbols = [f'{x} - Team {x%2}' for x in range(self.n_players)]

        self.tiles = self.init_tiles(tiles)
        self.board = deque([])
        self.turn_state = []
        self.n_pass = 0


    def init_tiles(self, tiles: list):
        shuffled = list(ALL_DOMINOES)
        random.shuffle(shuffled)

        n_tiles = 28 // self.n_players

        tiles = tiles if tiles is not None else [
            set(shuffled[i:i + n_tiles])
            for i in range(0, 28, n_tiles)
        ]

        assert len(tiles) == self.n_players, 'Tiles and players dont match'
        assert sum(len(tile) for tile in tiles) == 28, 'Invalid number of tiles'

        return tiles
        
    def is_over(self) -> bool:
        return (
            (self.winner is not None) or 
            (self.n_pass >= self.n_players)
        )
    
    def compute_final_score(self) -> float:
        if self.winner is not None:
            mult = -1 if self.winner else 1
            score = self.scores[self.winner]
            return mult * score

        return 0

    @property
    def scores(self) -> tuple[float, float]:
        return (
            sum(sum(x) for i, y in enumerate(self.tiles) for x in y if i%2), 
            sum(sum(x) for i, y in enumerate(self.tiles) for x in y if not i%2)
        )

    def legal_moves(self) -> list:
        # In first turn every move is legal
        if len(self.board) == 0:
            return [
                DOMINO_INDEX[tile] 
                for tile in self.tiles[self.turn]
            ]

        # Negative index for left compatibility
        # Positive index for right compatibility
        legal_moves = [
            -DOMINO_INDEX[tile]
            for tile in self.tiles[self.turn]
            if self.board[0][0] in tile
        ] + [
            DOMINO_INDEX[tile]
            for tile in self.tiles[self.turn]
            if self.board[-1][-1] in tile
        ]

        # If no legal moves are available, return 0 (Pass)
        return legal_moves or [0]

    def valid_move(self, i: int) -> bool:
        return i in self.legal_moves()

    def play_move(self, i: int):
        assert self.valid_move(i), f'Invalid move {i}'
        assert not self.is_over(), 'Game is over'

        # Player has to pass
        if i == 0:
            self.n_pass += 1
            self.turn += 1
            self.turn %= self.n_players
            self.turn_state.append(None)

            # Check closed game
            if self.n_pass >= self.n_players:
                scores = self.scores
                diff = scores[0] - scores[1]

                if diff > 0: self.winner = 0
                elif diff < 0: self.winner = 1

            return
        
        # If move is available, game is still open
        self.n_pass = 0
        self.turn_state.append(i)

        tile = ALL_DOMINOES[abs(i) - 1]
        self.tiles[self.turn].discard(tile)
        
        if i < 0:
            # Sort tile so that it matches with its right neighbor
            oriented_tile = sorted(
                tile, 
                key=lambda x: x == self.board[0][0],
            )

            self.board.appendleft(oriented_tile)
        else:
            # If its first move, then orientation doesnt matter
            # Sort tile so that it matches with its left neighbor

            oriented_tile = tile if len(self.board) == 0 else (
                sorted(
                    tile, 
                    key=lambda x: x == self.board[-1][-1],
                    reverse=True
                )
            )

            self.board.append(oriented_tile)

        # If a player used all tiles, he won
        if len(self.tiles[self.turn]) == 0:
            self.winner = int((self.turn % 2))

        # Update turn
        self.turn += 1
        self.turn %= self.n_players

    def undo_move(self):
        self.turn -= 1
        self.turn %= self.n_players
        self.winner = None

        i = self.turn_state.pop()
        
        # If last move was a pass
        if i is None:
            self.n_pass = max(0, self.n_pass - 1)
            return
        
        # Retrieve last placed tile
        oriented_tile = (
            self.board.popleft() 
            if i < 0 else 
            self.board.pop()
        )

        # Return tile to standard representation
        tile = tuple(sorted(oriented_tile))
        self.tiles[self.turn].add(tile)

    def display_board(self):
        print('\n', '-'*50, '\n', list(self.board))

    def display_legal_moves(self):
        print('All tiles: ', self.tiles[self.turn])
        print('\nAvailable tiles:')

        for i in self.legal_moves():
            label = 'Pass' if i == 0 else ALL_DOMINOES[abs(i) - 1]
            print(f'{i}: {label}')
        
        print()
    
    
class DominoesPlayer(Player):
    n_instances = 0
    def __init__(self, name=None):
        DominoesPlayer.n_instances += 1

        super().__init__(
            name or f'Player {DominoesPlayer.n_instances}'
        )

    def __call__(self, game: Dominoes) -> int:
        game.display_legal_moves()
        move = input('Select a tile [1-28]: ')
        assert move.lstrip('-').isdigit(), 'Only digits are allowed'
        return int(move)
    
    
class DominoesAI(Player):
    def __init__(
        self, 
        name, 
        alpha_beta=True,
        verbose=False, 
        max_depth=10
    ):
        super().__init__(name)
        self.verbose = verbose
        self.max_depth = max_depth
        self.alpha_beta = alpha_beta

    def __call__(self, game: Dominoes) -> int:
        game.display_legal_moves()

        return get_best_move(
            game, 
            ab=self.alpha_beta,
            verbose=self.verbose,
            max_depth=self.max_depth
        )