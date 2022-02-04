from players.players import Players
from players.rand_bot import RandBot
from options.options import Options
from options.bank import Bank
from options.challenge import Challenge
from options.discard import Discard
from cards import Card
from card_dict import card_dict
import random


class Game:
    def __init__(self, total_players, bot_game_type=0):
        self.bot_game_type = bot_game_type
        self.deck = self.set_deck()
        self.discard = []
        self.players = self.set_players(total_players)
        self.total_players = total_players
        self.turn_count = 0
        self.turn_owner = None
        self.turn_options = {}
        self.turn_decision = {}
        self.live_status = True

    def set_deck(self):
        deck = []
        for value in card_dict:
            for i in range(0, card_dict[value]['count']):
                for card_type in card_dict[value]['types']:
                    is_wild = card_dict[value]['wild']
                    deck.append(Card(value, card_type, is_wild))
        random.shuffle(deck)
        return deck

    def set_players(self, total_players):
        def get_hand():
            return [self.deck.pop() for i in range(5)]

        def create_player(id):
            if self.bot_game_type == 0 and id == 0:
                return Players(id, get_hand())
            else:
                return RandBot(id, get_hand())

        player_list = [create_player(i) for i in range(0, total_players)]
        return tuple(player for player in player_list)

    def set_turn_details(self):
        iteration = 0
        while True:

            iteration += 1
            key = (self.turn_count + self.total_players) % self.total_players
            current_player = self.players[key]

            if len(current_player.hand) > 0:
                self.turn_owner = current_player
                self.turn_count += 1
                break
            elif iteration == self.total_players:
                self.live_status = False
                break

    def play(self):
        while self.live_status:
            self.turn()
        self.conclude()
        self.save_details()

    def turn(self):
        self.set_turn_details()
        self.display_details()
        self.get_options()
        self.decide()

    def get_options(self):
        for card in self.turn_owner.hand:
            self.get_discard_options(card) # Must go prior to challenge and bank gets
            self.get_challenge_options(card)
        self.get_bank_options()

    def get_discard_options(self, card):
        self.turn_options[card] = [Discard(self.discard, [card])]

    def get_challenge_options(self, card):
        for opp in self.players:
            if opp != self.turn_owner:
                option = Challenge.valid_option(opp.bank, card, opp)
                if option:
                    self.turn_options[card].append(option)

    def get_bank_options(self):
        def create_option(card1, card2, discard_source):
            option = Bank.valid_option(self.turn_owner.bank, card1, card2, discard_source)
            if option:
                self.turn_options[card1].append(option)
            if option and not discard_source:
                self.turn_options[card2].append(option)

        for i in range(0, len(self.turn_owner.hand)-1):
            if len(self.discard) > 0:
                create_option(self.turn_owner.hand[i], self.discard[-1], True)
            for j in range(len(self.turn_owner.hand)-1, i, -1):
                create_option(self.turn_owner.hand[i], self.turn_owner.hand[j], False)

    def decide(self):
        decided_option = self.turn_owner.decide(self.turn_options)
        decided_option.execute_option(self.turn_owner, self.discard)
        self.refill_hand(self.turn_owner)
        if str(decided_option.__class__) == "<class 'options.challenge.Challenge'>":
            self.refill_hand(decided_option.opponent)

    def refill_hand(self, player):
        while len(player.hand) < 5:
            player.draw(self.deck)

    def conclude(self):
        pass

    def save_details(self):
        pass

    def display_details(self):
        print(f'Turn {self.turn_count}')
        print(f'Turn owner: {self.turn_owner.name}, {self.turn_owner}')
        if len(self.discard) > 0:print(f'Top of Discard: {self.discard[-1].type}')

        for player in self.players:
            hand_str = ''
            for card in player.hand:
                hand_str += f'{card.type}, '
            print(f'Player {player.name} hand: {hand_str}')
            bundle_str = ''
            player_total = 0
            for bundle in player.bank:

                player_total += bundle.value
                bundle_str += f'{bundle.parent_card.type}, {bundle.value}; '
            print(f'Player {player.name} total: {player_total} bank: {bundle_str}')

game = Game(3, 1)
game.play()
