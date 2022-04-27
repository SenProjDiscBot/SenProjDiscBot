from casino.Card import Card
from casino.Deck import Deck
from casino.Shoe import Shoe


class OneCard():
    def __init__(self):
        self.players = []
        self.pairs = {}
        self.shoe = Shoe(1)
        self.complete = False


    def add_player(self, player_name):
        if player_name not in self.players:
            self.players.append(player_name)


    def deal(self):
        if len(self.pairs) != 0:
            self.pairs = {}
        for player in self.players:
            self.pairs[player] = self.shoe.deal_card()

    def get_hands(self):
        if len(self.pairs) != 0:
            return self.pairs
    
    def get_winner(self):
        leader = ''
        leader_card = Card('jkr', 'jkr')
        if len(self.pairs) != 0:
            for name, card in self.pairs.items():
                if leader_card.get_oneval() < card.get_oneval():
                    leader = name
                    leader_card = card

        return leader, leader_card