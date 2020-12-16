import discord
from discord import Member
from discord import Reaction
from discord.ext import commands
from discord.ext.commands import has_permissions, MissingPermissions
from discord.ext.commands import bot
import asyncio
import random
import json
import os


class Setup(commands.Cog):
    path = os.path.dirname(os.path.realpath(__file__)) + "/"
    def __init__(self, client):
        self.client=client

    @commands.command()
    async def setup(self, ctx):
        with open(f"{self.path}Setup.json","r") as fp:
            setup_dict = json.load(fp)

        a=0
        while a==0:
            await ctx.send("Please input the channel you want to set as the one where the suggestions are posted?")
            channel= await ctx.bot.wait_for("message", check=lambda message: message.author == ctx.author, timeout=60)
            if "<#" in channel.content:
                channel.content = channel.content[2:-1]
            else:
                channel.content = channel.content
            
            if channel.content.isdigit():
                channel_suggestions= await self.client.fetch_channel(int(channel.content))
                setup_dict["suggestion_channel"]= channel_suggestions.id
                a=1
                break

            else:
                await ctx.send("Try again")


        b=0
        while b==0:
            await ctx.send("Please input the channel you want to set as the one where the suggestions are logged?")
            channel2= await ctx.bot.wait_for("message", check=lambda message: message.author == ctx.author, timeout=60)
            if "<#" in channel2.content:
                channel2.content = channel2.content[2:-1]
            else:
                channel2.content = channel2.content

            if channel2.content.isdigit():
                channel_logs= await self.client.fetch_channel(int(channel2.content)) 
                setup_dict["suggestion_logs"]= channel_logs.id
                b=1
                break

            else:
                await ctx.send("Try again")

        
        c=0
        while c==0: 
            await ctx.send("Please input the channel you want to set as the one where the suggestions are posted for mod reviews?")
            channel3= await ctx.bot.wait_for("message", check=lambda message: message.author == ctx.author, timeout=60)
            if "<#" in channel3.content:
                channel3.content = channel3.content[2:-1]
            else:
                channel3.content = channel3.content
            
            if channel3.content.isdigit():
                channel_mods= await self.client.fetch_channel(int(channel3.content)) 
                setup_dict["mod_channel"]= channel_mods.id
                c=1
                break

            else:
                await ctx.send("Try again")


        d=0
        while d==0:
            await ctx.send("Please input the mod role you would like to priviledge?")
            mod_role= await ctx.bot.wait_for("message", check=lambda message: message.author == ctx.author, timeout=60)
            if "<@&" in mod_role.content:
                mod_role.content = mod_role.content[3:-1]
            else:
                mod_role.content = mod_role.content
            
            if mod_role.content.isdigit():
                setup_dict["mod_role"]= int(mod_role.content)
                d=1
                break

            else:
                await ctx.send("Try again")

        g=0
        while g==0:
            await ctx.send("Please input the role you would ping?")
            ping_role= await ctx.bot.wait_for("message", check=lambda message: message.author == ctx.author, timeout=60)
            if "<@&" in mod_role.content:
                ping_role.content = ping_role.content[3:-1]
            else:
                ping_role.content = ping_role.content
            
            if ping_role.content.isdigit():
                setup_dict["ping_role"]= int(ping_role.content)
                d=1
                break

            else:
                await ctx.send("Try again")

        
        e=0
        while e==0:
            await ctx.send("Please input the Nitro Role for suggesting emotes?")
            nitro_role= await ctx.bot.wait_for("message", check=lambda message: message.author == ctx.author, timeout=60)
            if "<@&" in nitro_role.content:
                nitro_role.content = nitro_role.content[3:-1]
            else:
                nitro_role.content = nitro_role.content
            
            if nitro_role.content.isdigit():
                setup_dict["nitro_role"]= int(nitro_role.content)
                e=1
                break

            else:
                await ctx.send("Try again")

        f=0
        while f==0:
            await ctx.send("Please input the guild id?")
            guild= await ctx.bot.wait_for("message", check=lambda message: message.author == ctx.author, timeout=60)

            if guild.content.isdigit():
                setup_dict["Guild"]= int(guild.content)
                f=1
                break

            else:
                ctx.send("Try again.")



        with open(f"{self.path}Setup.json", "w") as f:
                json.dump(setup_dict, f)

        guild = self.client.get_guild(setup_dict["Guild"])
        mod_role1 = discord.utils.get(guild.roles, id=setup_dict["mod_role"])
        '''
        await ctx.send("Setup complete 👌")
        await channel_suggestions.send(f"Suggestions will be sent here")
        await channel_logs.send(f"Suggestions will be logged here")
        await channel_mods.send(f"Suggestions will be moderated here")
        await channel_mods.send(f"<@&{int(mod_role.content)}> is the new moderator role")     
        await channel_mods.send(f"<@&{int(nitro_role.content)}> is the new nitro role")
        '''
def setup(client):
    client.add_cog(Setup(client))



