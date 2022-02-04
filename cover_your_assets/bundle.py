class Bundle:
    def __init__(self, cards: list):
        self.cards = cards
        self.parent_card = self.set_type()
        self.value = None
        self.set_value()
        self.correct_card_order()

    def set_value(self):
        self.value = 0
        for card in self.cards:
            self.value += card.value

    def set_type(self):
        for card in self.cards:
            if not card.is_wild:
                return card

    def add_cards(self, cards):
        self.cards += cards
        self.set_value()
        self.correct_card_order()

    def correct_card_order(self):
        if self.cards[-1].is_wild:
            for i in range(0, len(self.cards)):
                if not self.cards[i].is_wild:
                    self.cards[-1], self.cards[i] = self.cards[i], self.cards[-1]# add break after this

