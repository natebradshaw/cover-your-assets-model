from options.options import Options

class Challenge(Options):
    def __init__(self, location, cards, opponent):
        super().__init__(location, cards)
        self.opponent = opponent
        self.winner = None
        self.bundle = self.opponent.bank[-1]
        self.new_pot = []

    @staticmethod
    def valid_option(opp_bank, card, opp):
        if len(opp_bank) > 1 and Options.validate_match(opp_bank[-1].parent_card, card):
            return Challenge(location=opp_bank, cards=[card], opponent=opp)
        else:
            return None

    def execute_option(self, player, discard=None):
        def rebuttle(per):
            selection = per.challenge_decide()
            if len(per.challenge_options) == 0:
                outcome(per)
                return False
            else:
                if selection is None:
                    outcome(per)
                    return False
                else:
                    per.challenge_options.remove(selection)
                    self.new_pot.append(selection)
                    return True

        def outcome(per):
            for p in players:
                p.challenge_options = []
            players.remove(per)
            self.winner = players[0]
        player.hand.remove(self.cards[0])
        players = [self.opponent, player]
        self.new_pot = [self.cards[0]]
        challenge_live = True
        parent_card = self.opponent.bank[-1].parent_card
        for person in players:
            self.get_options(parent_card, person)

        i = 0
        while challenge_live:
            challenge_live = rebuttle(players[i % 2])
            i += 1
        self.distribute_wealth(self.new_pot)

    def distribute_wealth(self, new_pot):

        if self.opponent == self.winner:
            bundle = self.opponent.bank[-1]
            bundle.add_cards(self.new_pot)
        else:
            bundle = self.opponent.bank.pop()
            bundle.add_cards(self.new_pot)
            self.winner.bank.append(bundle)

    def get_options(self, parent_card, player):
        for card in player.hand:
            if self.validate_match(parent_card, card) and card != self.cards[0]:
                player.challenge_options.append(card)

