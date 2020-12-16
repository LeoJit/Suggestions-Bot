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



client=commands.Bot(command_prefix=',') 
path = os.path.dirname(os.path.realpath(__file__)) + "/"

@client.event
async def on_ready():
    await client.change_presence(activity=discord.Game(name="Suggestions | ,help"))
    print("Bot ready!")


@client.command(hidden=True)
async def unload(ctx, extension):
    client.unload_extension(f"Cogs.{extension}")
    await ctx.send(f"Unloaded {extension} 🔓")

@client.command(hidden=True)
async def load(ctx, extension):
    client.load_extension(f"Cogs.{extension}")
    await ctx.send(f"Loaded {extension} 🔒")

@client.command(hidden=True)
async def reload(ctx, extension):
    client.unload_extension(f"Cogs.{extension}")
    client.load_extension(f"Cogs.{extension}")
    await ctx.send(f"Reloaded {extension} 🔃")

for filename in os.listdir(r"C:\Users\leoji\Desktop\Python\Suggestions_Bot\Cogs"):
    if filename.endswith(".py"):
        client.load_extension(f"Cogs.{filename[:-3]}")

file= open(f"{path}Token", "r")
token=str(file.read())

client.run(token)
