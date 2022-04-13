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

    await dm.send("You are now attempting pomodoro style efficiency")
    reminder_time = 1
    convertedTime = (int(reminder_time) * 60)#might need to convert to float
    pomodoro_25 = convertedTime * 25
    pomodoro_5 = convertedTime * 5
  
    i = 0
    while i < 16:
        pomodoro1(1)

    async def pomodoro1(i):
      await asyncio.sleep(pomodoro_25)
      await dm.send("please take a 5 minute break")
      await asyncio.sleep(pomodoro_5)
      await dm.send("Your 5 minute pomodoro break is over, please choose another task to focus on for 25 minutes")
      i = i +1
      return i


    if await self.guild_null(ctx):
      return
    

    

def setup(client):
  client.add_cog(pomodoro(client))
