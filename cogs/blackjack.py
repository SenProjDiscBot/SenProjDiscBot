from datetime import datetime, timedelta
from datetime import time
from time import strftime, strptime
from discord import PermissionOverwrite, Embed
from discord_components import DiscordComponents, ComponentsBot, Button, SelectOption, Select
from discord.ext import commands
import pymongo
from connect_to_db import connect_to_db
import pytz
import asyncio
from discord.utils import get
from casino.Card import Card
from casino.Deck import Deck
from casino.Shoe import Shoe
from casino.Blackjack import Blackjack

class blackjack(commands.Cog):

    def __init__(self,client):
        self.client = client
        DiscordComponents(client)
        # connect to mongo db
        print("Blackjack connecting to mongoDB....")
        self.db = connect_to_db()
        print("Blackjack connected to database!")   

    @commands.command(name='blackjack')
    async def blackjack(self, ctx):

        await self.create_emojis(ctx)
        game = Blackjack()
        game.check_chips_created(ctx)
        records = self.db.get_employee_records(ctx.guild.id)
        await game.add_player(str(ctx.author), ctx)
        while True:
            end_time = datetime.now() + timedelta(seconds = 30)
            while datetime.now() < end_time:
                embed = Embed(title="Blackjack:")
                embed.add_field(name='Rules', value="Dealer stands on 17\nDealer wins on blackjack\n4x payout for player Black Jack!\nChips are non-refundable once they hit the table.\nRequires 5 custom emoji slots")
                seat1name = game.get_seat_one_nic()
                val =  "Chips:" + str(game.get_seat_one_pool()) + "\nBet: " + str(game.get_seat_one_bet())
                if seat1name == "Empty":
                    val = "Empty"
                    seat1name = "Seat1:"
                embed.add_field(name=seat1name, value = val)

                seat2name = game.get_seat_two_nic()
                val = "Chips:" + str(game.get_seat_two_pool()) + "\nBet: " + str(game.get_seat_two_bet())
                if seat2name == "Empty":
                    val = "Empty"
                    seat2name = "Seat2:"
                embed.add_field(name=seat2name, value = val)

                seat3name = game.get_seat_three_nic()
                val = "Chips:" + str(game.get_seat_three_pool()) + "\nBet: " + str(game.get_seat_three_bet())
                if seat3name == "Empty":
                    val = "Empty"
                    seat3name = "Seat3:"
                embed.add_field(name=seat3name, value = val)

                seat4name = game.get_seat_four_nic()
                val = "Chips:" + str(game.get_seat_four_pool()) + "\nBet: " + str(game.get_seat_four_bet())
                if seat4name == "Empty":
                    val = "Empty"
                    seat4name = "Seat4:"
                embed.add_field(name=seat4name, value = val)
                await ctx.send("", embed = embed, components = [
                    Button(label="Bet 1000", style="3", custom_id="Bet1000"),
                    Button(label="Bet 100", style="3", custom_id="Bet100"),
                    Button(label="Bet 10", style="3", custom_id="Bet10"),
                    Button(label="Leave", style="4", custom_id="Leave"),
                ])
                # await response
                try:
                    ans = await self.client.wait_for("button_click", timeout=12, check = lambda i: i.custom_id == "Bet10" or "Bet100" or "Bet1000" or "Leave")
                    if ans.component.custom_id == "Bet10":
                        if self.db.check_active(str(ans.author), ctx.guild.id):
                            if not str(ans.author) in game.get_players():
                                await game.add_player(str(ans.author), ctx)
                            game.set_bet(str(ans.author), 10)
                    elif ans.component.custom_id == "Bet100":
                        if self.db.check_active(str(ans.author), ctx.guild.id):
                            if not str(ans.author) in game.get_players():
                                await game.add_player(str(ans.author), ctx)
                            game.set_bet(str(ans.author), 100)
                    elif ans.component.custom_id == "Bet1000":
                        if self.db.check_active(str(ans.author), ctx.guild.id):
                            if not str(ans.author) in game.get_players():
                                await game.add_player(str(ans.author), ctx)
                            game.set_bet(str(ans.author), 1000)
                    elif ans.component.custom_id == "Leave":
                        game.leave_player(str(ans.author), ctx)
                    await self.clear_last_msg(ctx.channel)
                except asyncio.TimeoutError:
                    await self.clear_last_msg(ctx.channel)
                    continue
            bets = game.get_seat_four_bet() + game.get_seat_three_bet() + game.get_seat_two_bet() + game.get_seat_one_bet()
            if len(set(game.get_players())) == 1 or bets == 0:
                await ctx.send("No one has made a bet!\nEZ-Bot will step away from the Blackjack table for now.\nUse the blackjack command to resume play.")
                for player in game.get_players():
                    game.leave_player(player, ctx)
                return
            game.start_game()
            while game.is_active():
                embed = await self.create_bj_embed(ctx, game, False)
                #see if dealer wins
                if game.count(game.get_dealer_cards()) == 21:
                    embed = await self.create_bj_embed(ctx, game, True)
                    await ctx.send("", embed = embed)
                    await ctx.send("", embed = game.end_game())
                    await asyncio.sleep(10)
                    continue
    
                # Seat 1
                while game.seat_one_taken and game.seat_one_bet > 0 and game.seat_one_out == False and game.count(game.seat_one) < 21:
                    embed = await self.create_bj_embed(ctx, game, False)
                    await ctx.send("", embed = embed)
                    await ctx.send(game.get_seat_one_nic() + ", you have " + str(game.clean_count(game.get_seat_one_cards())), components = [
                    Button(label="Hit", style="3", custom_id="Hit"),
                    Button(label="Stay", style="4", custom_id="Stay"),
                    ])
                    try:
                        ans = await self.client.wait_for("button_click", timeout=15, check = lambda i: str(i.user) == str(game.get_seat_one_name()) and i.custom_id == "Hit" or "Stay")
                        if str(ans.author) != game.get_seat_one_name():
                            await self.clear_last_msg(ctx.channel)
                            await self.clear_last_msg(ctx.channel)
                            continue
                        elif ans.component.custom_id == "Hit":
                            game.player_hit(str(ans.author))
                            
                        elif ans.component.custom_id == "Stay":
                            game.player_stand(str(ans.author))

                        await self.clear_last_msg(ctx.channel)
                        await self.clear_last_msg(ctx.channel)

                    except asyncio.TimeoutError:
                        await self.clear_last_msg(ctx.channel)
                        await self.clear_last_msg(ctx.channel)
                        await ctx.send(game.get_seat_one_name() + "has timed out.")
                        game.player_stand(game.get_seat_one_name())
                        continue
            
                # Seat 2
                while game.seat_two_taken and game.seat_two_bet > 0 and game.seat_two_out == False and game.count(game.seat_two) < 21:
                    embed = await self.create_bj_embed(ctx, game, False)
                    await ctx.send("", embed = embed)
                    await ctx.send(game.get_seat_two_nic() + ", you have " + str(game.clean_count(game.get_seat_two_cards())), components = [
                    Button(label="Hit", style="3", custom_id="Hit"),
                    Button(label="Stay", style="4", custom_id="Stay"),
                    ])
                    try:
                        ans = await self.client.wait_for("button_click", timeout=15, check = lambda i: str(i.user) == str(game.get_seat_two_name()) and i.custom_id == "Hit" or "Stay")
                        if str(ans.author) != game.get_seat_two_name():
                            await self.clear_last_msg(ctx.channel)
                            await self.clear_last_msg(ctx.channel)
                            continue
                        if ans.component.custom_id == "Hit":
                            game.player_hit(str(ans.author))

                        elif ans.component.custom_id == "Stay":
                            game.player_stand(str(ans.author))

                        await self.clear_last_msg(ctx.channel)
                        await self.clear_last_msg(ctx.channel)

                    except asyncio.TimeoutError:
                        await self.clear_last_msg(ctx.channel)
                        await self.clear_last_msg(ctx.channel)
                        await ctx.send(game.get_seat_two_name() + "has timed out.")
                        game.player_stand(game.get_seat_two_name())
                        continue
                # Seat 3
                while game.seat_three_taken and game.seat_three_bet > 0 and game.seat_three_out == False and game.count(game.seat_three) < 21:
                    embed = await self.create_bj_embed(ctx, game, False)
                    await ctx.send("", embed = embed)
                    await ctx.send(game.get_seat_three_nic() + ", you have " + str(game.clean_count(game.get_seat_three_cards())), components = [
                    Button(label="Hit", style="3", custom_id="Hit"),
                    Button(label="Stay", style="4", custom_id="Stay"),
                    ])
                    try:
                        ans = await self.client.wait_for("button_click", timeout=15, check = lambda i: str(i.user) == str(game.get_seat_three_name()) and i.custom_id == "Hit" or "Stay")
                        if str(ans.author) != game.get_seat_three_name():
                            await self.clear_last_msg(ctx.channel)
                            await self.clear_last_msg(ctx.channel)
                            continue
                        if ans.component.custom_id == "Hit":
                            game.player_hit(str(ans.author))
                            
                        elif ans.component.custom_id == "Stay":
                            game.player_stand(str(ans.author))

                        await self.clear_last_msg(ctx.channel)
                        await self.clear_last_msg(ctx.channel)
                    except asyncio.TimeoutError:
                        await self.clear_last_msg(ctx.channel)
                        await self.clear_last_msg(ctx.channel)
                        await ctx.send(game.get_seat_three_name() + "has timed out.")
                        game.player_stand(game.get_seat_three_name())

                        continue
                # Seat 4
                while game.seat_four_taken and game.seat_four_bet > 0 and game.seat_four_out == False and game.count(game.seat_four) < 21:
                    embed = await self.create_bj_embed(ctx, game, False)
                    await ctx.send("", embed = embed)
                    await ctx.send(game.get_seat_four_nic() + ", you have " + str(game.clean_count(game.get_seat_four_cards())), components = [
                    Button(label="Hit", style="3", custom_id="Hit"),
                    Button(label="Stay", style="4", custom_id="Stay"),
                    ])
                    try:
                        ans = await self.client.wait_for("button_click", timeout=15, check = lambda i: str(i.user) == str(game.get_seat_four_name()) and i.custom_id == "Hit" or "Stay")
                        if str(ans.author) != game.get_seat_four_name():
                            await self.clear_last_msg(ctx.channel)
                            await self.clear_last_msg(ctx.channel)
                            continue
                        if ans.component.custom_id == "Hit":
                            game.player_hit(str(ans.author))
                            
                        elif ans.component.custom_id == "Stay":
                            game.player_stand(str(ans.author))

                        await self.clear_last_msg(ctx.channel)
                        await self.clear_last_msg(ctx.channel)

                    except asyncio.TimeoutError:
                        await self.clear_last_msg(ctx.channel)
                        await self.clear_last_msg(ctx.channel)
                        await ctx.send(game.get_seat_four_name() + "has timed out.")
                        game.player_stand(game.get_seat_four_name())
                        continue
                # Dealer
                embed = await self.create_bj_embed(ctx, game, True)
                await ctx.send("", embed = embed)
                await asyncio.sleep(2)
                while game.count(game.get_dealer_cards()) < 17:
                    
                    game.dealer_hit()
                    embed = await self.create_bj_embed(ctx, game, True)
                    await self.clear_last_msg(ctx.channel)
                    await ctx.send("", embed = embed)
                    await asyncio.sleep(2)
                # end game
                emb = game.end_game()
                await ctx.send("", embed = emb)
                await asyncio.sleep(10)

                """
                try:
                    ans = await self.client.wait_for("button_click", timeout=5, check = lambda i: i.custom_id == "Hit" or "Stay")
                    if ans.component.custom_id == "Hit":
                        if str(ans.author) in game.get_players():
                            game.player_hit(str(ans.author))
                    elif ans.component.custom_id == "Leave":
                        game.leave_player(str(ans.author), ctx)
                    await self.clear_last_msg(ctx.channel)
                except asyncio.TimeoutError:
                    await self.clear_last_msg(ctx.channel)
                    continue
                """


            """        
            hands = game.get_hands()
            records = self.db.get_employee_records(ctx.guild.id)
            embed = Embed(title="Clubs > Spades > Diamonds > Hearts\nResults:")
            for player, card in hands.items():
                slice = records.find_one({'discord_id' : player})
                name = slice['name_first']
                emj = await self.get_suit(card.get_suit(), ctx)
                retStr = "**" + card.get_val() + "**" + emj + " (" + str(card.get_oneval()) + " points)"
                embed.add_field(name=name,value=retStr)
                    
            winner, hand = game.get_winner()
            slice = records.find_one({'discord_id' : winner})
            name = slice['name_first']
            retStr = name + " with a " + hand.get_name()
            embed.add_field(name="Winner:",value=retStr)
            await ctx.send(embed=embed)
            """
    async def create_bj_embed(self, ctx, game, show_dealer):
        embed = Embed(title="Blackjack:")
        val = ""
        for card in game.get_dealer_cards():
            emj = await self.get_suit(card.get_suit(), ctx)
            val = val + "**" + card.get_val() + "**" + emj + "(" + str(card.get_bjval()) + ") "
            if show_dealer == False:
                val = val + "**?**"  + await self.get_suit("B", ctx) + "(?) "
                break
        if val == "":
            val = "None"
        if show_dealer == True:
            total = "\nTotal: " + str(game.count(game.get_dealer_cards()))
            val = val + total
        embed.add_field(name='Dealer:', value=val)

        seat1name = game.get_seat_one_nic()
        chips = "Chips: " + str(game.get_seat_one_pool()) + " Bet: " + str(game.get_seat_one_bet()) + "\n"
        val = ""
        count = str(game.count(game.get_seat_one_cards()))
        for card in game.get_seat_one_cards():
            emj = await self.get_suit(card.get_suit(), ctx)
            val = val + "**" + card.get_val() + "**" + emj + " (" + str(card.get_bjval()) + ") "
        if val == "":
            val = "None"
            chips = ""
        else:
            val = val + "\nTotal: " + count
        val = chips + val
        embed.add_field(name='Seat 1: ' + seat1name, value = val)

        seat2name = game.get_seat_two_nic()
        chips = "Chips: " + str(game.get_seat_two_pool()) + " Bet: " + str(game.get_seat_two_bet()) + "\n"
        val = ""
        count = str(game.count(game.get_seat_two_cards()))
        for card in game.get_seat_two_cards():
            emj = await self.get_suit(card.get_suit(), ctx)
            val = val + "**" + card.get_val() + "**" + emj + " (" + str(card.get_bjval()) + ") "
        if val == "":
            val = "None"
            chips = ""
        else:
            val = val + "\nTotal: " + count
        val = chips + val
        embed.add_field(name='Seat 2: ' + seat2name, value = val)

        seat3name = game.get_seat_three_nic()
        chips = "Chips: " + str(game.get_seat_three_pool()) + " Bet: " + str(game.get_seat_three_bet()) + "\n"
        val = ""
        count = str(game.count(game.get_seat_three_cards()))
        for card in game.get_seat_three_cards():
            emj = await self.get_suit(card.get_suit(), ctx)
            val = val + "**" + card.get_val() + "**" + emj + " (" + str(card.get_bjval()) + ") "
        if val == "":
            val = "None"
            chips = ""
        else:
            val = val + "\nTotal: " + count
        val = chips + val
        embed.add_field(name='Seat 3: ' + seat3name, value = val)

        seat4name = game.get_seat_four_nic()
        chips = "Chips:" + str(game.get_seat_four_pool()) + " Bet: " + str(game.get_seat_four_bet()) + "\n"
        val = ""
        count = str(game.count(game.get_seat_four_cards()))
        for card in game.get_seat_four_cards():
            emj = await self.get_suit(card.get_suit(), ctx)
            val = val + "**" + card.get_val() + "**" + emj + " (" + str(card.get_bjval()) + ") "
        if val == "":
            val = "None"
            chips = ""
        else:
            val = val + "\nTotal: " + count
        val = chips + val
        embed.add_field(name='Seat 4: ' + seat4name, value = val)

        return embed

    async def get_suit(self, suit, ctx):
        emojis = await ctx.guild.fetch_emojis()
        id = 0
        if suit == "H":
            for emoji in emojis:
                if emoji.name == "heart":
                    id = emoji.id
                    return "<:heart:" + str(id) + ">"
        elif suit == "S":
           for emoji in emojis:
                if emoji.name == "spade":
                    id = emoji.id
                    return "<:spade:" + str(id) + ">"
        elif suit == "D":
            for emoji in emojis:
                if emoji.name == "diamond":
                    id = emoji.id
                    return "<:diamond:" + str(id) + ">"
        elif suit == "C":
            for emoji in emojis:
                if emoji.name == "club":
                    id = emoji.id
                    return "<:club:" + str(id) + ">"
        elif suit == "B":
            for emoji in emojis:
                if emoji.name == "back":
                    id = emoji.id
                    return "<:back:" + str(id) + ">"

    async def create_emojis(self, ctx):
        emojis = await ctx.guild.fetch_emojis()
        heart = False
        spade = False
        diamond = False
        club = False
        back = False
        for emoji in emojis:
            if emoji.name == "heart":
                heart = True
            elif emoji.name == "spade":
                spade = True
            elif emoji.name == "diamond":
                diamond = True
            elif emoji.name == "club":
                club = True
            elif emoji.name == "back":
                back = True

        if not heart:
            with open("casino/assets/heart.png", "rb") as image:
                f = image.read()
                b = bytearray(f)
            await ctx.guild.create_custom_emoji(name="heart", image=b)
        if not spade:
            with open("casino/assets/spade.png", "rb") as image:
                f = image.read()
                b = bytearray(f)
            await ctx.guild.create_custom_emoji(name="spade", image=b)
        if not diamond:
            with open("casino/assets/diamond.png", "rb") as image:
                f = image.read()
                b = bytearray(f)
            await ctx.guild.create_custom_emoji(name="diamond", image=b)
        if not club:
            with open("casino/assets/club.png", "rb") as image:
                f = image.read()
                b = bytearray(f)
            await ctx.guild.create_custom_emoji(name="club", image=b)
        if not back:
            with open("casino/assets/back2.png", "rb") as image:
                f = image.read()
                b = bytearray(f)
            await ctx.guild.create_custom_emoji(name="back", image=b)
    
    async def clear_last_msg(self, channel):
        async for x in channel.history(limit = 1):
            await x.delete()

    
def setup(client):
    client.add_cog(blackjack(client))