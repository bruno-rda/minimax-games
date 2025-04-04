from game.player import Player

class Game:
    def __init__(self):
        self.winner = None
        self.turn = 0
        self.symbols = ['', '']
    
    def is_over(self) -> bool:
        raise NotImplementedError
    
    def compute_final_score(self) -> float:
        raise NotImplementedError
    
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
        raise NotImplementedError


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