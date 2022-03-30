# Necessary imports
import discord
from discord.ext import commands

intents = discord.Intents.default()
intents.members = True


class afkCog(commands.Cog):
    # Start of afk command class
    def __init__(self,client):
        self.client = client

    # Start of afk command
    @commands.command()
    async def afk(self, ctx, message = None):
        current_nick = ctx.author.nick

        # Saves users default name as their nick if they do not already have one
        if current_nick == None:
            current_nick = ctx.author.name

        # Checks if user was previously AFK and is trying to run the command again
        # If they were, it takes out the [AFK] and exits the command
        if "[AFK]" in current_nick:
            await ctx.send(f"{ctx.author.mention} is no longer AFK")
            newNick = ctx.author.nick.replace('[AFK]', '')
            await ctx.author.edit(nick=newNick)
            return

        # Checks if user entered a message after running .afk
        if message == None:
            message = None
            await ctx.send(f"{ctx.author.mention} has gone afk.")
        else:
            # Prints more than the first word of the message a user enters if contains more than one word
            message = ctx.message.content.split(' ', 1)[1]
            await ctx.send(f"{ctx.author.mention} has gone afk {message}.")

        try:
            await ctx.author.edit(nick = f"{ctx.author.name} [AFK]")
        except:
            await ctx.send("Unable to change your name")

    # Reads all messages from all users
    @commands.Cog.listener()
    async def on_message(self,message):
        # Gets users nickname
        userName = message.author.nick

      if userName != None:
          # Checks if user has [AFK] in their name
          if "[AFK]" in userName:
              # Checks if user was trying to run the afk command again
              if "!afk" in message.content:
                  pass
              else:
                  # Takes out the [AFK] from the users name
                  newNick = message.author.nick.replace('[AFK]', '')
                  await message.author.edit(nick=newNick)

                  await message.channel.send(f"{message.author.mention} is no longer AFK")

def setup(client):
    client.add_cog(afkCog(client))
