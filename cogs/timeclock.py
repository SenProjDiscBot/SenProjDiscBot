from code import interact
from datetime import datetime
from datetime import time
from pickle import NONE
from sqlite3 import Timestamp
from time import strftime, strptime

from discord import emoji

from discord_components import DiscordComponents, ComponentsBot, Button, SelectOption, Select

from discord.ext import commands
import pymongo
from connect_to_db import connect_to_db

class timeclock(commands.Cog):

  def __init__(self,client):
    self.client = client
    DiscordComponents(client)



  async def guild_null(self, ctx):
    if ctx.guild == None:
      await ctx.send("This command does not work in direct messages!")
      return True
    return False


  @commands.command(name='in')
  async def clock_in(self, ctx):
    #check if command is not in direct messages
    if await self.guild_null(ctx):
      return

    #get user discord id
    discord_id = str(ctx.author)
  
    #connect to mongoDB
    db = connect_to_db(ctx)

    #open direct message channel with author
    dm = await ctx.author.create_dm()

    #check if discord user is in the database
    if not await db.check_active(ctx):
      await dm.send("You are not registered with this discord server.")
      await dm.send("Please use %register to sign up before clocking in")
      return

    #check if user is already clocked in
    if await db.check_in(ctx):
      await dm.send("You are already clocked in!")
      return

    records = db.get_active_shifts()
    in_time = datetime.now()
    #create employee dict
    new_employee = {
        'discord_id' : discord_id,
        'in_time' : in_time
    }
    #store employee in the database
    records.insert_one(new_employee)

    #post verfication in discord channel
    await dm.send("Your clock in has been successful at " +  str(in_time.strftime('%I:%M:%S %p')))


  @commands.command(name='out')
  async def clock_out(self, ctx):
    # check if command is not in direct messages
    if await self.guild_null(ctx):
      return
    #get user discord id
    discord_id = str(ctx.author)
  
    #connect to mongoDB
    db = connect_to_db(ctx)

    #create direct message channel with author
    dm = await ctx.author.create_dm()

    #check if discord user is already in the database
    if not await db.check_in(ctx):
      await dm.send("You are not clocked in.")
      return

    records = db.get_active_shifts()
    shift_data = records.find_one({'discord_id' : discord_id})
    in_time = shift_data["in_time"]
    out_time = datetime.now()
    total = out_time - in_time
    seconds = total.seconds

    data = {
      'discord_id' : discord_id,
      'in_time' : in_time,
      'out_time' : out_time,
      'seconds_worked' : seconds,
      'comment' : "",
      'paid' : False
    }

    records.delete_one({'discord_id' : discord_id})
    records = db.get_complete_shifts()
    records.insert_one(data)

    await dm.send("You are now clocked out!")
    await dm.send("You worked from " + str(in_time.strftime('%I:%M:%S %p')) + " to " + str(out_time.strftime('%I:%M:%S %p')))
    await dm.send("Time Worked: " + str(total).split(".")[0])

  @commands.command(name='fix')
  async def fix(self, ctx):
    # check if command is not in direct messages
    if await self.guild_null(ctx):
      return

    # helper function that checks if a message is in the authors dm channel
    def check(msg):
      return msg.author == ctx.author and msg.channel == dm

    if await self.guild_null(ctx):
      return
    # get user discord id
    discord_id = str(ctx.author)

    # connect to mongoDB
    db = connect_to_db(ctx)

    # create direct message channel with author
    dm = await ctx.author.create_dm()

    # check if discord user is already in the database
    if not await db.check_complete(ctx):
      await dm.send("You do not have any completed shifts to edit.")
      return

    records = db.get_complete_shifts()
    shifts = records.find({'discord_id': discord_id})

    #get last (most recent)
    shift_data = None
    for shift in shifts:
      shift_data = shift

    in_time = shift_data["in_time"]
    out_time = shift_data["out_time"]
    await dm.send("Your last shift was from " + str(in_time.strftime('%I:%M:%S %p')) + " to " + str(out_time.strftime('%I:%M:%S %p')))
    await dm.send("Which would you like to edit?")
    await dm.send("1. In: " + str(in_time.strftime('%I:%M:%S %p')))
    await dm.send("2. Out: " + str(out_time.strftime('%I:%M:%S %p')))
    await dm.send("3. None")

    ch = await self.client.wait_for("message", check=check)
    choice = ch.content

    while choice != "1" and choice != "2" and choice != "3":
      await dm.send("Selection not recognized:" + choice)
      ch = await self.client.wait_for("message", check=check)
      choice = ch.content
    dt_change = None
    if choice == "1":
      dt_change = in_time
    elif choice == "2":
      dt_change = out_time
    elif choice == "3":
      return

    await dm.send("Which would you like to edit?")
    await dm.send("1. Hours and Minutes")
    await dm.send("2. Minutes")
    await dm.send("3. None")

    hm = await self.client.wait_for("message", check=check)
    hour_minute = hm.content
    while hour_minute != "1" and hour_minute != "2" and hour_minute != "3":
      await dm.send("Selection not recognized")
      hm = await self.client.wait_for("message", check=check)
      hour_minute = hm.content

    if hour_minute == "3":
      return

    val = 100
    new_dt = None
    if hour_minute == "1":
      while val >= 24 or val < 0:
        await dm.send("Value for new hours? (0-23)")
        hm = await self.client.wait_for("message", check=check)
        val = int(hm.content)

      new_min = 100
      while new_min >= 60 or new_min < 0:
        await dm.send("Value for new minutes? (0-59)")
        hm = await self.client.wait_for("message", check=check)
        new_min = int(hm.content)

      new_dt = dt_change.replace(hour=val, minute=new_min, second=0)


    elif hour_minute == "2":
      while val >= 60 or val < 0:
        await dm.send("Value for new minutes? (0-59)")
        hm = await self.client.wait_for("message", check=check)
        val = int(hm.content)

      new_dt = dt_change.replace(minute=val, second=0)

    if choice == "1":
      if new_dt > out_time:
        await dm.send("This would result in your in time coming after your out time. Please try again with a valid in "
                      "time.")
        return
      total = out_time - new_dt
      seconds = total.seconds
      new_val = { "$set": { 'in_time': new_dt, 'seconds_worked': seconds}}
      records.update_one({'discord_id': discord_id, 'out_time': out_time}, new_val)
    elif choice == "2":
      if in_time > new_dt:
        await dm.send("This would result in your in time coming after your out time. Please try again with a valid in "
                      "time.")
        return
      total = new_dt - in_time
      seconds = total.seconds
      new_val = {"$set": {'out_time': new_dt, 'seconds_worked': seconds}}
      records.update_one({'discord_id': discord_id, 'in_time': in_time}, new_val)


    #post verfication in discord channel
    await dm.send("You have changed your most recent time!")
    await dm.send("Old data: " + str(dt_change.strftime('%I:%M %S:%p')))
    await dm.send("New data: " + str(new_dt.strftime('%I:%M:%S %p')))
    


  @commands.command(name='test')
  async def test(self, ctx):
    # create direct message channel with author
    dm = await ctx.author.create_dm()
    await dm.send("", components = [
      Select(
        placeholder = "test",
        options = [
          SelectOption(label="A", value="A"),
          SelectOption(label="B", value="B")
        ],
        custom_id='SelectTesting'
        ),
      Button(label="send", style="3", custom_id="send"),
      Button(label="cancel", style="4", custom_id="end")])
  
    
    send = await self.client.wait_for("button_click", check = lambda i: i.custom_id == "send")
    await send.send(content = "Sent!", ephemeral = False)
    select_interaction = await self.client.wait_for("select_option", check=lambda i: i.custom_id == "SelectTesting" and i.user == ctx.author)
    resp = select_interaction.values[0]
    print(str(resp))



def setup(client):
  client.add_cog(timeclock(client))