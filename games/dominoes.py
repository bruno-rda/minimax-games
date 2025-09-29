import random
from collections import deque
from .base import Game

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
        single_player: bool = False,
        tiles=None
    ):
        self.n_players = 2 if single_player else 4

        super().__init__(
            symbols=[f'{x} - Team {x%2}' for x in range(self.n_players)],
            max_score=120
        )

        self.tiles = self.init_tiles(tiles)
        self.board = deque([])
        self.turn_state = []
        self.occurences = [0]*7


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

    def get_key(self):
        return tuple(
            [
                frozenset(self.tiles[i])
                for i in range(self.n_players)
            ] + [
                self.board[0][0],
                self.board[-1][-1],
                self.turn
            ]
        )

    def is_closed_game(self):
        if len(self.board) < 10:
            return False
        
        l, r = self.board[0][0], self.board[-1][-1]
        return (
            self.occurences[l] == 8 and 
            self.occurences[r] == 8
        )
    
    def is_over(self) -> bool:
        return (
            (self.winner is not None) or 
            (self.is_closed_game())
        )
    
    def compute_final_score(self) -> float:
        if self.winner is not None:
            mult = 1 if self.winner == self.turn % 2 else -1
            return mult * self.scores[self.winner]
        return 0

    def get_upper_bound(self) -> float:
        return self.scores[self.turn % 2]

    def get_lower_bound(self) -> float:
        return -self.scores[(self.turn + 1) % 2]

    def evaluate_immediate_win(self) -> float | None:
        legal_moves = self.legal_moves()
        
        # If you can only pass, then there is no immediate win
        if legal_moves == [0]:
            return None
        
        # If you can play your last tile, then you win
        if len(legal_moves) == 1 and len(self.tiles[self.turn]) == 1:
            return self.get_upper_bound()
        
        for move in legal_moves:
            tile = ALL_DOMINOES[abs(move) - 1]
            self.occurences[tile[0]] += 1
            self.occurences[tile[1]] += 1

            closed_game = self.is_closed_game()
            self.occurences[tile[0]] -= 1
            self.occurences[tile[1]] -= 1

            # If game is not closed, then there is no immediate win
            if not closed_game:
                continue
                
            player = self.get_upper_bound()
            opponent = self.get_lower_bound() + sum(tile)
            diff = player + opponent
            
            # If you can close the game and have greater score, you win
            if diff > 0:
                return player
            elif diff < 0:
                return opponent
            else:
                return 0
            
        return None
    
    def evaluate_forced_loss(self):
        next_idx = (self.turn + 1) % self.n_players
        next_tiles = list(self.tiles[next_idx])
        
        # If opponent has more than 1 tile, then there is no forced loss
        if len(next_tiles) > 1:
            return None
        
        # Get the best tile to play assuming forced loss exists
        legal_moves = self.legal_moves()
        best_tile_sum = (
            0 # If opponent can only pass, best sum is 0
            if legal_moves == [0] else
            max(sum(ALL_DOMINOES[abs(x) - 1]) for x in legal_moves)
        )
        
        # Get edge tile numbers
        l, r = self.board[0][0], self.board[-1][-1]

        # If opponents last tile is compatible with both edge tiles, 
        # then there is a forced loss, and we can return the score
        if l in next_tiles[0] and r in next_tiles[0]:
            return self.get_lower_bound() + best_tile_sum
        
        # If there is no forced loss, return None
        return None
    
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
            self.turn += 1
            self.turn %= self.n_players
            self.turn_state.append(0)
            return
        
        # If move is available, game is still open
        self.turn_state.append(i)

        tile = ALL_DOMINOES[abs(i) - 1]
        self.tiles[self.turn].discard(tile)
        self.occurences[tile[0]] += 1
        self.occurences[tile[1]] += 1
        
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

        if self.is_closed_game():
            scores = self.scores
            diff = scores[0] - scores[1]

            if diff > 0:
                self.winner = 0
            elif diff < 0:
                self.winner = 1

        # Update turn
        self.turn += 1
        self.turn %= self.n_players

    def undo_move(self):
        self.turn -= 1
        self.turn %= self.n_players
        self.winner = None

        i = self.turn_state.pop()
        
        # If last move was a pass
        if i == 0:
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
        self.occurences[tile[0]] -= 1
        self.occurences[tile[1]] -= 1

    def display_board(self):
        print('\n', '-'*50, '\n', list(self.board))

    def display_legal_moves(self):
        print('All tiles: ', self.tiles[self.turn])
        print('\nAvailable tiles:')

        for i in self.legal_moves():
            label = 'Pass' if i == 0 else ALL_DOMINOES[abs(i) - 1]
            print(f'{i}: {label}')
        
        print()