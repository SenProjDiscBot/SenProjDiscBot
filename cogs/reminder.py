from datetime import datetime
from http import client
import time
from discord.ext import commands
from discord import DMChannel
import asyncio
import discord
class reminder(commands.Cog):

  def __init__(self,client):
    self.client = client

  async def guild_null(self, ctx):
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
        
    embed = discord.Embed(title="When would you like your reminder(in minutes?) ", color=0x000FF)
    await dm.send(embed=embed)
    rt = await self.client.wait_for("message", check=check)
    reminder_time = rt.content

    while True:
        try:
              is_int = int(rt.content)
              while int(rt.content) < 0:
                  await dm.send("Please enter a POSITIVE INTEGER for your reminder time")
                  rt = await self.client.wait_for("message", check=check)
              break
        except:
              embed = discord.Embed(title="Please enter a POSITIVE INTEGER for your reminder time ", color=0x000FF)
              await dm.send(embed=embed)
              rt = await self.client.wait_for("message", check=check)
              reminder_time = int(rt.content)

    embed = discord.Embed(title="What would you like to be reminded of ? ", color=0x000FF)
    await dm.send(embed=embed)
    rc = await self.client.wait_for("message", check=check)
    reminder_content = rc.content
    embed = discord.Embed(title="you will be reminded to " + reminder_content + " in " + reminder_time + " minutes! ", color=0x000FF)
    await dm.send(embed=embed)
    convertedTime = (int(reminder_time) * 60)
    await asyncio.sleep(convertedTime)
    embed = discord.Embed(title="EZ-Bot was set to remind you to: ", color=0x000FF)
    await dm.send(embed=embed)
    embed = discord.Embed(title=reminder_content, color=0x000FF)
    await dm.send(embed=embed)
    if await self.guild_null(ctx):
      return
    

    

def setup(client):
  client.add_cog(reminder(client))
