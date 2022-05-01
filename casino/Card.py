class Card:
    def __init__(self, val, suit):
        check = str(val) + str(suit)
        self.changabe = False
        if check == "AH":
            self.suit = "H"
            self.val = "A"
            self.bjval = 11
            self.changabe = True
            self.oneval = 1
            self.name = "Ace of Hearts"
            self.emoji_code = "AH"
        elif check == "2H":
            self.suit = "H"
            self.val = "2"
            self.bjval = 2
            self.oneval = 2
            self.name = "Two of Hearts"
            self.emoji_code = "2H"
        elif check == "3H":
            self.suit = "H"
            self.val = "3"
            self.bjval = 3
            self.oneval = 3
            self.name = "Three of Hearts"
            self.emoji_code = "3H"
        elif check == "4H":
            self.suit = "H"
            self.val = "4"
            self.bjval = 4
            self.oneval = 4
            self.name = "Four of Hearts"
            self.emoji_code = "4H"
        elif check == "5H":
            self.suit = "H"
            self.val = "5"
            self.bjval = 5
            self.oneval = 5
            self.name = "Five of Hearts"
            self.emoji_code = "5H"
        elif check == "6H":
            self.suit = "H"
            self.val = "6"
            self.bjval = 6
            self.oneval = 6
            self.name = "Six of Hearts"
            self.emoji_code = "6H"
        elif check == "7H":
            self.suit = "H"
            self.val = "7"
            self.bjval = 7
            self.oneval = 7
            self.name = "Seven of Hearts"
            self.emoji_code = "7H"
        elif check == "8H":
            self.suit = "H"
            self.val = "8"
            self.bjval = 8
            self.oneval = 8
            self.name = "Eight of Hearts"
            self.emoji_code = "8H"
        elif check == "9H":
            self.suit = "H"
            self.val = "9"
            self.bjval = 9
            self.oneval = 9
            self.name = "Nine of Hearts"
            self.emoji_code = "9H"
        elif check == "0H":
            self.suit = "H"
            self.val = "10"
            self.bjval = 10
            self.oneval = 10
            self.name = "Ten of Hearts"
            self.emoji_code = "0H"
        elif check == "JH":
            self.suit = "H"
            self.val = "J"
            self.bjval = 10
            self.oneval = 11
            self.name = "Jack of Hearts"
            self.emoji_code = "JH"
        elif check == "QH":
            self.suit = "H"
            self.val = "Q"
            self.bjval = 10
            self.oneval = 12
            self.name = "Queen of Hearts"
            self.emoji_code = "QH"
        elif check == "KH":
            self.suit = "H"
            self.val = "K"
            self.bjval = 10
            self.oneval = 13
            self.name = "King of Hearts"
            self.emoji_code = "KH"
        elif check == "AD":
            self.suit = "D"
            self.val = "A"
            self.bjval = 11
            self.changabe = True
            self.oneval = 14
            self.name = "Ace of Diamonds"
            self.emoji_code = "AD"
        elif check == "2D":
            self.suit = "D"
            self.val = "2"
            self.bjval = 2
            self.oneval = 15
            self.name = "Two of Diamonds"
            self.emoji_code = "2D"
        elif check == "3D":
            self.suit = "D"
            self.val = "3"
            self.bjval = 3
            self.oneval = 16
            self.name = "Three of Diamonds"
            self.emoji_code = "3D"
        elif check == "4D":
            self.suit = "D"
            self.val = "4"
            self.bjval = 4
            self.oneval = 17
            self.name = "Four of Diamonds"
            self.emoji_code = "4D"
        elif check == "5D":
            self.suit = "D"
            self.val = "5"
            self.bjval = 5
            self.oneval = 18
            self.name = "Five of Diamonds"
            self.emoji_code = "5D"
        elif check == "6D":
            self.suit = "D"
            self.val = "6"
            self.bjval = 6
            self.oneval = 19
            self.name = "Six of Diamonds"
            self.emoji_code = "6D"
        elif check == "7D":
            self.suit = "D"
            self.val = "7"
            self.bjval = 7
            self.oneval = 20
            self.name = "Seven of Diamonds"
            self.emoji_code = "7D"
        elif check == "8D":
            self.suit = "D"
            self.val = "8"
            self.bjval = 8
            self.oneval = 21
            self.name = "Eight of Diamonds"
            self.emoji_code = "8D"
        elif check == "9D":
            self.suit = "D"
            self.val = "9"
            self.bjval = 9
            self.oneval = 22
            self.name = "Nine of Diamonds"
            self.emoji_code = "9D"
        elif check == "0D":
            self.suit = "D"
            self.val = "10"
            self.bjval = 10
            self.oneval = 23
            self.name = "Ten of Diamonds"
            self.emoji_code = "0D"
        elif check == "JD":
            self.suit = "D"
            self.val = "J"
            self.bjval = 10
            self.oneval = 24
            self.name = "Jack of Diamonds"
            self.emoji_code = "JD"
        elif check == "QD":
            self.suit = "D"
            self.val = "Q"
            self.bjval = 10
            self.oneval = 25
            self.name = "Queen of Diamonds"
            self.emoji_code = "QD"
        elif check == "KD":
            self.suit = "D"
            self.val = "K"
            self.bjval = 10
            self.oneval = 26
            self.name = "King of Diamonds"
            self.emoji_code = "KD"
        elif check == "AS":
            self.suit = "S"
            self.val = "A"
            self.bjval = 11
            self.changabe = True
            self.oneval = 27
            self.name = "Ace of Spades"
            self.emoji_code = "AS"
        elif check == "2S":
            self.suit = "S"
            self.val = "2"
            self.bjval = 2
            self.oneval = 28
            self.name = "Two of Spades"
            self.emoji_code = "2S"
        elif check == "3S":
            self.suit = "S"
            self.val = "3"
            self.bjval = 3
            self.oneval = 29
            self.name = "Three of Spades"
            self.emoji_code = "3S"
        elif check == "4S":
            self.suit = "S"
            self.val = "4"
            self.bjval = 4
            self.oneval = 30
            self.name = "Four of Spades"
            self.emoji_code = "4S"
        elif check == "5S":
            self.suit = "S"
            self.val = "5"
            self.bjval = 5
            self.oneval = 31
            self.name = "Five of Spades"
            self.emoji_code = "5S"
        elif check == "6S":
            self.suit = "S"
            self.val = "6"
            self.bjval = 6
            self.oneval = 32
            self.name = "Six of Spades"
            self.emoji_code = "6S"
        elif check == "7S":
            self.suit = "S"
            self.val = "7"
            self.bjval = 7
            self.oneval = 33
            self.name = "Seven of Spades"
            self.emoji_code = "7S"
        elif check == "8S":
            self.suit = "S"
            self.val = "8"
            self.bjval = 8
            self.oneval = 34
            self.name = "Eight of Spades"
            self.emoji_code = "8S"
        elif check == "9S":
            self.suit = "S"
            self.val = "9"
            self.bjval = 9
            self.oneval = 35
            self.name = "Nine of Spades"
            self.emoji_code = "9D"
        elif check == "0S":
            self.suit = "S"
            self.val = "10"
            self.bjval = 10
            self.oneval = 36
            self.name = "Ten of Spades"
            self.emoji_code = "0S"
        elif check == "JS":
            self.suit = "S"
            self.val = "J"
            self.bjval = 10
            self.oneval = 37
            self.name = "Jack of Spades"
            self.emoji_code = "JS"
        elif check == "QS":
            self.suit = "S"
            self.val = "Q"
            self.bjval = 10
            self.oneval = 38
            self.name = "Queen of Spades"
            self.emoji_code = "QS"
        elif check == "KS":
            self.suit = "S"
            self.val = "K"
            self.bjval = 10
            self.oneval = 39
            self.name = "King of Spades"
            self.emoji_code = "KS"
        elif check == "AC":
            self.suit = "C"
            self.val = "A"
            self.bjval = 11
            self.changabe = True
            self.oneval = 40
            self.name = "Ace of Clubs"
            self.emoji_code = "AC"
        elif check == "2C":
            self.suit = "C"
            self.val = "2"
            self.bjval = 2
            self.oneval = 41
            self.name = "Two of Clubs"
            self.emoji_code = "2C"
        elif check == "3C":
            self.suit = "C"
            self.val = "3"
            self.bjval = 3
            self.oneval = 42
            self.name = "Three of Clubs"
            self.emoji_code = "3C"
        elif check == "4C":
            self.suit = "C"
            self.val = "4"
            self.bjval = 4
            self.oneval = 43
            self.name = "Four of Clubs"
            self.emoji_code = "4C"
        elif check == "5C":
            self.suit = "C"
            self.val = "5"
            self.bjval = 5
            self.oneval = 44
            self.name = "Five of Clubs"
            self.emoji_code = "5C"
        elif check == "6C":
            self.suit = "C"
            self.val = "6"
            self.bjval = 6
            self.oneval = 45
            self.name = "Six of Clubs"
            self.emoji_code = "6C"
        elif check == "7C":
            self.suit = "C"
            self.val = "7"
            self.bjval = 7
            self.oneval = 46
            self.name = "Seven of Clubs"
            self.emoji_code = "7C"
        elif check == "8C":
            self.suit = "C"
            self.val = "8"
            self.bjval = 8
            self.oneval = 47
            self.name = "Eight of Clubs"
            self.emoji_code = "8C"
        elif check == "9C":
            self.suit = "C"
            self.val = "9"
            self.bjval = 9
            self.oneval = 48
            self.name = "Nine of Clubs"
            self.emoji_code = "9C"
        elif check == "0C":
            self.suit = "C"
            self.val = "10"
            self.bjval = 10
            self.oneval = 49
            self.name = "Ten of Clubs"
            self.emoji_code = "0C"
        elif check == "JC":
            self.suit = "C"
            self.val = "J"
            self.bjval = 10
            self.oneval = 50
            self.name = "Jack of Clubs"
            self.emoji_code = "JC"
        elif check == "QC":
            self.suit = "C"
            self.val = "Q"
            self.bjval = 10
            self.oneval = 51
            self.name = "Queen of Clubs"
            self.emoji_code = "QC"
        elif check == "KC":
            self.suit = "C"
            self.val = "K"
            self.bjval = 10
            self.oneval = 52
            self.name = "King of Clubs"
            self.emoji_code = "KC"
        else:
            self.suit = "J"
            self.val = "JKR"
            self.bjval = 0
            self.oneval = 0
            self.name = "JOKER"
            self.emoji_code = "JKR"

    def get_suit(self):
        return self.suit

    def get_val(self):
        return self.val

    def get_bjval(self):
        return self.bjval

    def get_name(self):
        return self.name

    def get_emojicode(self):
        return self.emoji_code

    def get_oneval(self):
        return self.oneval

    def get_changable(self):
        return self.changabe

    def change_ace(self):
        if self.changabe:
            if self.val == "A":
                if self.bjval == 11:
                    self.bjval = 1
                    self.changabe = False
