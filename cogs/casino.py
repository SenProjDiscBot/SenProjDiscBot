from datetime import datetime, timedelta
from datetime import time
from msilib.schema import Component
from time import strftime, strptime
from discord import PermissionOverwrite, Embed
from discord_components import (
    DiscordComponents,
    ComponentsBot,
    Button,
    SelectOption,
    Select,
)
from discord.ext import commands
import pymongo
from connect_to_db import connect_to_db
import pytz
import asyncio
from discord.utils import get

from casino.Card import Card
from casino.Deck import Deck
from casino.Shoe import Shoe
from casino.OneCard import OneCard


class casino(commands.Cog):
    def __init__(self, client):
        self.client = client
        DiscordComponents(client)
        # connect to mongo db
        print("Casino connecting to mongoDB....")
        self.db = connect_to_db()
        print("Casino connected to database!")

    @commands.command(name="onecard")
    async def onecard(self, ctx):
        await self.create_emojis(ctx)
        game = OneCard()
        game.add_player(str(ctx.author))
        end_time = datetime.now() + timedelta(seconds=10)
        while datetime.now() < end_time:
            await ctx.send(
                "The dealer is starting a game of one card high.\nClubs > Spades > Diamonds > Hearts",
                components=[Button(label="Hit", style="3", custom_id="hit")],
            )
            # await response
            try:
                ans = await self.client.wait_for(
                    "button_click", timeout=2, check=lambda i: i.custom_id == "hit"
                )
                await self.clear_last_msg(ctx.channel)
                if self.db.check_active(ans.author, ctx.guild.id):
                    game.add_player(str(ans.author))
            except asyncio.TimeoutError:
                await self.clear_last_msg(ctx.channel)
                continue

        game.deal()
        hands = game.get_hands()
        records = self.db.get_employee_records(ctx.guild.id)
        embed = Embed(title="Clubs > Spades > Diamonds > Hearts\nResults:")
        for player, card in hands.items():
            slice = records.find_one({"discord_id": player})
            name = slice["name_first"]
            emj = await self.get_suit(card.get_suit(), ctx)
            retStr = (
                "**"
                + card.get_val()
                + "**"
                + emj
                + " ("
                + str(card.get_oneval())
                + " points)"
            )
            embed.add_field(name=name, value=retStr)

        winner, hand = game.get_winner()
        slice = records.find_one({"discord_id": winner})
        name = slice["name_first"]
        retStr = name + " with a " + hand.get_name()
        embed.add_field(name="Winner:", value=retStr)
        await ctx.send(embed=embed)

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
        async for x in channel.history(limit=1):
            await x.delete()


def setup(client):
    client.add_cog(casino(client))
