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

    await dm.send("Please send discription of bug with screenshot as a reply")
    br = await self.client.wait_for("message", check=check)
    bug_report = br.content
    await dm.send("Your report of a bug will be sent to our team")
    channel = ctx.get_channel(938266823315566592)
    await channel.send(bug_report)
    if await self.guild_null(ctx):
      return
    

    

def setup(client):
  client.add_cog(bugreport(client))