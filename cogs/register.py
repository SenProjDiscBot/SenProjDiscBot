from datetime import datetime
from datetime import time
from discord import DMChannel
from discord.ext import commands
from discord_components import DiscordComponents, ComponentsBot, Button, SelectOption, Select
import pymongo
from connect_to_db import connect_to_db

class register(commands.Cog):

  def __init__(self,client):
    self.client = client
    DiscordComponents(client)
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

    #get timezone
    await dm.send("What is your timezone?", components = [
        Select(
          placeholder = "Timezone",
          options = [
                    SelectOption(label="MIT	Midway Islands Time	GMT-11:00", value='Pacific/Midway'),
                    SelectOption(label="HST	Hawaii Standard Time GMT-10:00", value='US/Hawaii'),
                    SelectOption(label="AST Alaska Standard Time GMT-9:00", value='US/Alaska'),
                    SelectOption(label="PST	Pacific Standard Time	GMT-8:00", value='US/Pacific'),
                    SelectOption(label="MST	Mountain Standard Time GMT-7:00", value='US/Mountain'),
                    SelectOption(label="CST	Central Standard Time	GMT-6:00", value='US/Central'),
                    SelectOption(label="EST	Eastern Standard Time	GMT-5:00", value='US/Eastern'),
                    SelectOption(label="PRT	Puerto Rico and US Virgin Islands Time GMT-4:00", value='America/Puerto_Rico'),
                    SelectOption(label="AGT	Argentina Standard Time	GMT-3:00", value='America/Argentina/Ushuaia'),
                    SelectOption(label="UTC	Universal Coordinated Time GMT+0:00", value='UTC'),
                    SelectOption(label="ECT	European Central Time	GMT+1:00", value='Europe/Rome'),
                    SelectOption(label="EET	Eastern European Time	GMT+2:00", value='Europe/Kiev'),
                    SelectOption(label="EAT	Eastern African Time GMT+3:00", value='Africa/Nairobi'),
                    SelectOption(label="NET	Near East Time GMT+4:00", value='Asia/Dubai'),
                    SelectOption(label="PLT	Pakistan Lahore Time GMT+5:00", value='Asia/Oral'),
                    SelectOption(label="BST	Bangladesh Standard Time GMT+6:00", value='Asia/Bishkek'),
                    SelectOption(label="VST	Vietnam Standard Time	GMT+7:00", value='Asia/Bangkok'),
                    SelectOption(label="CTT	China Taiwan Time	GMT+8:00", value='Asia/Hong_Kong'),
                    SelectOption(label="JST	Japan Standard Time	GMT+9:00", value='Asia/Tokyo'),
                    SelectOption(label="AET	Australia Eastern Time GMT+10:00", value='Australia/Brisbane'),
                    SelectOption(label="SST	Solomon Standard Time	GMT+11:00", value='Australia/Sydney'),
                    SelectOption(label="NST	New Zealand Standard Time	GMT+12:00", value='Pacific/Fiji')
          ],
          custom_id= 'timezone'
          )
      ])
    timezone_interaction = await self.client.wait_for("select_option", check=lambda i: i.custom_id == "timezone" and i.user == ctx.author)
    timezone = timezone_interaction.values[0]
    await self.clear_last_msg(dm)

    #create employee dict
    new_employee = {
        'discord_id' : discord_id,
        'name_first' : first_name,
        'name_last' : last_name,
        'timezone' : timezone
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
    
    #get timezone
    await dm.send("What is your timezone?", components = [
        Select(
          placeholder = "Timezone",
          options = [
                    SelectOption(label="MIT	Midway Islands Time	GMT-11:00", value='Pacific/Midway'),
                    SelectOption(label="HST	Hawaii Standard Time	GMT-10:00", value='US/Hawaii'),
                    SelectOption(label="AST Alaska Standard Time - GMT-9:00", value='US/Alaska'),
                    SelectOption(label="PST	Pacific Standard Time	GMT-8:00", value='US/Pacific'),
                    SelectOption(label="MST	Mountain Standard Time	GMT-7:00", value='US/Mountain'),
                    SelectOption(label="CST	Central Standard Time	GMT-6:00", value='US/Central'),
                    SelectOption(label="EST	Eastern Standard Time	GMT-5:00", value='US/Eastern'),
                    SelectOption(label="PRT	Puerto Rico and US Virgin Islands Time	GMT-4:00", value='America/Puerto_Rico'),
                    SelectOption(label="AGT	Argentina Standard Time	GMT-3:00", value='America/Argentina/Ushuaia'),
                    SelectOption(label="UTC	Universal Coordinated Time	GMT+0:00", value='UTC'),
                    SelectOption(label="ECT	European Central Time	GMT+1:00", value='Europe/Rome'),
                    SelectOption(label="EET	Eastern European Time	GMT+2:00", value='Europe/Kiev'),
                    SelectOption(label="EAT	Eastern African Time	GMT+3:00", value='Africa/Nairobi'),
                    SelectOption(label="NET	Near East Time	GMT+4:00", value='Asia/Dubai'),
                    SelectOption(label="PLT	Pakistan Lahore Time	GMT+5:00", value='Asia/Oral'),
                    SelectOption(label="BST	Bangladesh Standard Time	GMT+6:00", value='Asia/Bishkek'),
                    SelectOption(label="VST	Vietnam Standard Time	GMT+7:00", value='Asia/Bangkok'),
                    SelectOption(label="CTT	China Taiwan Time	GMT+8:00", value='Asia/Hong_Kong'),
                    SelectOption(label="JST	Japan Standard Time	GMT+9:00", value='Asia/Tokyo'),
                    SelectOption(label="AET	Australia Eastern Time	GMT+10:00", value='Australia/Brisbane'),
                    SelectOption(label="SST	Solomon Standard Time	GMT+11:00", value='Australia/Sydney'),
                    SelectOption(label="NST	New Zealand Standard Time	GMT+12:00", value='Pacific/Fiji')
          ],
          custom_id= 'timezone'
          )
      ])
    timezone_interaction = await self.client.wait_for("select_option", check=lambda i: i.custom_id == "timezone" and i.user == ctx.author)
    timezone = timezone_interaction.values[0]
    await self.clear_last_msg(dm)
    

    #store employee in the database
    records.update_one({'discord_id' : discord_id} , {"$set":{'name_first' : first_name, 'name_last' : last_name, 'timezone' : timezone}})

    #post verfication in discord channel
    await dm.send("You have updated your information.")



  async def clear_last_msg(self, channel):
    async for x in channel.history(limit = 1):
      await x.delete()

def setup(client):
  client.add_cog(register(client))
