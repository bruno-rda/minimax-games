from games.base import Game
from players.base import Player

def play(game: Game, player: Player, opponent: Player):
    players = [player, opponent]

    while not game.is_over():
        game.display_board()

        current = players[game.turn % 2]
        symbol = game.symbols[game.turn % 2]
        print(f'\nTurn: {current.name} {symbol}')

        try:
            move = current.choose_move(game)
            print(f'{current.name} {symbol} plays: {move}\n')
            game.play_move(move)
        except AssertionError as e:
            print(e)
        except KeyboardInterrupt:
            return
        except Exception as e:
            raise e

    else:
        game.display_board()

        if game.winner is None:
            print('\nDraw')
        else:
            winner = players[game.winner % 2]
            symbol = game.symbols[game.winner % 2]

            print(
                f'\nWinner: {winner.name} {symbol}'
                f'\nScore: {abs(game.compute_final_score())}'
            )