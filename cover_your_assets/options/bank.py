from options.options import Options
from bundle import Bundle

class Bank(Options):
    def __init__(self, location, cards, discard_source):
        super().__init__(location, cards)
        self.discard_source = discard_source

    @staticmethod
    def valid_option(bank, card1, card2, discard_source):
        if Options.validate_match(card1, card2):
            return Bank(location=bank, cards=[card1, card2], discard_source=discard_source)
        return None

    def execute_option(self, player, discard=None):
        if not self.discard_source:
            self.remove_cards_from_hand(player)
        else:
            player.hand.remove(self.cards[0])
            discard.pop()
        bundle = Bundle(self.cards)
        self.location.append(bundle)
