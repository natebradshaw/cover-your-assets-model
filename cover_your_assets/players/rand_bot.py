from players.players import Players


class RandBot(Players):
    def __init__(self, id, hand):
        super().__init__(id, hand)

    def set_name(self):
        return str(self.id)
