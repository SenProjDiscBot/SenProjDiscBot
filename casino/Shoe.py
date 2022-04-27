import random
from casino.Card import Card
from casino.Deck import Deck

class Shoe():
    def __init__(self, num_decks):
        if type(num_decks) != int or num_decks <= 0:
            num_decks = 1
            
        self.stack = []
        self.num_decks = num_decks
        for x in range(int(num_decks)):
            deck = Deck().get_deck()
            for card in deck:
                self.stack.append(card)

        random.shuffle(self.stack)

    
    def deal_card(self):
        return self.stack.pop()


    def refresh(self):
        self.stack = []
        for x in range(int(self.num_decks)):
            deck = Deck().get_deck()
            for card in deck:
                self.stack.append(card)

        random.shuffle(self.stack)

    def get_cards_left(self):
        return len(self.stack)