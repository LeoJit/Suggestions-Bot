import discord
from discord import Member
from discord import Reaction
from discord.ext import commands
from discord.ext.commands import has_permissions, MissingPermissions
from discord.ext.commands import bot
import asyncio
import json
import os
import datetime
from datetime import timedelta, datetime

class User_Commands(commands.Cog):
    path = os.path.dirname(os.path.realpath(__file__)) + "/"
    def __init__(self, client):
        self.client=client

    @commands.command()
    @commands.cooldown(1,86400, commands.BucketType.user)
    async def suggest(self, ctx):
        with open(f"{self.path}Setup.json","r") as fp:
            setup_dict = json.load(fp)
        channel1= setup_dict["suggestion_channel"]

        with open(f"{self.path}Suggestions.json","r") as fp:
            sug_dict = json.load(fp)

        with open(f"{self.path}userid.json", "r") as fp:
            uid_dict=json.load(fp)

        file= open(f"{self.path}sug_number.txt", "r")
        a= int(file.read())

        await ctx.message.delete()
        await ctx.send("Sent a message for the suggestion")
        await ctx.author.send("What is the title of your suggestion?")
        title= await ctx.bot.wait_for("message", check=lambda message: message.author == ctx.author and isinstance(message.channel,  discord.channel.DMChannel), timeout=60)
        

        z=0
        while z==0:
            await ctx.author.send("Provide your suggestion: ")
            suggestion= await ctx.bot.wait_for("message", check=lambda message: message.author == ctx.author and isinstance(message.channel,  discord.channel.DMChannel), timeout=300)
            if suggestion.content.count("https://")==0:
                head= "**Suggestion #**" + str(a)
                suggestion_msg= "**" + title.content + "**\n\n" + suggestion.content
                suggestion_embed= discord.Embed(title=head, description=suggestion_msg, colour=discord.Colour.blurple())
                int1= a
                sug_dict[a]=suggestion_msg
                z=1
                break

            else:
                await ctx.author.send("Thought you could trick a bot huh? Only boosters can suggest emotes dear friend.")

        
        await ctx.author.send("Are you sure you want to suggestion this?")        
        final_suggestion=await ctx.author.send(content=None, embed=suggestion_embed)
        await final_suggestion.add_reaction("✅")
        await final_suggestion.add_reaction("❌")
        em_list1=['✅', '❌']
        def r_check(reaction: Reaction, user: Member):
            return reaction.message.id == final_suggestion.id and user == ctx.author and str(reaction.emoji) in em_list1

        try:
            reaction, _ = await ctx.bot.wait_for('reaction_add', check=r_check, timeout=30)
        except asyncio.TimeoutError:
            await ctx.author.send("Sorry, you timed out.")

        if reaction.emoji=="✅":
            await ctx.author.send("Suggestion sent.")
            aid= ctx.author.id
            uid_dict[a]= aid
            channel_suggestions= await self.client.fetch_channel(int(channel1))
            await channel_suggestions.send(f"New suggestion from {ctx.author.mention}. Please vote.")
            suggestion_final_channel = await channel_suggestions.send(content=None, embed=suggestion_embed)
            await suggestion_final_channel.add_reaction("👍")
            await suggestion_final_channel.add_reaction("👎")
            em_list2=['👍', '👎']
            def r_check(reaction: Reaction, user: Member):
                return reaction.message.id == suggestion_final_channel.id and user == ctx.author and str(reaction.emoji) in em_list2
            
            with open(f"{self.path}Suggestions.json", "w") as f:
                json.dump(sug_dict, f)

            with open(f"{self.path}userid.json", "w") as f:
                json.dump(uid_dict, f)

            b=a+1
            file= open(f"{self.path}sug_number.txt", "w")
            file.write(str(b))

        if reaction.emoji== '❌':
            await ctx.author.send("Cancelled")
            return

    
    @suggest.error
    async def suggest_error(self, ctx, exc):
        if isinstance(exc, commands.CommandOnCooldown):
            await ctx.send(f"The command is on cooldown. Try again in {exc.retry_after:,.2f} sec.")

    @commands.command()
    async def time(self, ctx):
        now= datetime.utcnow()
        date= now.strftime("%d/%m/%Y")
        time1 = datetime.strftime(now, "%H:%M:%S")

        embed= "**Current time: **" + str(time1) + "\n**Current date: **" + str(date)
        time_embed= discord.Embed(title= "Current Coordinated Universal Time", description= embed)
        await ctx.send(content=None, embed= time_embed)
    

def setup(client):
    client.add_cog(User_Commands(client))
            
