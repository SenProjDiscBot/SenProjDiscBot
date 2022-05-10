from casino.Card import Card
from casino.Deck import Deck
from casino.Shoe import Shoe
from connect_to_db import connect_to_db
from discord import Embed


class Blackjack:
    def __init__(self):
        # connect to mongo db
        print("BJ connecting to mongoDB....")
        self.db = connect_to_db()
        print("BJ connected to database!")

        self.dealer = []
        self.seat_one = []
        self.seat_one_bet = 0
        self.seat_one_pool = 0
        self.seat_one_out = False
        self.seat_one_player = "Empty"
        self.seat_one_nic = "Empty"
        self.seat_one_taken = False
        self.seat_two = []
        self.seat_two_bet = 0
        self.seat_two_pool = 0
        self.seat_two_out = False
        self.seat_two_player = "Empty"
        self.seat_two_nic = "Empty"
        self.seat_two_taken = False
        self.seat_three = []
        self.seat_three_bet = 0
        self.seat_three_pool = 0
        self.seat_three_out = False
        self.seat_three_player = "Empty"
        self.seat_three_nic = "Empty"
        self.seat_three_taken = False
        self.seat_four = []
        self.seat_four_bet = 0
        self.seat_four_pool = 0
        self.seat_four_out = False
        self.seat_four_player = "Empty"
        self.seat_four_nic = "Empty"
        self.seat_four_taken = False
        self.seats = [self.seat_one, self.seat_two, self.seat_three, self.seat_four]
        self.names = [
            self.seat_one_player,
            self.seat_two_player,
            self.seat_three_player,
            self.seat_four_player,
        ]
        self.shoe = Shoe(7)
        self.game_active = False

    async def add_player(self, player_name, ctx):
        if not player_name in self.names:
            records = self.db.get_employee_records(ctx.guild.id)
            userdata = records.find_one({"discord_id": player_name})
            if userdata == None:
                return
            if "Empty" in self.names:
                if self.seat_one_player == "Empty":
                    self.seat_one_player = player_name
                    self.seat_one_nic = userdata["name_first"]
                    self.seat_one_taken = True
                    self.seat_one_pool = userdata["chips"]
                    self.names = [
                        self.seat_one_player,
                        self.seat_two_player,
                        self.seat_three_player,
                        self.seat_four_player,
                    ]

                elif self.seat_two_player == "Empty":
                    self.seat_two_player = player_name
                    self.seat_two_nic = userdata["name_first"]
                    self.seat_two_taken = True
                    self.seat_two_pool = userdata["chips"]
                    self.names = [
                        self.seat_one_player,
                        self.seat_two_player,
                        self.seat_three_player,
                        self.seat_four_player,
                    ]

                elif self.seat_three_player == "Empty":
                    self.seat_three_player = player_name
                    self.seat_three_nic = userdata["name_first"]
                    self.seat_three_taken = True
                    self.seat_three_pool = userdata["chips"]
                    self.names = [
                        self.seat_one_player,
                        self.seat_two_player,
                        self.seat_three_player,
                        self.seat_four_player,
                    ]

                elif self.seat_four_player == "Empty":
                    self.seat_four_player = player_name
                    self.seat_four_nic = userdata["name_first"]
                    self.seat_four_taken = True
                    self.seat_four_pool = userdata["chips"]
                    self.names = [
                        self.seat_one_player,
                        self.seat_two_player,
                        self.seat_three_player,
                        self.seat_four_player,
                    ]

            else:
                ret = (
                    "All seats are taken. Sorry "
                    + userdata["name_first"]
                    + ". You will have to wait for a seat to open up."
                )
                await ctx.send(ret)

    def leave_player(self, player_name, ctx):
        if player_name in self.names:
            records = self.db.get_employee_records(ctx.guild.id)
            if not self.db.check_active(player_name, ctx.guild.id):
                return
            if self.seat_one_player == player_name:
                self.seat_one_player = "Empty"
                self.seat_one_nic = "Empty"
                self.seat_one_taken = False
                records.update_one(
                    {"discord_id": player_name}, {"$set": {"chips": self.seat_one_pool}}
                )
                self.seat_one_pool = 0
                self.names = [
                    self.seat_one_player,
                    self.seat_two_player,
                    self.seat_three_player,
                    self.seat_four_player,
                ]

            elif self.seat_two_player == player_name:
                self.seat_two_player = "Empty"
                self.seat_two_nic = "Empty"
                self.seat_two_taken = False
                records.update_one(
                    {"discord_id": player_name}, {"$set": {"chips": self.seat_two_pool}}
                )
                self.seat_two_pool = 0
                self.names = [
                    self.seat_one_player,
                    self.seat_two_player,
                    self.seat_three_player,
                    self.seat_four_player,
                ]

            elif self.seat_three_player == player_name:
                self.seat_three_player = "Empty"
                self.seat_three_nic = "Empty"
                self.seat_three_taken = False
                records.update_one(
                    {"discord_id": player_name},
                    {"$set": {"chips": self.seat_three_pool}},
                )
                self.seat_three_pool = 0
                self.names = [
                    self.seat_one_player,
                    self.seat_two_player,
                    self.seat_three_player,
                    self.seat_four_player,
                ]

            elif self.seat_four_player == player_name:
                self.seat_four_player = "Empty"
                self.seat_four_nic = "Empty"
                self.seat_four_taken = False
                records.update_one(
                    {"discord_id": player_name},
                    {"$set": {"chips": self.seat_four_pool}},
                )
                self.seat_four_pool = 0
                self.names = [
                    self.seat_one_player,
                    self.seat_two_player,
                    self.seat_three_player,
                    self.seat_four_player,
                ]

    def get_seat_one_pool(self):
        return self.seat_one_pool

    def get_seat_two_pool(self):
        return self.seat_two_pool

    def get_seat_three_pool(self):
        return self.seat_three_pool

    def get_seat_four_pool(self):
        return self.seat_four_pool

    def get_seat_one_bet(self):
        return self.seat_one_bet

    def get_seat_two_bet(self):
        return self.seat_two_bet

    def get_seat_three_bet(self):
        return self.seat_three_bet

    def get_seat_four_bet(self):
        return self.seat_four_bet

    def get_seat_one_taken(self):
        return self.seat_one_taken

    def get_seat_two_taken(self):
        return self.seat_two_taken

    def get_seat_three_taken(self):
        return self.seat_three_taken

    def get_seat_four_taken(self):
        return self.seat_four_taken

    def set_seat_one_out(self):
        self.seat_one_out = True

    def set_seat_two_out(self):
        self.seat_two_out = True

    def set_seat_three_out(self):
        self.seat_three_out = True

    def set_seat_four_out(self):
        self.seat_four_out = True

    def get_seat_one_out(self):
        return self.seat_one_out

    def get_seat_two_out(self):
        return self.seat_two_out

    def get_seat_three_out(self):
        return self.seat_three_out

    def get_seat_four_out(self):
        return self.seat_four_out

    def get_seat_one_name(self):
        return self.seat_one_player

    def get_dealer_cards(self):
        return self.dealer

    def get_seat_one_cards(self):
        return self.seat_one

    def get_seat_two_name(self):
        return self.seat_two_player

    def get_seat_two_cards(self):
        return self.seat_two

    def get_seat_three_name(self):
        return self.seat_three_player

    def get_seat_three_cards(self):
        return self.seat_three

    def get_seat_four_name(self):
        return self.seat_four_player

    def get_seat_four_cards(self):
        return self.seat_four

    def get_seat_one_nic(self):
        return self.seat_one_nic

    def get_seat_two_nic(self):
        return self.seat_two_nic

    def get_seat_three_nic(self):
        return self.seat_three_nic

    def get_seat_four_nic(self):
        return self.seat_four_nic

    def get_players(self):
        return self.names

    def start_game(self):
        if not self.game_active:
            self.game_active = True
            # strange order/repitition for proper blackjack dealing rng though in the end it doesnt matter
            self.dealer.append(self.shoe.deal_card())
            if self.seat_one_bet > 0:
                self.seat_one.append(self.shoe.deal_card())
            if self.seat_two_bet > 0:
                self.seat_two.append(self.shoe.deal_card())
            if self.seat_three_bet > 0:
                self.seat_three.append(self.shoe.deal_card())
            if self.seat_four_bet > 0:
                self.seat_four.append(self.shoe.deal_card())
            self.dealer.append(self.shoe.deal_card())
            if self.seat_one_bet > 0:
                self.seat_one.append(self.shoe.deal_card())
            if self.seat_two_bet > 0:
                self.seat_two.append(self.shoe.deal_card())
            if self.seat_three_bet > 0:
                self.seat_three.append(self.shoe.deal_card())
            if self.seat_four_bet > 0:
                self.seat_four.append(self.shoe.deal_card())

    def get_hands(self):
        hands = {}
        if self.game_active:
            hands["Dealer"] = self.dealer
            if len(self.seat_one) > 0:
                hands[self.seat_one_player] = self.seat_one
            if len(self.seat_two) > 0:
                hands[self.seat_two_player] = self.seat_two
            if len(self.seat_three) > 0:
                hands[self.seat_three_player] = self.seat_three
            if len(self.seat_four) > 0:
                hands[self.seat_four_player] = self.seat_four
        return hands

    def end_game(self):
        embed = Embed(title="Results:", color=0x000FF)

        self.game_active = False
        # dealer bust - pay people who didnt bust
        if self.count(self.dealer) > 21:
            if self.seat_one_bet > 0:
                val = ""
                if self.count(self.seat_one) <= 21 and self.seat_one_bet > 0:
                    self.seat_one_pool = self.seat_one_pool + (2 * self.seat_one_bet)
                    val = "Player 1 wins " + str(2 * self.seat_one_bet) + " chips!"
                else:
                    val = "Player 1 also bust."
                embed.add_field(name=self.seat_one_nic, value=val)
            if self.seat_two_bet > 0:
                val = ""
                if self.count(self.seat_two) <= 21 and self.seat_two_bet > 0:
                    self.seat_two_pool = self.seat_two_pool + (2 * self.seat_two_bet)
                    val = "Player 2 wins " + str(2 * self.seat_two_bet) + " chips!"
                else:
                    val = "Player 2 also bust."
                embed.add_field(name=self.seat_two_nic, value=val)
            if self.seat_three_bet > 0:
                val = ""
                if self.count(self.seat_three) <= 21 and self.seat_three_bet > 0:
                    self.seat_three_pool = self.seat_three_pool + (
                        2 * self.seat_three_bet
                    )
                    val = "Player 3 wins " + str(2 * self.seat_three_bet) + " chips!"
                else:
                    val = "Player 3 also bust."
                embed.add_field(name=self.seat_three_nic, value=val)
            if self.seat_four_bet > 0:
                val = ""
                if self.count(self.seat_four) <= 21 and self.seat_four_bet > 0:
                    self.seat_four_pool = self.seat_four_pool + (2 * self.seat_four_bet)
                    val = "Player 4 wins " + str(2 * self.seat_four_bet) + " chips!"
                else:
                    val = "Player 4 also bust."
                embed.add_field(name=self.seat_four_nic, value=val)
                val = ""
            self.reset_game()
            return embed

        # case dealer 21 everyone loses
        elif self.count(self.dealer) == 21 and len(self.dealer) == 2:
            embed.add_field(
                name="Dealer hit blackjack!",
                value="Players who also hit blackjack will push.",
            )
        if self.seat_one_bet > 0:
            # seat 1 bust
            if self.count(self.seat_one) > 21:
                embed.add_field(
                    name=self.seat_one_nic, value="Player 1 has gone bust..."
                )
            # seat 1 push
            elif self.count(self.seat_one) == self.count(self.dealer):
                self.seat_one_pool = self.seat_one_pool + self.seat_one_bet
                embed.add_field(
                    name=self.seat_one_nic, value="Player 1 pushes with the dealer."
                )
            # seat 1 win
            elif self.count(self.seat_one) > self.count(self.dealer):
                p1val = ""
                if self.count(self.seat_one) == 21 and len(self.seat_one) == 2:
                    self.seat_one_bet = self.seat_one_bet * 2
                    p1val = "BLACKJACK!\n"
                self.seat_one_pool = self.seat_one_pool + (2 * self.seat_one_bet)
                p1val = (
                    p1val + "Player 1 wins " + str(2 * self.seat_one_bet) + " chips!"
                )
                embed.add_field(name=self.seat_one_nic, value=p1val)
            # seat 1 not bust but lose
            else:
                embed.add_field(name=self.seat_one_nic, value="Player 1 loses.")
        if self.seat_two_bet > 0:
            # seat 2 bust
            if self.count(self.seat_two) > 21:
                embed.add_field(
                    name=self.seat_two_nic, value="Player 2 has gone bust..."
                )
            # seat 2 push
            elif self.count(self.seat_two) == self.count(self.dealer):
                self.seat_two_pool = self.seat_two_pool + self.seat_two_bet
                embed.add_field(
                    name=self.seat_two_nic, value="Player 2 pushes with the dealer."
                )
            # seat 2 win
            elif self.count(self.seat_two) > self.count(self.dealer):
                p2val = ""
                if self.count(self.seat_two) == 21 and len(self.seat_two) == 2:
                    self.seat_two_bet = self.seat_two_bet * 2
                    p2val = "BLACKJACK!\n"
                self.seat_two_pool = self.seat_two_pool + (2 * self.seat_two_bet)
                p2val = (
                    p2val + "Player 2 wins " + str(2 * self.seat_two_bet) + " chips!"
                )
                embed.add_field(name=self.seat_two_nic, value=p2val)
            # seat 2 not bust but lose
            else:
                embed.add_field(name=self.seat_two_nic, value="Player 2 loses.")

        if self.seat_three_bet > 0:
            # seat 3 bust
            if self.count(self.seat_three) > 21:
                embed.add_field(
                    name=self.seat_three_nic, value="Player 3 has gone bust..."
                )
            # seat 3 push
            elif self.count(self.seat_three) == self.count(self.dealer):
                self.seat_three_pool = self.seat_three_pool + self.seat_three_bet
                embed.add_field(
                    name=self.seat_three_nic, value="Player 3 pushes with the dealer."
                )
            # seat 3 win
            elif self.count(self.seat_three) > self.count(self.dealer):
                p3val = ""
                if self.count(self.seat_three) == 21 and len(self.seat_three) == 2:
                    self.seat_three_bet = self.seat_three_bet * 2
                    p3val = "BLACKJACK!\n"
                self.seat_three_pool = self.seat_three_pool + (2 * self.seat_three_bet)
                p3val = (
                    p3val + "Player 3 wins " + str(2 * self.seat_three_bet) + " chips!"
                )
                embed.add_field(name=self.seat_three_nic, value=p3val)
            # seat 3 not bust but lose
            else:
                embed.add_field(name=self.seat_three_nic, value="Player 3 loses.")

        if self.seat_four_bet > 0:
            # seat 4 bust
            if self.count(self.seat_four) > 21:
                embed.add_field(
                    name=self.seat_four_nic, value="Player 4 has gone bust..."
                )
            # seat 4 push
            elif self.count(self.seat_four) == self.count(self.dealer):
                self.seat_four_pool = self.seat_four_pool + self.seat_four_bet
                embed.add_field(
                    name=self.seat_four_nic, value="Player 4 pushes with the dealer."
                )
            # seat 4 win
            elif self.count(self.seat_three) > self.count(self.dealer):
                p4val = ""
                if self.count(self.seat_four) == 21 and len(self.seat_four) == 2:
                    self.seat_four_bet = self.seat_four_bet * 2
                    p4val = "BLACKJACK!\n"
                self.seat_four_pool = self.seat_four_pool + (2 * self.seat_four_bet)
                p4val = (
                    p4val + "Player 4 wins " + str(2 * self.seat_four_bet) + " chips!"
                )
                embed.add_field(name=self.seat_four_nic, value=p4val)
            # seat 4 not bust but lose
            else:
                embed.add_field(name=self.seat_four_nic, value="Player 4 loses.")

        self.reset_game()
        return embed

    """
    def player_alive(self, player_name):
        if player_name in self.names:
            if self.seat_one_player == player_name and self.seat_one_bet > 0:
                self.seat_one.append(self.shoe.deal_card())

            elif self.seat_two_player == player_name and self.seat_two_bet > 0:
                self.seat_two.append(self.shoe.deal_card())

            elif self.seat_three_player == player_name and self.seat_three_bet > 0:
                self.seat_three.append(self.shoe.deal_card())

            elif self.seat_four_player == player_name and self.seat_four_bet > 0:
                self.seat_four.append(self.shoe.deal_card())
    """

    def count(self, hand):
        total = 0
        counted = []
        for card in hand:
            counted.append(card)
            if (total + card.get_bjval()) > 21:
                for card2 in counted:
                    if card2.get_changable():
                        card2.change_ace()
                        break
                total = self.clean_count(counted)
            else:
                total = total + card.get_bjval()
        return total

    def clean_count(self, hand):
        total = 0
        for card in hand:
            total = total + card.get_bjval()
        return total

    def hand_counter(self, player_name):
        if player_name in self.names:
            if self.seat_one_player == player_name and len(self.seat_one) > 0:
                total = 0
                for card in self.seat_one:
                    if (total + card.get_bjval()) > 21:
                        for card in self.seat_one:
                            if card.get_changable():
                                total = total - 10
                                card.change_ace()
                                break
                    total = total + card.get_bjval()
                if total > 21:
                    self.seat_one_out = True
                return total

            elif self.seat_two_player == player_name and len(self.seat_two) > 0:
                total = 0
                for card in self.seat_two:
                    if (total + card.get_bjval()) > 21:
                        for card in self.seat_two:
                            if card.get_changable():
                                total = total - 10
                                card.change_ace()
                                break
                    total = total + card.get_bjval()
                if total > 21:
                    self.seat_two_out = True
                return total

            elif self.seat_three_player == player_name and len(self.seat_three) > 0:
                total = 0
                for card in self.seat_three:
                    if (total + card.get_bjval()) > 21:
                        for card in self.seat_three:
                            if card.get_changable():
                                total = total - 10
                                card.change_ace()
                                break
                    total = total + card.get_bjval()
                if total > 21:
                    self.seat_three_out = True
                return total

            elif self.seat_four_player == player_name and len(self.seat_four) > 0:
                total = 0
                for card in self.seat_four:
                    if (total + card.get_bjval()) > 21:
                        for card in self.seat_four:
                            if card.get_changable():
                                total = total - 10
                                card.change_ace()
                                break
                    total = total + card.get_bjval()
                if total > 21:
                    self.seat_four_out = True
                return total

    def dealer_hit(self):
        self.dealer.append(self.shoe.deal_card())
        self.count(self.dealer)

    def player_hit(self, player_name):
        if player_name in self.names:
            if (
                self.seat_one_player == player_name
                and self.seat_one_bet > 0
                and self.hand_counter(player_name) < 21
            ):
                self.seat_one.append(self.shoe.deal_card())
                if self.count(self.seat_one) >= 21:
                    self.seat_one_out = True

            elif (
                self.seat_two_player == player_name
                and self.seat_two_bet > 0
                and self.hand_counter(player_name) < 21
            ):
                self.seat_two.append(self.shoe.deal_card())
                if self.count(self.seat_two) >= 21:
                    self.seat_two_out = True

            elif (
                self.seat_three_player == player_name
                and self.seat_three_bet > 0
                and self.hand_counter(player_name) < 21
            ):
                self.seat_three.append(self.shoe.deal_card())
                if self.count(self.seat_three) >= 21:
                    self.seat_three_out = True

            elif (
                self.seat_four_player == player_name
                and self.seat_four_bet > 0
                and self.hand_counter(player_name) < 21
            ):
                self.seat_four.append(self.shoe.deal_card())
                if self.count(self.seat_four) >= 21:
                    self.seat_four_out = True

    def player_stand(self, player_name):
        if player_name in self.names:
            if self.seat_one_player == player_name:
                self.seat_one_out = True

            elif self.seat_two_player == player_name:
                self.seat_two_out = True

            elif self.seat_three_player == player_name:
                self.seat_three_out = True

            elif self.seat_four_player == player_name:
                self.seat_four_out = True

    def set_bet(self, player_name, bet):
        if player_name in self.names:
            if self.seat_one_player == player_name:
                if self.seat_one_pool >= bet:
                    self.seat_one_bet = self.seat_one_bet + bet
                    self.seat_one_pool = self.seat_one_pool - bet
                    self.seat_one_out = False

            elif self.seat_two_player == player_name:
                if self.seat_two_pool >= bet:
                    self.seat_two_bet = self.seat_two_bet + bet
                    self.seat_two_pool = self.seat_two_pool - bet
                    self.seat_two_out = False

            elif self.seat_three_player == player_name:
                if self.seat_three_pool >= bet:
                    self.seat_three_bet = self.seat_three_bet + bet
                    self.seat_three_pool = self.seat_three_pool - bet
                    self.seat_three_out = False

            elif self.seat_four_player == player_name:
                if self.seat_four_pool >= bet:
                    self.seat_four_bet = self.seat_four_bet + bet
                    self.seat_four_pool = self.seat_four_pool - bet
                    self.seat_four_out = False

    def update_chips(self, ctx):
        users = self.db.get_employee_records(ctx.guild.id)

    def reset_game(self):
        self.dealer = []
        self.seat_one = []
        self.seat_one_bet = 0
        self.seat_one_out = False
        self.seat_two = []
        self.seat_two_bet = 0
        self.seat_two_out = False
        self.seat_three = []
        self.seat_three_bet = 0
        self.seat_three_out = False
        self.seat_four = []
        self.seat_four_bet = 0
        self.seat_four_out = False

    def is_active(self):
        return self.game_active

    def deal(self):
        if len(self.pairs) != 0:
            self.pairs = {}
        for player in self.players:
            self.pairs[player] = self.shoe.deal_card()

    def check_chips_created(self, ctx):
        users = self.db.get_employee_records(ctx.guild.id)
        userdata = users.find({"chips": {"$exists": False}})
        for user in userdata:
            users.update_one(
                {"discord_id": user["discord_id"]}, {"$set": {"chips": 1000}}
            )
