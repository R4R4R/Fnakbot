import discord
from discord.ext import commands
import random
import platform
import time
import datetime
import asyncio
import math
import codecs
import urllib.error
import urllib.request
from urllib.request import urlretrieve
import urllib.parse
import re
from subprocess import Popen
import PIL
from PIL import Image

bot = commands.Bot(command_prefix='f!')

startup_extensions = ["Music","Logs"]

@bot.event
async def on_ready():
	print('Logged in as '+bot.user.name+' (ID:'+bot.user.id+') | Connected to '+str(len(bot.servers))+' servers | Connected to '+str(len(set(bot.get_all_members())))+' users')
	print('Current Discord.py Version: {} | Current Python Version: {}'.format(discord.__version__, platform.python_version()))
	print('Use this link to invite {}:'.format(bot.user.name))
	print('--------')
	print('--------')
	await bot.change_presence(game=discord.Game(name='Fnakball'))
	
	
@bot.command()
async def load(extension_name : str):
    """Loads an extension."""
    try:
        bot.load_extension(extension_name)
    except (AttributeError, ImportError) as e:
        await bot.say("```py\n{}: {}\n```".format(type(e).__name__, str(e)))
        return
    await bot.say("{} loaded.".format(extension_name))

@bot.command()
async def unload(extension_name : str):
    """Unloads an extension."""
    bot.unload_extension(extension_name)
    await bot.say("{} unloaded.".format(extension_name))

@bot.command()
async def add(left : int, right : int):
    """Adds two numbers together."""
    await bot.say(left + right)

@bot.command()
async def repeat(times : int, content='repeating...'):
    """Repeats a message multiple times."""
    for i in range(times):
        await bot.say(content)

if __name__ == "__main__":
    for extension in startup_extensions:
        try:
            bot.load_extension(extension)
        except Exception as e:
            exc = '{}: {}'.format(type(e).__name__, e)
            print('Failed to load extension {}\n{}'.format(extension, exc))
            
##Ping command to check if bot is working
@bot.command(pass_context =True)
async def ping(ctx):
	embed=discord.Embed(description=(":ping_pong: Pong!"), color=0x51719f)
	await bot.say(embed=embed)



bot.run("<token>", bot=True, reconnect=True)
