from game import Game, Player, Solver
from typing import Literal

class Connect4(Game):
    def __init__(self):
        super().__init__(
            symbols=['🟡', '🔴'],
            max_score=42-7
        )

        self.player = set()
        self.opponent = set()
        self.occurences = [0]*7
        self.turn_state = []

    @staticmethod
    def winning_move(moves: set, last_move: int) -> bool:
        row, col = last_move // 7, last_move % 7

        def get_max_consecutive(offset, moves):
            consecutive = 0

            for offset_ in [offset, -offset]:
                i, prev_col = 1, col
                while True:
                    move = last_move - offset_ * i
                    if move not in moves or abs(move % 7 - prev_col) > 1:
                        break

                    prev_col = move % 7
                    consecutive += 1
                    i += 1
                    if consecutive >= 3: return True

            return False

        # Vertical win
        if row >= 3:
            if get_max_consecutive(7, moves):
                return True

        # Horizontal win
        center = row * 7 + 3
        if center in moves:
            if get_max_consecutive(1, moves):
                return True

        # Diag up win
        center = 8 * (3 - col) + last_move
        if center in moves:
            if get_max_consecutive(8, moves):
                return True

        # Diag down win
        center = -6 * (3 - col) + last_move
        if center in moves:
            if get_max_consecutive(6, moves):
                return True

        return False

    def get_key(self) -> tuple:
        return tuple([
            frozenset(self.player),
            frozenset(self.opponent)
        ])
    
    def is_over(self) -> bool:
        return (
            (self.winner is not None) or 
            (len(self.turn_state) >= 42)
        )
    
    def compute_final_score(self) -> float:
        if self.winner is not None:
            mult = 1 if self.winner == self.turn else -1
            return mult * (43 - len(self.turn_state))
        return 0
        
    def get_upper_bound(self) -> float:
        return (43 - len(self.turn_state))

    def evaluate_immediate_win(self) -> float | None:
        moves = self.player if not (self.turn % 2) else self.opponent

        for choice in self.legal_moves():
            move = choice + (self.occurences[choice]) * 7
            
            # If next move wins, return score
            if self.winning_move(moves | {move}, move): 
                return self.get_upper_bound() - 1
        
        return None
    
    def evaluate_forced_loss(self):
        moves = self.player if (self.turn % 2) else self.opponent
        winning_chance = 0

        for choice in self.legal_moves():
            move = choice + (self.occurences[choice]) * 7
            
            if self.winning_move(moves | {move}, move): 
                winning_chance += 1 
            
            # If opponent has at least 2 winning moves, player cannot prevent loss
            if winning_chance == 2: 
                return self.get_lower_bound() + 2
        
        return None
    
    def legal_moves(self) -> list:
        return [i for i in [3, 4, 2, 5, 1, 6, 0] if self.occurences[i] < 6]

    def valid_move(self, choice: Literal[0, 1, 2, 3, 4, 5, 6]) -> bool:
        return choice in self.legal_moves()

    def play_move(self, choice: Literal[0, 1, 2, 3, 4, 5, 6]) -> None:
        assert self.valid_move(choice), 'Invalid move'
        assert not self.is_over(), 'Game is over'

        # Register move
        self.turn_state.append(choice)
        self.occurences[choice] += 1

        move = choice + (self.occurences[choice] - 1) * 7
        moves = self.player if not (self.turn % 2) else self.opponent
        moves.add(move)

        # Check if last move wins the game for current player
        if self.winning_move(moves, move):
            self.winner = self.turn

        # Switch turns
        self.turn ^= 1

    def undo_move(self) -> None:
        self.turn ^= 1
        self.winner = None

        choice = self.turn_state.pop()
        self.occurences[choice] -= 1

        move = choice + (self.occurences[choice]) * 7
        moves = self.player if not (self.turn % 2) else self.opponent
        moves.discard(move)


    def display_board(self) -> None:
        board = [['  ' for _ in range(6)] for _ in range(7)]

        for i, moves in enumerate([self.player, self.opponent]):
            symbol = self.symbols[i]

            for choice in moves:
                row, col = choice // 7, choice % 7
                board[col][row] = symbol

        for row in range(-1, -7, -1):
            print('| ' + ' | '.join(board[col][row] for col in range(7)) + ' |')
            print('-' * 36)

        print('| ' + '  | '.join(str(col) for col in range(7)) + '  |')
    

class Connect4Player(Player):
    n_instances = 0
    def __init__(self, name=None):
        Connect4Player.n_instances += 1

        super().__init__(
            name or f'Player {Connect4Player.n_instances}'
        )

    def __call__(self, game: Connect4) -> int:
        move = input('Select a column [0-6]: ')
        assert move.isdigit(), 'Only digits are allowed'
        return int(move)


class Connect4AI(Player):
    def __init__(self, name, verbose=False, max_depth=10):
        super().__init__(name)
        self.solver = Solver(
            verbose=verbose, 
            max_depth=max_depth
        )

    def __call__(self, game: Connect4) -> int:
        return self.solver.get_best_move(game)