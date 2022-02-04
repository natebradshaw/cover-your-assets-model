from options.options import Options

class Players:
    def __init__(self, id, hand):
        self.id = id
        self.name = self.set_name()
        self.hand = hand
        self.bank = []
        self.challenge_options = []

    def set_name(self):
        return input(f'Player {self.id}, what is your name?: ')

    def decide(self, options):
        def invalid_entry():
            print('Invalid Entry')

        print()
        self.print_new_turn()
        self.print_group(self.hand)
        while True:
            card_selection = input('Select card:')

            try:
                card_key = (int(card_selection)) -1
                if card_key < 0:
                    invalid_entry()
                    continue
            except ValueError:
                invalid_entry()
                continue

            try:
                card = self.hand[card_key]
            except IndexError:
                invalid_entry()
                continue

            while True:
                print()
                print(f'Card {card_selection} ({card.type}) Options:')
                self.print_options(options, card, card_selection)
                option_selection = input('Select move, or enter "change card":')
                if option_selection.upper() == 'CHANGE CARD':
                    break

                try:
                    option_key = (int(option_selection)) - 1
                    if option_key < 0:
                        invalid_entry()
                        continue
                except ValueError:
                    invalid_entry()
                    continue

                try:
                    option = options[card][option_key]
                except IndexError:
                    invalid_entry()
                    continue

                return option

    def draw(self, deck):
        self.hand.append(deck.pop())

    def get_challenge_options(self, parent_card, player):
        for card in player.hand:
            if self.validate_match(parent_card, card):
                player.challenge_options.append(card)

    def challenge_decide(self):
        def invalid_entry():
            print('Invalid Entry')

        self.print_group(self.challenge_options, 'REBUTTLES')
        while True:
            option_selection = input('Select card, or enter "no play":')
            if option_selection.upper() == 'NO PLAY':
                return None

            try:
                option_key = (int(option_selection)) - 1
                if option_key < 0:
                    invalid_entry()
                    continue
            except ValueError:
                invalid_entry()
                continue

            try:
                self.hand.remove(self.challenge_options[option_key])
                return self.challenge_options[option_key]
            except IndexError:
                invalid_entry()
                continue

    def print_group(self, group, group_name='HAND'):
        print()
        print(f"Player {self.name}'s {group_name}:")
        for i in range(0,len(group)):
            print(f'{i+1}:(${group[i].value}) {group[i].type}')

    def print_options(self, options, card, card_selection):
        # def print_cards():
        #     cards_str = '|'
        #     for sing_card in options[card][j].cards:
        #         cards_str += f' {sing_card.type} |'
        #     return cards_str
        i = 0
        for option in options[card]:
            i += 1
            if type(option) == "<class 'options.challenge.Challenge'>":
                print(f'{i}:{type(option)} - opp:{option.opponent.name}, {option.cards[0].type}')
            else:
                card_str = '|'
                for sing_card in option.cards:
                    card_str += sing_card.type + '|'
                print(f'{i}:{type(option)}, {card_str}')

    def print_new_turn(self):
        new_turn_display = f'NEW TURN: PLAYER {self.name} | '
        for i in range(0,2):
            new_turn_display += new_turn_display
        print(new_turn_display)

    def remove_single_card(self, card):
        self.hand.remove(card)

    def is_card_in_hand(self, card):
        for c in self.hand:
            if c == card:
                return True
        return False



