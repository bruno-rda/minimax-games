from games.base import Game

class Player:
    def __init__(self, name: str):
        self.name = name

    def choose_move(self, game: Game) -> int:
        raise NotImplementedError