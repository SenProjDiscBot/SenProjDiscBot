from datetime import datetime

import time
from discord.ext import commands
from discord import DMChannel
import asyncio
import random
import webbrowser
import discord
from discord.ext.commands import Bot


class weather(commands.Cog):
    def __init__(self, client):
        self.client = client

    async def guild_null(self, ctx):
        if ctx.guild == None:
            await ctx.send("this command does not work in DM's")
            return True
        return False

    @commands.command(name="weather")
    async def weather(self, ctx):

        if await self.guild_null(ctx):
            return

        def check(msg):
            return msg.author == ctx.author and msg.channel

        qrembed = discord.Embed(title="Enter City for weather forecast", color=0x000FF)
        await ctx.send(embed=qrembed)
        weather_city = await self.client.wait_for("message", check=check)
        city = weather_city.content
        url = (
            "https://search.yahoo.com/search?fr=mcafee&type=E211US105G91649&p="
            + city
            + "+weather+today"
        )
        webbrowser.open_new_tab(url)

        if await self.guild_null(ctx):
            return


def setup(client):
    client.add_cog(weather(client))
