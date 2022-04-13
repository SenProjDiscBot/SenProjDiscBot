from datetime import datetime
from http import client
import time
from discord.ext import commands
from discord import DMChannel
import asyncio


class pomodoro(commands.Cog):

  def __init__(self,client):
    self.client = client

  async def guild_null(self, ctx):
    if ctx.guild == None:
      await ctx.send("this command does not work in DM's")
      return True
    return False

  @commands.command(name='pomodoro')
  async def pomodoro(self, ctx):
    dm = await ctx.author.create_dm()
    if await self.guild_null(ctx):
      return
    
    def check(msg):
      return msg.author == ctx.author and msg.channel == dm

    await dm.send("Now entering Pomodoro timer, Please select a task to focus on for 25 minutes!")

    converted_25 = (int(1) * 60)
    converted_5 = (int(1) * 60)
    i = 0
    while i < 16:
      await asyncio.sleep(converted_25)
      await dm.send("please take a 5 minute break")
      await asyncio.sleep(converted_5)
      await dm.send("Your 5 minute pomodoro break is over, please choose another task to focus on for 25 minutes")
      i = i + 1

  @commands.command(name = 'quitpomodoro')
  async def quitpomodoro(self, ctx):
    dm = await ctx.author.create_dm()
    if await self.guild_null(ctx):
      return
    
    def check(msg):
      return msg.author == ctx.author and msg.channel == dm

    await dm.send("Would you like to exit the Pommodoro timer? (Yes/No)")
    qr = await self.client.wait_for("message", check=check)
    if qr.content == 'Yes'or 'yes':
      await dm.send("You have now exited the Pomodoro Timer!")
      quit()
    else:
      await dm.send("You are still in the Pomodoro timer!")

    if await self.guild_null(ctx):
      return
    

    

def setup(client):
  client.add_cog(pomodoro(client))
