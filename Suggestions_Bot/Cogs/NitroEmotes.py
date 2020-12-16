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

class NitroEmotes(commands.Cog):
    path = os.path.dirname(os.path.realpath(__file__)) + "/"
    def __init__(self, client):
        self.client=client

    async def cog_check(self, ctx):
        with open(f"{self.path}Setup.json","r") as fp:
            setup_dict = json.load(fp)
        guild =  self.client.get_guild(setup_dict["Guild"])
        nitro_role = ctx.guild.get_role(setup_dict["nitro_role"])
        return nitro_role in ctx.author.roles

    async def cog_command_error(self, ctx, error):
        if isinstance(error, commands.CheckFailure):
            await ctx.send("Nothing comes for free, dear friend. Only boosters can suggest emotes...")

    
    @commands.command()
    @commands.cooldown(1,86400, commands.BucketType.user)
    async def suggest_emote(self, ctx):
        with open(f"{self.path}Setup.json","r") as fp:
            setup_dict = json.load(fp)
        channel1= setup_dict["suggestion_channel"]

        with open(f"{self.path}emotenames.json","r") as fp:
            emotename_dict = json.load(fp)

        with open(f"{self.path}emoteslink.json","r") as fp:
            emotelink_dict = json.load(fp)

        with open(f"{self.path}userid_emotes.json","r") as fp:
            emoteuid_dict = json.load(fp)

        file= open(f"{self.path}emote_sugnumber.txt", "r")
        a= int(file.read())

        await ctx.message.delete()
        await ctx.send("Sent a message for the emote suggestion")

        await ctx.author.send("Please send the picture of the emotes you wish to be added to the server")
        pict = await ctx.bot.wait_for("message", check=lambda message: message.author == ctx.author and isinstance(message.channel,  discord.channel.DMChannel), timeout=60)
        pic= pict.attachments[0]
        await ctx.author.send("Provide a suitable name for your emote: \n `Format- :nas:`")

        n=0
        while n==0:
            name= await ctx.bot.wait_for("message", check=lambda message: message.author == ctx.author and isinstance(message.channel,  discord.channel.DMChannel), timeout=120)
            if name.content.count(":") >= 2:
                head= "**Emote suggestion #**" + str(a)
                pic_msg= "**" + name.content + "**"
                pic_embed= discord.Embed(title=head, description=pic_msg, colour=discord.Colour.blurple())
                pic_embed.set_image(url= pic.url)
                int1= a
                emotelink_dict[a]= pic.url
                emotename_dict[a]=name.content
                uid= ctx.author.id
                emoteuid_dict[a]=uid
                n=1
                break

            else:
                await ctx.author.send("Please use the format `:nas:`")

        await ctx.author.send("Are you sure you want to suggestion this?")  
        final_emote=await ctx.author.send(content=None, embed=pic_embed)
        await final_emote.add_reaction("✅")
        await final_emote.add_reaction("❌")
        em_list1=['✅', '❌']
        def r_check(reaction: Reaction, user: Member):
            return reaction.message.id == final_emote.id and user == ctx.author and str(reaction.emoji) in em_list1

        try:
            reaction, _ = await ctx.bot.wait_for('reaction_add', check=r_check, timeout=30)
        except asyncio.TimeoutError:
            await ctx.author.send("Sorry, you timed out.")

        if reaction.emoji=="✅":
            await ctx.author.send("Suggestion sent.")
            channel_suggestions= await self.client.fetch_channel(int(channel1))
            await channel_suggestions.send(f"New emote suggestion from {ctx.author.mention}. Please vote.")
            suggestion_final_channel = await channel_suggestions.send(content=None, embed=pic_embed)
            await suggestion_final_channel.add_reaction("👍")
            await suggestion_final_channel.add_reaction("👎")
            em_list2=['👍', '👎']
            def r_check(reaction: Reaction, user: Member):
                return reaction.message.id == suggestion_final_channel.id and user == ctx.author and str(reaction.emoji) in em_list2
            
            with open(f"{self.path}emotenames.json","w") as f:
                json.dump(emotename_dict, f)


            with open(f"{self.path}emoteslink.json","w") as f:
                json.dump(emotelink_dict, f)

            with open(f"{self.path}userid_emotes.json","w") as f:
                json.dump(emoteuid_dict, f)


            b=a+1
            file= open(f"{self.path}emote_sugnumber.txt", "w")
            file.write(str(b))

        if reaction.emoji== '❌':
            await ctx.author.send("Cancelled")
            return

    @suggest_emote.error
    async def suggest_emote_error(self, ctx, exc):
        if isinstance(exc, commands.CommandOnCooldown):
            await ctx.send(f"The command is on cooldown. Try again in {exc.retry_after:,.2f} sec.")

def setup(client):
    client.add_cog(NitroEmotes(client))