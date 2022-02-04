from options.options import Options

class Discard(Options):
    def __init__(self, location, cards):
        super().__init__(location, cards)

    def execute_option(self, player, discard=None):
        self.remove_cards_from_hand(player)
        self.location.append(self.cards[0])


