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
	
@commands.has_permissions(ban_members=True)	
@bot.command()
async def load(extension_name : str):
    """Loads an extension."""
    try:
        bot.load_extension(extension_name)
    except (AttributeError, ImportError) as e:
        await bot.say("```py\n{}: {}\n```".format(type(e).__name__, str(e)))
        return
    await bot.say("{} loaded.".format(extension_name))

@commands.has_permissions(ban_members=True)
@bot.command()
async def unload(extension_name : str):
    """Unloads an extension."""
    bot.unload_extension(extension_name)
    await bot.say("{} unloaded.".format(extension_name))

if __name__ == "__main__":
    for extension in startup_extensions:
        try:
            bot.load_extension(extension)
        except Exception as e:
            exc = '{}: {}'.format(type(e).__name__, e)
            print('Failed to load extension {}\n{}'.format(extension, exc))
            
@bot.command(pass_context =True)
async def ping(ctx):
	embed=discord.Embed(description=(":ping_pong: Pong!"), color=0x51719f)
	await bot.say(embed=embed)

##For storing and getting a users 3ds friend code
@bot.command(pass_context =True)
async def fcset(ctx, *tooset):
	readFile = open("fc.txt", "r")
	newfile = readFile.read()
	readFile.close()
	toset = " ".join(tooset)
	username = str(ctx.message.author.id) 
	if newfile.find(username)==-1:
		writeFile = open("fc.txt", "a")
		if newfile != "":
			writeFile.write("\n")
		writeFile.write(username + "="+ str(toset))
		writeFile.close()
	else:
		newfile2 = newfile.splitlines()
		for x in range(len(newfile2)):
			if newfile2[x].find(username)>-1:
				newfile2[x] = (username + "=" + str(toset))
				break
		newfile3 = "\n".join(newfile2)
		writeFile = open("fc.txt", "w")
		writeFile.write(newfile3)
		writeFile.close()
	await bot.say("fc set")

@bot.command(pass_context =True)
async def fc(ctx, member: discord.Member=None):
	readFile = open("fc.txt", "r")
	newfile = readFile.read()
	readFile.close()
	username = str((member or ctx.message.author).id)
	fc = ""
	newfile2 = newfile.splitlines()
	for x in range(len(newfile2)):
		if newfile2[x].find(username)>-1:
			fc = newfile2[x]
			pos = fc.find("=")+1
			fc2 = fc[pos:]
	await bot.say(fc2)

##For storing and getting a users Pokemon Showdown name
@bot.command(pass_context =True)
async def showdownset(ctx, *tooset):
	readFile = open("showdown.txt", "r")
	newfile = readFile.read()
	readFile.close()
	toset = " ".join(tooset)
	username = str(ctx.message.author.id) 
	if newfile.find(username)==-1:
		writeFile = open("showdown.txt", "a")
		if newfile != "":
			writeFile.write("\n")
		writeFile.write(username + "="+ str(toset))
		writeFile.close()
	else:
		newfile2 = newfile.splitlines()
		for x in range(len(newfile2)):
			if newfile2[x].find(username)>-1:
				newfile2[x] = (username + "=" + str(toset))
				break
		newfile3 = "\n".join(newfile2)
		writeFile = open("showdown.txt", "w")
		writeFile.write(newfile3)
		writeFile.close()
	await bot.say("showdown set")

@bot.command(pass_context =True)
async def showdown(ctx, member: discord.Member=None):
	readFile = open("showdown.txt", "r")
	newfile = readFile.read()
	readFile.close()
	username = str((member or ctx.message.author).id)
	sd = ""
	newfile2 = newfile.splitlines()
	for x in range(len(newfile2)):
		if newfile2[x].find(username)>-1:
			sd = newfile2[x]
			pos = sd.find("=")+1
			sd2 = sd[pos:]
	await bot.say(sd2)

##Admin commands
##Kicks a user
@bot.command(pass_context = True)
@commands.has_permissions(kick_members=True)
async def kick(ctx, userName: discord.User):
  """Kick A User from server"""
  await bot.kick(userName)
  await bot.say("They have been kicked")

##Bans a user
@bot.command(pass_context = True)
@commands.has_permissions(ban_members=True)
async def ban(ctx, userName: discord.User):
  """Kick A User from server"""
  await bot.ban(userName)
  await bot.say("They have been banned")
  
##sets the role for when a member joins
@bot.command()
@commands.has_permissions(kick_members=True)
async def autorole(*args):
	args = " ".join(args)
	file = open("autorole.txt", "w")
	file.write(args)
	file.close()
	await bot.say("The autorole is now " + args)
##passively gives a new member their role
@bot.event
async def on_member_join(member):
	file = open("autorole.txt", "r")
	cont = file.read()
	file.close()
	await bot.say(member)
	if cont is not "":
		role = discord.utils.get(member.server.roles, name=cont)
		await bot.add_roles(member, role)


##greets you
@bot.command()
async def hello():
	greet = random.randint(1,4)
	if greet == 1:
		await bot.say("o/")
	elif greet == 2:
		await bot.say("hoi")
	elif greet == 3:
		await bot.say("Hello world!")

##rps
rpsgame = False

@bot.command(pass_context =True)
async def rps(ctx):
        global rpsgame
        print(rpsgame)
        if not rpsgame:
                embed=discord.Embed(description="Let's play a simple game of rock paper scissors, type rock, scissors or paper to play", color=0x51719f)
                await bot.say(embed=embed)
                rpsgame = True
                message = await bot.wait_for_message(timeout=120, author=ctx.message.author, channel=ctx.message.channel)
                if message == None:
                        await bot.say("Timed out")
                else:
                        choicetext = message.content.lower()
                        print(choicetext)
                        botchoice = random.choice(["rock", "paper", "scissors"])
                        if choicetext == "rock":
                                await bot.say("Fnakbot chose " + botchoice)
                                if botchoice == "rock":
                                        await bot.say("We tied")
                                elif botchoice == "paper":
                                        await bot.say("Fnakbot won")
                                else:
                                        await bot.say("You won")
                        elif choicetext == "paper":
                                await bot.say("Fnakbot chose " + botchoice)
                                if botchoice == "paper":
                                        await bot.say("We tied")
                                elif botchoice == "scissors":
                                        await bot.say("Fnakbot won")
                                else:
                                        await bot.say("You won")
                        elif choicetext == "scissors":
                                await bot.say("Fnakbot chose " + botchoice)
                                if botchoice == "scissors":
                                        await bot.say("We tied")
                                elif botchoice == "rock":
                                        await bot.say("Fnakbot won")
                                else:
                                        await bot.say("You won")
                        else:
                                await bot.say("I guess I win")
                rpsgame = False

@commands.has_permissions(ban_members=True)
@bot.command(pass_context =True)
async def avatar(ctx, url):
	urlretrieve(url, 'avatar.jpg')
	with open('avatar.jpg', 'rb') as f:
   		await bot.edit_profile(avatar=f.read())


bot.run("<token>", bot=True, reconnect=True)
