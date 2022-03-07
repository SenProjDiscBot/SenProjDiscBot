from datetime import datetime
from datetime import time
from discord import DMChannel
from discord.ext import commands
import pymongo
from connect_to_db import connect_to_db

class register(commands.Cog):

  def __init__(self,client):
    self.client = client
    # connect to mongo db
    print("Register connecting to mongoDB....")
    self.db = connect_to_db()
    print("Register connected to database!")



  async def guild_null(self, ctx):
    if ctx.guild == None:
      await ctx.send("This command does not work in direct messages!")
      return True
    return False


  @commands.command(name='register')
  async def register(self, ctx):
    # check if command is not in direct messages
    if await self.guild_null(ctx):
      return
    #get user discord id
    discord_id = str(ctx.author)
  
    #connect to mongoDB
    records = self.db.get_employee_records(ctx)

    #check if discord user is already in the database
    if await self.db.check_active(ctx):
      await ctx.send("You are already in this database.")
      return

    #open a dm channel with user
    dm = await ctx.author.create_dm()

    #helper function that checks if a message is in the authors dm channel
    def check(msg):
      return msg.author == ctx.author and msg.channel == dm

    #get first name
    await dm.send("First Name?")
    fn = await self.client.wait_for("message", check=check)
    first_name = fn.content

    #get last name
    await dm.send("Last Name?")
    ln = await self.client.wait_for("message", check=check)
    last_name = ln.content

    #create employee dict
    new_employee = {
        'discord_id' : discord_id,
        'name_first' : first_name,
        'name_last' : last_name
    }
    #store employee in the database
    records.insert_one(new_employee)

    #post verfication in discord channel
    await ctx.send(first_name + " " + last_name + " created in the database.")



  @commands.command(name='edit')
  async def edit(self, ctx):
    # check if command is not in direct messages
    if await self.guild_null(ctx):
      return
    #get user discord id
    discord_id = str(ctx.author)

    #get mongoDB table
    records = self.db.get_employee_records(ctx)
    #check if discord user is already in the database
    if not await self.db.check_active(ctx):
      return

    #open a dm channel with user
    dm = await ctx.author.create_dm()

    #helper function that checks if a message is in the authors dm channel
    def check(msg):
      return msg.author == ctx.author and msg.channel == dm
    old = records.find_one({'discord_id' : discord_id})
    old_first = old['name_first']
    old_last = old['name_last']

    #get first name
    await dm.send("Current: " + old_first + "\nFirst Name?")
    fn = await self.client.wait_for("message", check=check)
    first_name = fn.content

    #get last name
    await dm.send("Current: " + old_last + "\nLast Name?")
    ln = await self.client.wait_for("message", check=check)
    last_name = ln.content

    #store employee in the database
    records.update_one({'discord_id' : discord_id} , {"$set":{'name_first' : first_name, 'name_last' : last_name}})

    #post verfication in discord channel
    await dm.send("You have updated your information.")


def setup(client):
  client.add_cog(register(client))
