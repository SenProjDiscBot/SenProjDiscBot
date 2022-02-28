from operator import truediv
from typing import Collection
from discord.ext import commands
import pymongo

class connect_to_db():
 
    def __init__(self, ctx):
        #get discord channel id
        discord_channel_id = ctx.guild.id
        #connect to mongoDB
        client = pymongo.MongoClient(
        "mongodb+srv://Danny:qwert123@cluster0.tx7kv.mongodb.net/Cluster0?retryWrites=true&w=majority")
        self.db = client.get_database(str(discord_channel_id))
        
    
    def get_employee_records(self):
        ret = self.db.employee_records
        return ret

    def get_active_shifts(self):
        ret = self.db.active_shifts
        return ret

    def get_complete_shifts(self):
        ret = self.db.complete_shifts
        return ret

    async def check_complete(self, ctx):
    # checks if author of ctx has any completed shifts
        #get user discord id
        discord_id = str(ctx.author)
        records = self.db.complete_shifts

        #check if discord user is already in the database
        slice = len(list(records.find({'discord_id' : discord_id})))

        if slice > 0:
            return True

        return False
    
    async def check_active(self, ctx):
    # checks if author of ctx is a registered user in this servers system
        #get user discord id
        discord_id = str(ctx.author)
        records = self.db.employee_records

        #check if discord user is already in the database
        slice = len(list(records.find({'discord_id' : discord_id})))

        if slice > 0:
            return True

        return False

    async def check_in(self, ctx):
    # checks if author of ctx is clocked in
        #get user discord id
        discord_id = str(ctx.author)
        records = self.db.active_shifts

        #check if discord user is already in the database
        slice = len(list(records.find({'discord_id' : discord_id})))

        if slice > 0:
            return True

        return False