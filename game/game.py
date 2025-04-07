from game.player import Player

class Game:
    def __init__(
        self, 
        symbols: list[str], 
        max_score: int
    ):
        self.winner = None
        self.turn = 0
        self.symbols = symbols
        self.max_score = max_score
    
    def is_over(self) -> bool:
        raise NotImplementedError
    
    def compute_final_score(self) -> float:
        '''
        Computes the score of the final state.
        A positive score means a win for the current player.
        A negative score means a loss for the current player.
        * Only meant to be called if game is over *
        '''
        raise NotImplementedError
    
    def evaluate_immediate_win(self) -> float | None:
        '''
        Returns score of the immediate win if it exists.
        Immediate win is when you can win in the next move.
        '''
        raise NotImplementedError
    
    def evaluate_forced_loss(self) -> float | None:
        '''
        Returns score of the forced loss if it exists.
        Forced loss is when you cant prevent the opponent from winning.
        '''
        raise NotImplementedError
    
    def get_upper_bound(self) -> float:
        '''
        Returns score of the current player if they instantly win.
        '''
        raise NotImplementedError
    
    def get_lower_bound(self) -> float:
        '''
        Returns score of the opposing player if they instantly win.
        '''
        return -self.get_upper_bound()
    
    def play_move(self, move) -> None:
        raise NotImplementedError
    
    def undo_move(self) -> None:
        raise NotImplementedError

    def legal_moves(self):
        raise NotImplementedError

    def display_board(self) -> None:
        raise NotImplementedError
    
    def get_key(self):
        ''' 
        Returns unique key that unambiguosly represents the state
        so that solution scores can be computed and stored.
        '''
        return None


    def play(self, player: Player, opponent: Player):
        while not self.is_over():
            self.display_board()

            name = player.name if not (self.turn % 2) else opponent.name
            print(f'\nTurn: {name} {self.symbols[self.turn]}')

            try:
                choice = (
                    player(self) 
                    if not (self.turn % 2) else
                    opponent(self)
                )

                print(f'{name} {self.symbols[self.turn]} plays: {choice}\n')
                self.play_move(choice)
            except AssertionError as e:
                print(e)
            except KeyboardInterrupt:
                return
            except Exception as e:
                raise e

        else:
            self.display_board()

            if self.winner is None:
                print('\nDraw')
            else:
                name = player.name if not (self.winner % 2) else opponent.name

                print(
                    f'\nWinner: {name} {self.symbols[self.winner]}'
                    f'\nScore: {abs(self.compute_final_score())}'
                )