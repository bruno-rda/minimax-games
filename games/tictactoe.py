from typing import Literal
from .base import Game

class TicTacToe(Game):
    def __init__(self):
        super().__init__(
            symbols=['❌', '⭕️'],
            max_score=9-5
        )
        self.player = set()
        self.opponent = set()
        self.turn_state = []

    @staticmethod
    def winning_move(moves, last_move):
        all_moves = list(moves | {last_move})

        winning = (
            (0, 1, 2), (3, 4, 5), (6, 7, 8), (0, 3, 6),
            (1, 4, 7), (2, 5, 8), (0, 4, 8), (2, 4, 6)
        )

        return any(all([move in all_moves for move in win]) for win in winning)

    def get_key(self):
        return tuple([
            frozenset(self.player),
            frozenset(self.opponent)
        ])
    
    def is_over(self) -> bool:
        return (self.winner is not None) or (len(self.turn_state) >= 9)
    
    def compute_final_score(self) -> float:
        if self.winner is not None:
            mult = 1 if self.winner == self.turn else -1
            return mult * (10 - len(self.turn_state))
        return 0

    def get_upper_bound(self) -> float:
        return (10 - len(self.turn_state))

    def evaluate_immediate_win(self) -> float | None:
        moves = self.player if not (self.turn % 2) else self.opponent

        for choice in self.legal_moves():
            if self.winning_move(moves | {choice}, choice):
                return self.get_upper_bound() - 1
        
        return None
    
    def evaluate_forced_loss(self) -> bool:
        moves = self.player if (self.turn % 2) else self.opponent
        winning_chance = 0

        for choice in self.legal_moves():
            if self.winning_move(moves | {choice}, choice): 
                winning_chance += 1
            
            # If opponent has at least 2 winning moves, player cannot prevent loss
            if winning_chance == 2: 
                return self.get_lower_bound() + 2
        
        return None
    
    def legal_moves(self) -> set:
        return {0, 1, 2, 3, 4, 5, 6, 7, 8} - (self.player | self.opponent)

    def valid_move(self, choice: Literal[0, 1, 2, 3, 4, 5, 6, 7, 8]) -> bool:
        return choice in self.legal_moves()

    def play_move(self, choice: Literal[0, 1, 2, 3, 4, 5, 6, 7, 8]):
        assert self.valid_move(choice), 'Invalid move'
        assert not self.is_over(), 'Game is over'

        # Register move
        self.turn_state.append(choice)
        moves = self.player if not (self.turn % 2) else self.opponent
        moves.add(choice)

        # Check if last move wins the game for current player
        if self.winning_move(moves, choice):
            self.winner = self.turn

        # Switch turns
        self.turn ^= 1

    def undo_move(self):
        self.turn ^= 1
        self.winner = None

        choice = self.turn_state.pop()
        moves = self.player if not (self.turn % 2) else self.opponent
        moves.discard(choice)

    def display_board(self):
        board = [[str(i*3 + j) for i in range(3)] for j in range(3)]

        for i, moves in enumerate([self.player, self.opponent]):
            symbol = self.symbols[i]

            for choice in moves:
                row, col = choice // 3, choice % 3
                board[col][row] = symbol

        for row in range(0, 3):
            print('|\t' + '\t|\t'.join(board[col][row] for col in range(3)) + '\t|')
            print('-' * 49)