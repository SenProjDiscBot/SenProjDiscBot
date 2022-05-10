from cgi import test
from datetime import datetime, timedelta
from datetime import time

import unittest
from casino.Card import Card
from casino.Deck import Deck
from casino.Shoe import Shoe



class TestCasino(unittest.TestCase):
    def __init__(self, *args, **kwargs):
        super(TestCasino, self).__init__(*args, **kwargs)
       
    
    def test_card(self):
        val = "A"
        suit = "H"
        acehearts = Card(val, suit)
        check = (acehearts.get_val() == 'A')
        self.assertTrue(check)

        val = "Q"
        suit = "S"
        queenspades = Card(val, suit)
        check = (queenspades.get_emojicode() == 'QS')
        self.assertTrue(check)

        val = "5"
        suit = "C"
        fiveclubs = Card(val, suit)
        check = (fiveclubs.get_name() == 'Five of Clubs')
        self.assertTrue(check)

        val = "Q"
        suit = "D"
        queendiamonds = Card(val, suit)
        check = (queendiamonds.get_bjval() == 10)
        self.assertTrue(check)

        val = "K"
        suit = "C"
        queendiamonds = Card(val, suit)
        check = (queendiamonds.get_oneval() == 52)
        self.assertTrue(check)

        val = ""
        suit = "sakasdf"
        joker = Card(val, suit)
        check = (joker.get_emojicode() == 'JKR')
        self.assertTrue(check)

    def test_deck(self):
        deck = Deck()
        check = len(deck.get_deck())
        self.assertEqual(check, 52)

    def test_shoe(self):
        shoe = Shoe(2)
        self.assertEqual(shoe.get_cards_left(), 104)
        card = shoe.deal_card()
        print(card.get_emojicode())
        self.assertEqual(type(card), Card)
        self.assertEqual(shoe.get_cards_left(), 103)

        shoe = Shoe(0)
        self.assertEqual(shoe.get_cards_left(), 52)

        shoe = Shoe(-1)
        self.assertEqual(shoe.get_cards_left(), 52)

        shoe = Shoe('Toast')
        self.assertEqual(shoe.get_cards_left(), 52)
        


    
if __name__ == '__main__':
    unittest.main()