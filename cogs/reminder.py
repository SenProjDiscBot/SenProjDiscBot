from datetime import datetime
from datetime import time
from discord.ext import commands
from discord import DMChannel


class reminder(commands.Cog):

  def __init__(self,client):
    self.client = client

  async def guild_null(slef, ctx):
    if ctx.guild == None:
      await ctx.send("this command does not work in DM's")
      return True
    return False
    
      

  @commands.command(name='reminder')
  async def reminder(self, ctx):
    dm = await ctx.author.create_dm()
    if await self.guild_null(ctx):
      return
    

    def check(msg):
      return msg.author == ctx.author and msg.channel == dm
    

    await dm.send("When would you like your reminder in minutes? ")
    rt = await self.client.wait_for("message", check=check)
    reminder_time = rt.content

    await ctx.send("what would you like to be reminded of?")
    if await self.guild_null(ctx):
      return


    

def setup(client):
  client.add_cog(reminder(client))
  