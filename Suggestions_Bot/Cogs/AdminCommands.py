import discord
from discord import Member
from discord import Reaction
from discord.ext import commands
from discord.ext.commands import has_permissions, MissingPermissions
from discord.ext.commands import bot
import asyncio
import json
import os
import requests
import io
from PIL import Image
import datetime
from datetime import timedelta, datetime


class AdminCommands(commands.Cog):
    path = os.path.dirname(os.path.realpath(__file__)) + "/"
    def __init__(self, client):
        self.client=client

    async def cog_check(self, ctx):
        return ctx.author.guild_permissions.manage_messages

    async def cog_command_error(self, ctx, error):
        if isinstance(error, commands.CheckFailure):
            await ctx.send("**Error:** You are not allowed to use this command")

    @commands.command()
    async def view(self, ctx, id:int):
        with open(f"{self.path}Setup.json","r") as fp:
                setup_dict = json.load(fp)
        channel3= setup_dict["mod_channel"]
        with open(f"{self.path}Suggestions.json","r") as fp:
            sug_dict = json.load(fp)

        l=list(sug_dict)

        if str(id) in l:
            head= "**Suggestion #**" + str(id)
            suggestion_msg= sug_dict[str(id)]
            suggestion_embed= discord.Embed(title=head, description=suggestion_msg)
            channel_mods= await self.client.fetch_channel(int(channel3))
            await channel_mods.send(content=None, embed=suggestion_embed)

        else:
            await ctx.send(f"No channel found with the suggestion number #{id}")


    @commands.command()
    async def approve(self, ctx, id:int, *,  reason = None):
        with open(f"{self.path}Setup.json","r") as fp:
            setup_dict = json.load(fp)
        channel3= setup_dict["mod_channel"]
        channel2=setup_dict["suggestion_logs"]

        with open(f"{self.path}userid.json", "r") as fp:
            uid_dict = json.load(fp)

        with open(f"{self.path}Suggestions.json","r") as fp:
            sug_dict = json.load(fp)
        

        head1= "**Suggestion #**" + str(id) + " approved"
        approval_msg= sug_dict[str(id)] + "\n\n**Reason from **" + ctx.author.mention + "\n" + reason
        approval_embed= discord.Embed(title=head1, description=approval_msg, colour= discord.Colour.green())
        channel_logs= await self.client.fetch_channel(int(channel2))
        await channel_logs.send(content=None, embed=approval_embed)

        user_id= uid_dict[str(id)]
        user= await self.client.fetch_user(user_id)
        await user.send("Hello. Your suggestion has been approved")
        await user.send(content=None, embed= approval_embed)

        await ctx.send(f"Approved suggestion #{id}")

        uid_dict.pop((str(id)))
        sug_dict.pop((str(id)))

        with open(f"{self.path}Suggestions.json", "w") as fp:
                json.dump(sug_dict, fp)

        with open(f"{self.path}userid.json","w") as fp:
                json.dump(uid_dict, fp)

    @commands.command()
    async def deny(self, ctx, id:int, *, reason=None):
        with open(f"{self.path}Setup.json","r") as fp:
            setup_dict = json.load(fp)
        channel3= setup_dict["mod_channel"]
        channel2=setup_dict["suggestion_logs"]

        with open(f"{self.path}userid.json", "r") as fp:
            uid_dict = json.load(fp)

        with open(f"{self.path}Suggestions.json","r") as fp:
            sug_dict = json.load(fp)


        head2= "**Suggestion #**" + str(id) + " denied"
        denial_msg= sug_dict[str(id)] + "\n\n**Reason from **" + ctx.author.mention + "\n" + reason
        denial_embed= discord.Embed(title=head2, description=denial_msg, colour= discord.Colour.red())
        channel_logs= await self.client.fetch_channel(int(channel2))
        await channel_logs.send(content=None, embed=denial_embed)

        user_id= uid_dict[str(id)]
        user= await self.client.fetch_user(user_id)
        await user.send("Hello. Your suggestion has been denied")
        await user.send(content=None, embed= denial_embed)

        await ctx.send(f"Denied suggestion #{id}")

        uid_dict.pop((str(id)))
        sug_dict.pop((str(id)))

        with open(f"{self.path}Suggestions.json", "w") as fp:
                json.dump(sug_dict, fp)

        with open(f"{self.path}userid.json","w") as fp:
                json.dump(uid_dict, fp)

    @commands.command()
    async def clear_logs(self, ctx):
        with open(f"{self.path}Suggestions.json","r") as fp:
            sug_dict = json.load(fp)

        with open(f"{self.path}userid.json", "r") as fp:
            uid_dict = json.load(fp)

        sug_dict= {}
        uid_dict= {}


        with open(f"{self.path}Suggestions.json", "w") as fp:
                json.dump(sug_dict, fp)
        
        with open(f"{self.path}userid.json","w") as fp:
                json.dump(uid_dict, fp)

        await ctx.send("Logs cleared 👍")


    @commands.command()
    async def view_open(self, ctx):
        with open(f"{self.path}Setup.json","r") as fp:
                setup_dict = json.load(fp)
        channel3= setup_dict["mod_channel"]

        with open(f"{self.path}userid.json", "r") as fp:
            uid_dict = json.load(fp)

        with open(f"{self.path}Suggestions.json","r") as fp:
            sug_dict = json.load(fp)

        l=list(sug_dict)

        if len(l)>0:
            for i in range(1, (len(l)+1)):
                user_id= uid_dict[str(l[i-1])]
                user= await self.client.fetch_user(user_id)
                head= "**Suggestion #**" + str(l[i-1]) + " from " + str(user)
                suggestion_msg= sug_dict[str(l[i-1])]
                suggestion_embed= discord.Embed(title=head, description=suggestion_msg, colour= discord.Colour.teal())
                channel_mods= await self.client.fetch_channel(int(channel3))
                await channel_mods.send(content=None, embed=suggestion_embed)

        else:
            await ctx.send("No open suggestions.")

    @commands.command()
    async def view_open_emotes(self, ctx):
        with open(f"{self.path}Setup.json","r") as fp:
                setup_dict = json.load(fp)
        channel3= setup_dict["mod_channel"]

        with open(f"{self.path}emotenames.json","r") as fp:
            emotename_dict = json.load(fp)

        with open(f"{self.path}emoteslink.json","r") as fp:
            emotelink_dict = json.load(fp)

        with open(f"{self.path}userid_emotes.json","r") as fp:
            emoteuid_dict = json.load(fp)

        l=list(emotename_dict)

        if len(l)>0:
            for i in range(1, (len(l)+1)):
                user_id1= emoteuid_dict[str(l[i-1])]
                user1= await self.client.fetch_user(user_id1)
                head= "**Suggestion #**" + str(l[i-1]) + " from " + str(user1)
                pic_msg= "**" + emotename_dict[str(l[i-1])] + "**"
                pic_embed= discord.Embed(title=head, description=pic_msg)
                pic_embed.set_image(url=emotelink_dict[str(l[i-1])])
                channel_mods= await self.client.fetch_channel(int(channel3))
                await channel_mods.send(content=None, embed=pic_embed)

        else:
            await ctx.send("No open emotes.")

    @commands.command()
    async def approve_emote(self, ctx, id:int):
        with open(f"{self.path}Setup.json","r") as fp:
                setup_dict = json.load(fp)
        channel3= setup_dict["mod_channel"]
        channel2=setup_dict["suggestion_logs"]

        with open(f"{self.path}emotenames.json","r") as fp:
            emotename_dict = json.load(fp)

        with open(f"{self.path}emoteslink.json","r") as fp:
            emotelink_dict = json.load(fp)

        with open(f"{self.path}userid_emotes.json","r") as fp:
            emoteuid_dict = json.load(fp)
        
        head_emote= "**Emote suggestion #**" + str(id) + " approved"
        approval_emote_msg= "**" + emotename_dict[str(id)] + "**"
        approval_emote_embed= discord.Embed(title=head_emote, description=approval_emote_msg, colour= discord.Colour.green())
        approval_emote_embed.set_thumbnail(url= emotelink_dict[str(id)])
        channel_logs= await self.client.fetch_channel(int(channel2))
        guild =  self.client.get_guild(setup_dict["Guild"])
        await channel_logs.send(content=None, embed=approval_emote_embed)
        
        emote= emotename_dict[str(id)]
        emote_name= emote[1:-1]

        img_data = requests.get(emotelink_dict[str(id)]).content
        with open(f"{self.path}emojis\Emote.png", 'wb') as handler:
            handler.write(img_data)

        im =Image.open(f"{self.path}emojis\Emote.png")
        imgByteArr = io.BytesIO()
        im.save(imgByteArr, format=im.format)
        imgByteArr = imgByteArr.getvalue()
        await guild.create_custom_emoji(name=emote_name, image = imgByteArr)
        await ctx.send(f"Added `{emote_name}` to this server.")
        

        user_id= emoteuid_dict[str(id)]
        user= await self.client.fetch_user(user_id)
        await user.send("Hello. Your suggestion has been approved")
        await user.send(content=None, embed= approval_emote_embed)

        await ctx.send(f"Approved suggestion `#{id}`")

        emoteuid_dict.pop((str(id)))
        emotelink_dict.pop((str(id)))
        emotename_dict.pop((str(id)))

        with open(f"{self.path}emotenames.json","w") as f:
                json.dump(emotename_dict, f)

        with open(f"{self.path}emoteslink.json","w") as f:
            json.dump(emotelink_dict, f)

        with open(f"{self.path}userid_emotes.json","w") as f:
            json.dump(emoteuid_dict, f)

    @commands.command()
    async def deny_emote(self, ctx, id:int, *, reason):
        with open(f"{self.path}Setup.json","r") as fp:
                setup_dict = json.load(fp)
        channel3= setup_dict["mod_channel"]
        channel2=setup_dict["suggestion_logs"]

        with open(f"{self.path}emotenames.json","r") as fp:
            emotename_dict = json.load(fp)

        with open(f"{self.path}emoteslink.json","r") as fp:
            emotelink_dict = json.load(fp)

        with open(f"{self.path}userid_emotes.json","r") as fp:
            emoteuid_dict = json.load(fp)


        head2= "**Emote suggestion #**" + str(id) + " denied"
        denial_emote_msg= "**" + emotename_dict[str(id)] + "**" + "\n\n**Reason from **" + ctx.author.mention + "\n" + reason
        denial_reason= "**Reason from **" + ctx.author.mention + "\n" + reason
        denial_emote_embed= discord.Embed(title=head2, description=denial_emote_msg, colour= discord.Colour.red())
        denial_emote_embed.set_thumbnail(url= emotelink_dict[str(id)])
        channel_logs= await self.client.fetch_channel(int(channel2))
        await channel_logs.send(content=None, embed=denial_emote_embed)

        user_id= emoteuid_dict[str(id)]
        user= await self.client.fetch_user(user_id)
        await user.send("Hello. Your suggestion has been denied")
        await user.send(content=None, embed= denial_emote_embed)

        await ctx.send(f"Denied suggestion `#{id}`")

        emoteuid_dict.pop((str(id)))
        emotelink_dict.pop((str(id)))
        emotename_dict.pop(str(id))

        with open(f"{self.path}emotenames.json","w") as f:
                json.dump(emotename_dict, f)

        with open(f"{self.path}emoteslink.json","w") as f:
            json.dump(emotelink_dict, f)

        with open(f"{self.path}userid_emotes.json","w") as f:
            json.dump(emoteuid_dict, f)

    @commands.command()
    async def settings(self, ctx):
        with open(f"{self.path}Setup.json","r") as fp:
                setup_dict = json.load(fp)
        channel3= setup_dict["mod_channel"]
        channel2=setup_dict["suggestion_logs"]
        channel1= setup_dict["suggestion_channel"]
        mod_role= setup_dict["mod_role"]
        booster= setup_dict["nitro_role"]
        prez= setup_dict["ping_role"]
        time= setup_dict["time"]
        guild =  self.client.get_guild(setup_dict["Guild"])

        channels= "**Guild: **" + str(guild) + "\n\n**Channels:**\n" + "**Suggestions Channel: **" + f"<#{int(channel1)}>" + "\n**Suggestions Logs: **" + f"<#{int(channel2)}>" + "\n**Staff Channel: **" + f"<#{int(channel3)}> \n\n" + "**Roles: **\n" + "**Mod Roles: **" + f"<@&{int(mod_role)}>, <@&{int(prez)}>" + "\n**Booster Role: **" + f"<@&{int(booster)}> \n\n" + "**Reminder Time: **" + f"`{time}`"

        settings_embed= discord.Embed(title= "Settings", description= channels, colour= discord.Colour.blue())
        settings_embed.set_footer(text= "Prefix of this bot is `,`")
        await ctx.send(content=None, embed=settings_embed)

    @commands.command()
    async def set_reminder(self, ctx):
        with open(f"{self.path}Setup.json","r") as fp:
            setup_dict = json.load(fp)

        channel3= setup_dict["mod_channel"]
        channel_mods= await self.client.fetch_channel(int(channel3))

        g=0
        while g==0:
            now = datetime.utcnow()
            time1 = datetime.strftime(now, "%H:%M:%S")
            await ctx.send(f"At what time UTC would you want to receive reminders about open suggestions? \n Current time is `{time1}`")
            time= await ctx.bot.wait_for("message", check=lambda message: message.author == ctx.author, timeout=60)

            if time.content.count(":")==1:
                setup_dict["time"]= time.content
                g=1
                break
            else:
                await ctx.send("Please try again...")
        
        with open(f"{self.path}Setup.json", "w") as f:
                json.dump(setup_dict, f)

        await channel_mods.send(f"You will be reminded daily at `{time.content}` UTC :)")
        
    @commands.command()
    async def add_role(self, ctx, role:discord.Role, *args:discord.Member):
        guild= ctx.get_guild()
        role1= ctx.guild.get_role(role)
        for i in range(len(args)):
            await args[i].add_roles(role)
        await ctx.send("Added role")

def setup(client):
    client.add_cog(AdminCommands(client))
