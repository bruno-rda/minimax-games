class Player:
    def __init__(self, name: str):
        self.name = name

    def __call__(self, game):
        raise NotImplementedError