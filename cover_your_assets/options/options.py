import abc

class Options:
    def __init__(self, location, cards):
        self.location = location
        self.cards = cards

    @abc.abstractmethod
    def execute_option(self, player, discard=False):
        "Each type of option will have a unique way of being executing"

    @staticmethod
    def validate_match(card1, card2):
        if card1.is_wild != card2.is_wild or (card1.type == card2.type and
                                              (not card1.is_wild and not card2.is_wild)):
            return True
        return False

    def remove_cards_from_hand(self, player):
        for play_card in self.cards:
            for card in player.hand:
                if card == play_card:
                    player.hand.remove(card)
                    break

