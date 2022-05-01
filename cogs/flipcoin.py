from datetime import datetime
from http import client
import time
from discord.ext import commands
from discord import DMChannel
import asyncio
import random
import discord


class flipcoin(commands.Cog):
    def __init__(self, client):
        self.client = client

    async def guild_null(self, ctx):
        if ctx.guild == None:
            await ctx.send("this command does not work in DM's")
            return True
        return False

    @commands.command(name="flipcoin")
    async def flipcoin(self, ctx):
        if await self.guild_null(ctx):
            return

        def check(msg):
            return msg.author == ctx.author and msg.channel

        embed = discord.Embed(title="Please guess either Heads or Tails", color=0x000FF)
        await ctx.send(embed=embed)
        ht = await self.client.wait_for("message", check=check)
        heads_or_tails = str(ht.content)

        if heads_or_tails == "Heads":
            heads_or_tails = "Heads"
        elif heads_or_tails == "HEADS":
            heads_or_tails = "Heads"
        elif heads_or_tails == "heads":
            heads_or_tails = "Heads"
        elif heads_or_tails == "Tails":
            heads_or_tails = "Tails"
        elif heads_or_tails == "TAILS":
            heads_or_tails = "Tails"
        elif heads_or_tails == "tails":
            heads_or_tails = "Tails"
        else:
            q = 0
            while q == 0:
                embed = discord.Embed(
                    title="Please Enter Heads or Tails", color=0x000FF
                )
                await ctx.send(embed=embed)
                ht = await self.client.wait_for("message", check=check)
                heads_or_tails = str(ht.content)
                if heads_or_tails == "Heads":
                    heads_or_tails = "Heads"
                    q = 1
                elif heads_or_tails == "HEADS":
                    heads_or_tails = "Heads"
                    q = 1
                elif heads_or_tails == "heads":
                    heads_or_tails = "Heads"
                    q = 1
                elif heads_or_tails == "Tails":
                    heads_or_tails = "Tails"
                    q = 1
                elif heads_or_tails == "TAILS":
                    heads_or_tails = "Tails"
                    q = 1
                elif heads_or_tails == "tails":
                    heads_or_tails = "Tails"
                    q = 1

        num = random.randint(1, 2)

        if num == 1:
            coin_result = "Heads"
        else:
            coin_result = "Tails"

        if heads_or_tails == coin_result:
            embed1 = discord.Embed(
                title="YOU GUESSED RIGHT!! " + coin_result + " Was correct!",
                color=0x000FF,
            )
            await ctx.send(embed=embed1)
        else:
            embed1 = discord.Embed(
                title="You guessed wrong :/ " + heads_or_tails + " Was inccorrect!",
                color=0x000FF,
            )
            await ctx.send(embed=embed1)
            return
        if await self.guild_null(ctx):
            return


def setup(client):
    client.add_cog(flipcoin(client))
