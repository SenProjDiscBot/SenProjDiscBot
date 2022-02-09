from datetime import datetime
from datetime import time
from discord.ext import commands

class timeclock(commands.Cog):

  def __init__(self,client):
    self.client = client

  @commands.command(name='in')
  async def clockIn(self, ctx):
    #build file name from Member class
    name = str(ctx.author)
    file_name = name + ".txt"

    #try to create file
    try:
     file = open(file_name, 'x')
     file.close()
    except:
      print("File already exists")

    #open file in read/write mode
    file = open(file_name, 'r+')
    #parse lines
    var = file.read().split("\n")
    #check if file is empty
    if var[0] != "":
      #check if already clocked in
      last_line = var[len(var) - 2]
      words = last_line.split(" ")
      if words[0] == "in":
        await ctx.send("You are already clocked in")
        file.close()
        return
    #write clock in date and time to file
    now = datetime.now()
    record = "in " + str(now.strftime("%d/%m/%Y %H:%M") + "\n")
    file.write(record)
    file.flush()
    file.close()
    await ctx.send("You are now clocked in starting at: " + str(now.strftime("%d/%m/%Y %H:%M")))


  @commands.command(name='out')
  async def clockOut(self, ctx):
    name = str(ctx.author)
    file_name = name + ".txt"
    try:
     file = open(file_name, 'x')
     file.close()
    except:
      print("File already exists")
    file = open(file_name, 'r+')
    var = file.read().split("\n")

    time = 0;
    now = datetime.now()
    if var[0] != "":
      last_line = var[len(var) - 2]

      words = last_line.split(" ")

      if words[0] == "out":
        await ctx.send("You are not clocked in yet")
        file.close()
        return
      if words[0] == "in":
        in_time = words[2].split(":")
        hours = int(in_time[0])
        minutes = int(in_time[1])
        current_time = now.strftime("%H:%M").split(":")
        c_hours = int(current_time[0])
        c_minutes = int(current_time[1])
        time = c_hours - hours
        time = time + ((c_minutes - minutes)/60)
    record = "out " + str(now.strftime("%d/%m/%Y %H:%M") + "\n")
    file.write(record)
    file.flush()
    file.close()
    await ctx.send("You are clocked out.\nYou worked " + str(time) + " hours.")

  @commands.command(name='hours')
  async def checkHours(self, ctx):
    name = str(ctx.author)
    file_name = name + ".txt"

    file = open(file_name, 'r')
    var = file.read().split("\n")
    ins = 0
    outs = 0
    in_count = 0
    out_count = 0
    last_in_date = ""
    for line in var:
      if line == "":
        continue
      words = line.split(" ")
      hours = words[2].split(":")[0]
      minutes = words[2].split(":")[1]
      if words[0] == "in":
        ins = ins + int(hours) + (int(minutes)/60)
        in_count += 1
      elif words[0] == "out":
        outs = outs + int(hours) + (int(minutes)/ 60)
        out_count+= 1
    time = outs - ins
    file.close()
    if in_count != out_count:
      await ctx.send("Please clock out before checking total hours worked.")
      return

    await ctx.send("You have worked a total of " + str(time) + " hours.")

def setup(client):
  client.add_cog(timeclock(client))