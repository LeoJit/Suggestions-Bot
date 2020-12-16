import discord
from discord import Member
from discord import Reaction
from discord.ext import commands
from discord.ext import tasks
from discord.ext.commands import has_permissions, MissingPermissions
from discord.ext.commands import bot
import asyncio
import random   
import json
import os
import datetime
from datetime import timedelta, datetime

class Schedule(commands.Cog):
    path = os.path.dirname(os.path.realpath(__file__)) + "/"
    def __init__(self, client):
        self.client = client
        self.time_to_open.start()

    @tasks.loop(minutes=1)
    async def time_to_open(self):
        with open(f"{self.path}Setup.json","r") as fp:
            setup_dict = json.load(fp)
            channel3= setup_dict["mod_channel"]
            mods= setup_dict["mod_role"]
            prez=setup_dict["ping_role"]

        with open(f"{self.path}Suggestions.json","r") as fp:
            sug_dict = json.load(fp)

        with open(f"{self.path}userid.json", "r") as fp:
            uid_dict = json.load(fp)

        await self.client.wait_until_ready()  
        timetoformat1 = setup_dict["time"] 
        time1 = datetime.strptime(timetoformat1, "%H:%M")
        now = datetime.utcnow() 
        Time1 = time1.replace(year=now.year, month=now.month, day=now.day)
        time_difference_in_minutes1 = (datetime.utcnow()-Time1) / timedelta(minutes=1)

        if (time_difference_in_minutes1 >= 0.0 and time_difference_in_minutes1 < 1.0):
            l=list(sug_dict)
            if len(l)>1:
                channel_mods= await self.client.fetch_channel(int(channel3))
                await channel_mods.send(f"<@&{mods}>, <@&{prez}> this is your reminder to answer the open suggestions...")
                for i in range(1, (len(l)+1)):
                    user_id= uid_dict[str(l[i-1])]
                    user= await self.client.fetch_user(user_id)
                    head= "**Suggestion #**" + str(l[i-1]) + " from " + str(user)
                    suggestion_msg= sug_dict[str(l[i-1])]
                    suggestion_embed= discord.Embed(title=head, description=suggestion_msg, colour= discord.Colour.teal())
                    channel_mods= await self.client.fetch_channel(int(channel3))
                    await channel_mods.send(content=None, embed=suggestion_embed)

            else:
                await channel_mods.send("@Ref, no open suggestions.")

def setup(client):
    client.add_cog(Schedule(client))
        