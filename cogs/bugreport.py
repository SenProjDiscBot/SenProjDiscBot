from datetime import datetime
from http import client
import time
from discord.ext import commands
from discord import DMChannel
import asyncio


class bugreport(commands.Cog):

  def __init__(self,client):
    self.client = client

  async def guild_null(self, ctx):
    if ctx.guild == None:
      await ctx.send("this command does not work in DM's")
      return True
    return False
    
      

  @commands.command(name='bugreport')
  async def bugreport(self, ctx):
    dm = await ctx.author.create_dm()
    if await self.guild_null(ctx):
      return
    
    def check(msg):
      return msg.author == ctx.author and msg.channel == dm

    await dm.send("Please post description of bug and pertinent screenshots in Bug-Report Channel")
    br = await self.client.wait_for("message", check=check)
    if await self.guild_null(ctx):
      return
    

    

def setup(client):
  client.add_cog(bugreport(client))