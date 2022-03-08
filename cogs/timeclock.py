from datetime import datetime, timedelta
from datetime import time
from time import strftime, strptime
import discord
from discord_components import DiscordComponents, ComponentsBot, Button, SelectOption, Select
from discord.ext import commands
import pymongo
from connect_to_db import connect_to_db
import pytz

class timeclock(commands.Cog):

  def __init__(self,client):
    self.client = client
    DiscordComponents(client)
    # connect to mongo db
    print("Timeclock connecting to mongoDB....")
    self.db = connect_to_db()
    print("Timeclock connected to database!")



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

    #open direct message channel with author
    dm = await ctx.author.create_dm()

    #check if discord user is in the database
    if not await self.db.check_active(ctx):
      await dm.send("You are not registered with this discord server.")
      await dm.send("Please use the 'register' command to sign up before clocking in")
      return

    #check if user is already clocked in
    if await self.db.check_in(ctx):
      await dm.send("You are already clocked in!")
      return

    # verify user has set their timezone
    users = self.db.get_employee_records(ctx)
    userdata = list(users.find({'discord_id' : discord_id, "timezone" : {"$exists":False}}))
    if len(userdata) > 0:
      await dm.send("Please use the 'edit' command to update your timezone before clocking in.")
      return
    records = self.db.get_active_shifts(ctx)

    userdata = users.find_one({'discord_id':discord_id})
    timezone = userdata['timezone']
    timezone_pytz = pytz.timezone(timezone)
    in_time = datetime.now()
    #create employee dict
    new_employee = {
        'discord_id' : discord_id,
        'in_time' : in_time
    }
    #store employee in the database
    records.insert_one(new_employee)

    #post verfication in discord channel
    await dm.send("Your clock in has been successful at " +  str(in_time.astimezone(timezone_pytz).strftime('%I:%M:%S %p')))


  @commands.command(name='out')
  async def clock_out(self, ctx):
    # check if command is not in direct messages
    if await self.guild_null(ctx):
      return
    #get user discord id
    discord_id = str(ctx.author)

    #create direct message channel with author
    dm = await ctx.author.create_dm()

    #check if discord user is clocked in
    if not await self.db.check_in(ctx):
      await dm.send("You are not clocked in.")
      return

    # verify user has set their timezone
    users = self.db.get_employee_records(ctx)
    userdata = list(users.find({'timezone' : {'$exists':False}, 'discord_id' : discord_id }))
    for user in userdata:
      print(user["discord_id"])
    if len(userdata) > 0:
      await dm.send("Please use the 'edit' command to update your timezone before clocking out.")
      return
    records = self.db.get_active_shifts(ctx)
    shift_data = records.find_one({'discord_id' : discord_id})
    
    userdata = users.find_one({'discord_id':discord_id})
    timezone = userdata['timezone']
    timezone_pytz = pytz.timezone(timezone)
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
    records = self.db.get_complete_shifts(ctx)
    records.insert_one(data)

    await dm.send("You are now clocked out!")
    await dm.send("You worked from " + str(in_time.astimezone(timezone_pytz).strftime('%I:%M:%S %p')) + " to " + str(out_time.astimezone(timezone_pytz).strftime('%I:%M:%S %p')))
    await dm.send("Time Worked: " + str(total).split(".")[0])

  @commands.command(name='fix')
  async def fix(self, ctx):
    # check if command is not in direct messages
    if await self.guild_null(ctx):
      return
    # helper function that checks if a message is in the authors dm channel
 
    # get user discord id
    discord_id = str(ctx.author)
    # create direct message channel with author
    dm = await ctx.author.create_dm()

    # check if discord user has completed shifts to edit
    if not await self.db.check_complete(ctx):
      await dm.send("You do not have any completed shifts to edit.")
      return
    
    # get timezone
    users = self.db.get_employee_records(ctx)
    userdata = users.find_one({'discord_id':discord_id})
    timezone = userdata['timezone']
    tzp = pytz.timezone(timezone)

    # get 14 most recent completed shifts table associated with ctx author
    records = self.db.get_complete_shifts(ctx)
    shifts = records.find({'discord_id': discord_id})
    count = 0
    shift_data = []
    for shift in shifts:
      count += 1
      if count > 14:
        break
      # format shift data, create SelectOption, append to list of options (key based on seconds from epoch of in_time)
      outstr = shift["out_time"].astimezone(tzp).strftime("%I:%M %p")
      shift_data.append(SelectOption(label=str(shift["in_time"].astimezone(tzp).strftime('%A %B %d from %I:%M %p to ' + outstr)), value= str(shift["in_time"].timestamp())))

    # build a Select to choose a shift for user to edit and send in dms
    await dm.send("Which shift would you like to edit?", components = [
        Select(
          placeholder = "Shifts",
          options = shift_data,
          custom_id= 'shift'
        )
    ])
    # await response
    shiftans = await self.client.wait_for("select_option", check=lambda i: i.custom_id == "shift" and i.user == ctx.author)

    # use seconds from epoch of chosen option, convert back to date time, use this to search for associated out time
    in_time = datetime.fromtimestamp(float(shiftans.values[0]))
    out_data = records.find_one({"in_time" : in_time, 'discord_id' : discord_id})
    out_time = out_data["out_time"]
   
    # clear spent Select
    await self.clear_last_msg(dm)

    # build a Select to chose to edit the in time or the out time of the chosen shift
    await dm.send("Which would you like to edit?", components = [
        Select(
          placeholder = "In or Out",
          options = [
            SelectOption(label="In: " + str(in_time.astimezone(tzp).strftime('%I:%M:%S %p on %A %B %d')), value= "in"),
            SelectOption(label ="Out: " + str(out_time.astimezone(tzp).strftime('%I:%M:%S %p on %A %B %d')), value = "out")
          ],
          custom_id= 'inout'
        )
    ])
    # await response
    choice1 = await self.client.wait_for("select_option", check=lambda i: i.custom_id == "inout" and i.user == ctx.author)

    # clear spent Select
    await self.clear_last_msg(dm)

    # display the datetime selected for editing
    if choice1.values[0] == "in":
      dt_change = in_time
      await dm.send("You are editing your in time (" + str(in_time.astimezone(tzp).strftime('%I:%M:%S %p on %A %B %d')) + ")")
    else:
      dt_change = out_time
      await dm.send("You are editing your out time (" + str(out_time.astimezone(tzp).strftime('%I:%M:%S %p on %A %B %d')) + ")")
    

    # begin while loop that allows for user verification and re-trial before final submittion      
    try_again = True
    while try_again:
      # build SelectOptions for 24 hour values 12 AM, 1 - 11 AM, 12 PM, 1 - 11 PM in order restricted based on corresponding in/out time
      ops = []

      if choice1.values[0] == "in":
        # 12 AM
        # only append if hour is less than that of out time
        if int(out_time.strftime('%H')) >= 0:
          ops.append(SelectOption(label="12 AM", value=0))
        # 1-11 AM
        for x in range(11):
          label = x+1
          strlable = str(label) + " AM"
          # only append if hour is less than that of out time
          if int(out_time.strftime('%H')) >= label:
            ops.append(SelectOption(label=strlable, value=x + 1))
        # 12 PM
        # only append if hour is less than that of out time
        if int(out_time.strftime('%H')) >= 12:
          ops.append(SelectOption(label="12 PM", value=12))
        # 1-11 PM
        for x in range(11):
          label = x+1
          val = x + 13
          strlable = str(label) + " PM"
          # only append if hour is less than that of out time
          if int(out_time.strftime('%H')) >= val:
            ops.append(SelectOption(label=strlable, value=val))
      else:
        # 12 AM
        # only append if hour is greater than that of in time
        if int(in_time.strftime('%H')) <= 0:
          ops.append(SelectOption(label="12 AM", value=0))
        # 1-11 AM
        for x in range(11):
          label = x+1
          strlable = str(label) + " AM"
          # only append if hour is greater than that of in time
          if int(in_time.strftime('%H')) <= label:
            ops.append(SelectOption(label=strlable, value=x + 1))
        # 12 PM
        # only append if hour is greater than that of in time
        if int(in_time.strftime('%H')) <= 12:
          ops.append(SelectOption(label="12 PM", value=12))
        # 1-11 PM
        for x in range(11):
          label = x+1
          val = x + 13
          strlable = str(label) + " PM"
          # only append if hour is greater than that of in time
          if int(in_time.strftime('%H')) <= val:
            ops.append(SelectOption(label=strlable, value=val))      
      
      # build and send hours Select
      await dm.send("", components = [
        Select(
          placeholder = "Hours",
          options = ops,
          custom_id= 'hours'
          )
      ])
      # await response
      hours_interaction = await self.client.wait_for("select_option", check=lambda i: i.custom_id == "hours" and i.user == ctx.author)
      hourstr = str(hours_interaction.values[0])
      
      # clear spend Select
      await self.clear_last_msg(dm)
      
     
      # Build and send minutes Select with hours from previous answer displayed for clarity
      await dm.send("", components = [
        Select(
          placeholder = "Minutes",
          options = [SelectOption(label=hourstr + ":00", value=0),
          SelectOption(label=hourstr + ":15", value=15),
          SelectOption(label=hourstr + ":30", value=30),
          SelectOption(label=hourstr + ":45", value=45)],
          custom_id= 'minutes'
          )
      ])
      
      minutes_interaction = await self.client.wait_for("select_option", check=lambda i: i.custom_id == "minutes" and i.user == ctx.author)
      # create new datetime value with users responses
      hours = int(hours_interaction.values[0])
      minutes = int(minutes_interaction.values[0])
      new_dt = dt_change.replace(hour= hours, minute= minutes, second=0)
      tz = pytz.timezone('UTC')
      new_dt = new_dt.astimezone(tz)
      # clear spend Select
      await self.clear_last_msg(dm)

      # verify new datetime is correct
      await dm.send(new_dt.astimezone(tzp).strftime('%I:%M:%S %p'))
      await dm.send("Is this correct?", components = [
        Button(label="Yes", style="3", custom_id="send"),
        Button(label="No", style="4", custom_id="again")
      ])
      #await response
      choice = await self.client.wait_for("button_click", check = lambda i: i.custom_id == "send" or "again")
      # clear spent Buttons
      await self.clear_last_msg(dm)
      await self.clear_last_msg(dm)
      # break loop if user confirms verification 
      if choice.component.custom_id == "send":
        try_again = False

        # select in or out
        if choice1.values[0] == "in":
          # verify replacement does not cause in_time to come after out_time resulting in negative hours
          if new_dt.astimezone(tzp) > out_time.astimezone(tzp):
            await dm.send("This would result in your in time coming after your out time. Please try again with a valid in time.")
            # restart loop
            try_again = True
            continue
          else:
            # open dm with boss for verification
            emp_name = self.db.get_employee_records(ctx).find_one({ "discord_id" : discord_id})
            name = emp_name["name_first"] + " " + emp_name["name_last"]
            boss_dm = await ctx.guild.owner.create_dm()
            await boss_dm.send(name + " would like to change a shift on " + new_dt.strftime('%A %B %d'))
            await boss_dm.send("Old shift: " + str(dt_change.astimezone(tzp).strftime('%I:%M:%S %p') + " to " + out_time.astimezone(tzp).strftime('%I:%M:%S %p')))
            await boss_dm.send("New shift: " + str(new_dt.astimezone(tzp).strftime('%I:%M:%S %p') + " to " + out_time.astimezone(tzp).strftime('%I:%M:%S %p')))
            await boss_dm.send("Would you like to allow this?", components = [
              Button(label="Yes", style="3", custom_id="yes"),
              Button(label="No", style="4", custom_id="no")
            ])
            #await response
            await dm.send("Please wait while we aprove this with your boss.")
            boss_choice = await self.client.wait_for("button_click", check = lambda i: i.custom_id == "yes" or "no")
            # clear spent Buttons
            await self.clear_last_msg(boss_dm)
            if boss_choice.component.custom_id == "yes":
              await boss_dm.send("Thank you, I will let " + name + " know their shift has been changed!")
            else:
              await boss_dm.send("Thank you, I will let " + name + " know their shift has not been changed and to contact you if they have any questions as to why.")
              await dm.send("Your boss has declined your timeclock change. Please contact them if you have any concerns as to why.")
              return
  
            # update record with new in_time datetime and total seconds of the shift
            total = out_time.astimezone(tzp) - new_dt.astimezone(tzp)
            seconds = total.seconds
            new_val = { "$set": { 'in_time': new_dt, 'seconds_worked': seconds}}
            records.update_one({'discord_id': discord_id, 'out_time': out_time}, new_val)
            #post verfication in dm
            await dm.send("Your boss has confirmed your timeclock change on " + str(new_dt.strftime('%A %B %d')))
            await dm.send("Old shift: " + str(dt_change.astimezone(tzp).strftime('%I:%M:%S %p') + " to " + out_time.astimezone(tzp).strftime('%I:%M:%S %p')))
            await dm.send("New shift: " + str(new_dt.astimezone(tzp).strftime('%I:%M:%S %p') + " to " + out_time.astimezone(tzp).strftime('%I:%M:%S %p')))

        elif choice1.values[0] == "out":
          if in_time.astimezone(tzp) > new_dt.astimezone(tzp):
            await dm.send("This would result in your in time coming after your out time. Please try again with a valid in time.")
            # restart loop
            try_again = True
            continue
          else:
            # open dm with boss for verification
            emp_name = self.db.get_employee_records(ctx).find_one({ "discord_id" : discord_id})
            name = emp_name["name_first"] + " " + emp_name["name_last"]
            boss_dm = await ctx.guild.owner.create_dm()
            await boss_dm.send(name + " would like to change a shift on " + new_dt.strftime('%A %B %d'))
            await boss_dm.send("Old shift: " + in_time.astimezone(tzp).strftime('%I:%M:%S %p') + " to " + dt_change.astimezone(tzp).strftime('%I:%M:%S %p'))
            await boss_dm.send("New shift: " + in_time.astimezone(tzp).strftime('%I:%M:%S %p') + " to " + new_dt.astimezone(tzp).strftime('%I:%M:%S %p'))
            await boss_dm.send("Would you like to allow this?", components = [
              Button(label="Yes", style="3", custom_id="yes"),
              Button(label="No", style="4", custom_id="no")
            ])
            #await response
            await dm.send("Please wait while we aprove this with your boss.")
            boss_choice = await self.client.wait_for("button_click", check = lambda i: i.custom_id == "yes" or "no")
            # clear spent Buttons
            await self.clear_last_msg(boss_dm)
            if boss_choice.component.custom_id == "yes":
              await boss_dm.send("Thank you, I will let " + name + " know their shift has been changed!")
            else:
              await boss_dm.send("Thank you, I will let " + name + " know their shift has not been changed and to contact you if they have any questions as to why.")
              await dm.send("Your boss has declined your timeclock change. Please contact them if you have any concerns as to why.")
              return
          
            # update record with new out_time datetime and total seconds of the shift
            total = new_dt.astimezone(tzp) - in_time.astimezone(tzp)
            seconds = total.seconds
            new_val = {"$set": {'out_time': new_dt, 'seconds_worked': seconds}}
            records.update_one({'discord_id': discord_id, 'in_time': in_time}, new_val)
            #post verfication in dm
            await dm.send("You have edited your out time on " + str(new_dt.astimezone(tzp).strftime('%A %B %d')))
            await dm.send("Old shift: " + in_time.astimezone(tzp).strftime('%I:%M:%S %p') + " to " + str(dt_change.astimezone(tzp).strftime('%I:%M:%S %p')))
            await dm.send("New shift: " + in_time.astimezone(tzp).strftime('%I:%M:%S %p') + " to " + str(new_dt.astimezone(tzp).strftime('%I:%M:%S %p')))


    
    
  @commands.command(name = 'time')
  async def printtime(self, ctx):
    # open dm channel
    dm = await ctx.author.create_dm()
    # get completed shifts table
    records = self.db.get_complete_shifts(ctx)
    # get timezone
    discord_id = str(ctx.author)
    users = self.db.get_employee_records(ctx)
    userdata = users.find_one({'discord_id':discord_id})
    timezone = userdata['timezone']
    tzp = pytz.timezone(timezone)
    # get shifts associated with author of ctx 
    shifts = records.find({'discord_id': discord_id})
    total = 0
    shift_data = []
    for shift in shifts:
      # format out time
      outstr = shift["out_time"].astimezone(tzp).strftime("%I:%M %p on %A %m-%d")
      # get total seconds, minutes, hours in shift
      s = (shift["out_time"] - shift["in_time"]).total_seconds()
      hours, remainder = divmod(s, 3600)
      minutes, seconds = divmod(remainder, 60)
      # add seconds to running total
      total += s
      # format shift data
      data =  '{:02}:{:02}:{:02}'.format(int(hours), int(minutes), int(seconds))
      # append shift data
      shift_data.append(str(data + " on " + shift["in_time"].astimezone(tzp).strftime('%A %m-%d-%Y from %I:%M %p to ' + outstr)))

    # send shift information in dm  
    for shift in shift_data:
      await dm.send(shift)
    
    # calculate and send total time based on running total of seconds.
    hours, remainder = divmod(total, 3600)
    minutes, seconds = divmod(remainder, 60)
    total_time =  '{:02}:{:02}:{:02}'.format(int(hours), int(minutes), int(seconds))
    await dm.send("Total time: " + total_time)

  
  @commands.command(name = 'clean')
  async def clean(self, ctx):
  # development command that has the bot delete its messages in ctx authors dm's
    dm = await ctx.author.create_dm()
    async for x in dm.history(limit = 1000):
      if x.author == self.client.user:
          await x.delete()


  async def clear_last_msg(self, channel):
    async for x in channel.history(limit = 1):
      await x.delete()


def setup(client):
  client.add_cog(timeclock(client))
