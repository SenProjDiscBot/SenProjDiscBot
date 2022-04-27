

from multiprocessing import pool


class Seat():
    def __init__(self):
        self.cards = []
        self.bet = 0
        self.pool = 0
        self.bust= False
        self.stay = False
        self.discord_id = "Empty"
        self.nickname = "Empty"
        self.seat_taken = False

    def get_cards(self):
        return self.cards

    def add_card(self, card):
        self.cards.append(card)

    def get_bet(self):
        return self.bet
    
    def get_bet(self):
        return self.bet

    def add_bet(self, bet):
        if self.pool >= bet:
            self.bet = self.bet + bet
            self.pool = self.pool - bet
    
    def get_pool(self):
        return self.pool

    def set_pool(self, pool):
        self.pool = pool
    
    def is_bust(self):
        return self.bust

    def set_bust(self, bool):
        self.bust = bool

    def is_stay(self):
        return self.stay

    def set_stay(self, bool):
        self.stay = bool

    def get_disc_id(self):
        return self.discord_id
    
    def set_disc_id(self, id):
        self.discord_id = id

    def get_nic(self):
        return self.nickname
    
    def set_nic(self, nic):
        self.nickname = nic

    def is_taken(self):
        return self.seat_taken

    def set_taken(self, bool):
        self.is_taken = bool

    def reset_hand(self):
        self.cards = []
        self.bet = 0
        self.bust = False
        self.stay = False

    def player_leave(self):
        self.cards = []
        self.bet = 0
        self.pool = 0
        self.bust= False
        self.stay = False
        self.discord_id = "Empty"
        self.nickname = "Empty"
        self.seat_taken = False