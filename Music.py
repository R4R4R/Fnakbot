import discord
from discord.ext import commands
import random
import platform
import time
import datetime
import asyncio
import math
import codecs
import urllib.request
import urllib.parse
import re
from subprocess import Popen

player = None
player2 = None
voice = None
channel = None
musicList = []
start_time = 0
elapsed_time = 0
skips = 0
currentSong = ""
notDownloading = True
mp3 = False
auto4 = True
switched = False

class Music():

	def __init__(self,bot):
		self.bot = bot
	
	async def on_ready(self):
		global voice
		global start_time
		voice = await self.bot.join_voice_channel(self.bot.get_channel('478334246813958145'))
		global channel
		channel = self.bot.get_channel('478334246813958145')
		global player
		beforeArgs = "-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5" 
		player = await voice.create_ytdl_player('https://www.youtube.com/watch?v=RN3Ulf84eRs', pipe=False, before_options=beforeArgs, after=lambda: my_after())
		start_time = time.time()
		player.volume = 0.3
		self.autotest()
		player.start()
		
	def restarted(self):
	            global player
	            if player is not None:
	                    for x in self.bot.voice_clients:
	                                    player.after = None
	                                    asyncio.run_coroutine_threadsafe(x.disconnect(), self.bot.loop)
										
	def autotest(self):
			asyncio.run_coroutine_threadsafe(self.autotest2(), self.bot.loop)
			asyncio.run_coroutine_threadsafe(self.autotest3(), self.bot.loop)
				
	
	@commands.command(pass_context =True)
	async def join(self, ctx):
            if str(ctx.message.author.id) == "218852384976273418":
                    self.restarted()
                    global voice
                    global start_time
                    voice = await self.bot.join_voice_channel(ctx.message.author.voice_channel)
                    global channel
                    channel = ctx.message.author.voice_channel
                    global player
                    beforeArgs = "-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5" 
                    player = await voice.create_ytdl_player('https://www.youtube.com/watch?v=RN3Ulf84eRs', pipe=False, before_options=beforeArgs, after=lambda: self.my_after())
                    start_time = time.time()
                    player.volume = 0.3
                    self.autotest()
                    player.start()

   
	async def autotest2(self):
            while True:
                    await asyncio.sleep(10)
                    global player
                    global elapsed_time
                    global start_time
                    elapsed_time = time.time() - start_time
                    seconds = int(player.duration) - elapsed_time +20
                    if seconds < 0:
                            await self.nextSong()
                    if notDownloading:
                            await self.nextSong()
							
	async def autotest3(self):
		while True:
			await asyncio.sleep(1)
			pipe.stdout.flush()
            
	async def nextSong(self):
			global player
			global voice 
			global musicList
			global start_time
			global elapsed_time
			global skips
			global notDownloading
			global mp3
			global auto4
			global switched
			if not mp3:
				elapsed_time = time.time() - start_time
				seconds = int(player.duration) - elapsed_time - 1
			if mp3:
				elapsed_time = time.time() - start_time
				seconds = int(8897) - elapsed_time
			if (len(musicList) > 0 and player.is_done()) or (len(musicList) > 0 and mp3) :
					notDownloading = False
					skips = 0
					player.after = None
					player.stop()
					player = musicList[0]
					musicList.pop(0)
					start_time = time.time()
					elapsed_time = 0
					mp3 = False
					notDownloading = True
					await self.bot.change_presence(game=discord.Game(name=player.title))
					player.volume = 0.3
					player.start()
			elif player.is_done() or seconds < 0 or switched:
					if auto4:
						notDownloading = False
						switched = False
						skips = 0
						player.after = None
						player.stop()
						player = voice.create_ffmpeg_player("auto.mp3", pipe=False, after=lambda: self.my_after())
						mp3 = True
						start_time = time.time()
						elapsed_time = 0
						notDownloading = True
						await self.bot.change_presence(game=discord.Game(name="R's auto"))
						player.volume = 0.3
						player.start()
					else:
						notDownloading = False
						mp3 = False
						switched = False
						skips = 0
						player.after = None
						player.stop()
						f = open("auto.txt", "r")
						lines = f.read().splitlines()
						f.close()
						x = random.randint(1,int(len(lines)/2)+1)
						newUrl = lines[((x*2)-1)]
						beforeArgs = "-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5" 
						player = await voice.create_ytdl_player(newUrl, before_options=beforeArgs, pipe=False, after=lambda: self.my_after())
						start_time = time.time()
						elapsed_time = 0
						notDownloading = True
						await self.bot.change_presence(game=discord.Game(name="R's auto"))
						player.volume = 0.3
						auto = True
						player.start()
				
	@commands.command(pass_context=True)
	async def play(self, ctx, *args):
			global musicList
			global voice
			global voice
			worked = False
			url = args[0]
			if url.find("&index")>0:
					url = url[:url.find("&index")]
			search = " ".join(args)
			if voice is not None:
					channel1 = ctx.message.author.voice.voice_channel
					channel2 = voice.channel
					if channel1 == channel2:
							try:
									beforeArgs = "-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5" 
									temp =  await voice.create_ytdl_player(url, before_options=beforeArgs, pipe=False, after=lambda: self.my_after())
									worked = True
							except:
									worked = False
							if len(musicList) >=15:
									embed=discord.Embed(description="No more songs can be queued..", color=0x51719f)
									await self.bot.say(embed=embed)
							elif worked:
									musicList.append(temp)
									await self.nextSong()
									embed=discord.Embed(description="Your song was queued.", color=0x51719f)
									await self.bot.say(embed=embed)
							else:
									query_string = urllib.parse.urlencode({"search_query" : search})
									html_content = urllib.request.urlopen("http://www.youtube.com/results?" + query_string)
									search_results = re.findall(r'href=\"\/watch\?v=(.{11})', html_content.read().decode()) 
									length = len(search_results)
									answer = None
									found = False
									for x in range(0, length):
										url = "http://www.youtube.com/watch?v=" + search_results[x]
										y = x - 1
										await self.bot.send_message(ctx.message.channel, "Is this the link you would like to play? (Answer with Yes or No. Say Quit to quit searching):")
										await self.bot.send_message(ctx.message.channel, url)
										answer = await self.bot.wait_for_message(timeout=60, author=ctx.message.author, channel=ctx.message.channel)
										if answer == None:
											await self.bot.send_message(ctx.message.channel, "Timed out")
											break
										elif answer.content.lower() == "yes":
											print(url)
											beforeArgs = "-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5" 
											temp =  await voice.create_ytdl_player(url, before_options=beforeArgs, pipe=False, after=lambda: self.my_after())
											musicList.append(temp)
											await self.nextSong()
											embed=discord.Embed(description="Your song was queued.", color=0x51719f)
											await self.bot.say(embed=embed)
											found = True
											break
										elif answer.content.lower() == "no":
											await self.bot.send_message(ctx.message.channel, "Check the next link or try again with a new title")
										elif answer.content.lower() == "quit":
											await self.bot.send_message(ctx.message.channel, "Got it")
											break
										else:
											await self.bot.send_message(ctx.message.channel, "Invalid answer")
											x = x - 1


	@commands.command(pass_context=True)
	async def queue(self, ctx):
			global musicList
			global player
			global elapsed_time
			global start_time
			global mp3
			embed=discord.Embed(title="Queue", color=0x51719f)
			if not mp3:
				elapsed_time = time.time() - start_time
				seconds = int(player.duration) - elapsed_time
			else:
				elapsed_time = time.time() - start_time
				seconds = int(8897) - elapsed_time
			m, s = divmod(seconds, 60)
			duration ="%02d:%02d" % (m, s)
			if mp3:
				embed.add_field(name="Currently playing:", value=(("["+'Wuppo - Full Soundtrack'+"]("+'https://www.youtube.com/watch?v=1FUyK5za0h4'+")")+"\nDuration: " + str(duration)), inline=True)
			if not mp3:
				embed.add_field(name="Currently playing:", value=(("["+player.title+"]("+player.url+")")+"\nDuration: " + str(duration)), inline=True)
			if len(musicList) is not 0:
					songs=codecs.encode("These are the songs in the queue\n")
					for x in range(len(musicList)):
							song = musicList[x]
							songs += codecs.encode(str(x+1))+codecs.encode(": [")+ codecs.encode(song.title)+ codecs.encode("](")+ codecs.encode(song.url)+codecs.encode(")\n")
					embed.add_field(name="Songs in Queue", value=codecs.decode(songs), inline=False)
			tempMsg = await self.bot.say(embed=embed)
			if seconds < 0:
					await self.nextSong()
			await asyncio.sleep(10)
			await self.bot.delete_message(tempMsg)
			await self.bot.delete_message(ctx.message)
                                    
	@commands.command(pass_context=True)
	async def leave(self, ctx):
            global player
            if player is not None:
                    if str(ctx.message.author.id) == "218852384976273418":
                            for x in self.bot.voice_clients:
                                    player.after = None
                                    return await x.disconnect()

	@commands.command(pass_context=True)
	async def skip(self, ctx):
            global voice
            global skips
            if voice is not None:
                    channel1 = ctx.message.author.voice.voice_channel
                    channel2 = voice.channel
                    if channel1 == channel2:
                            if str(ctx.message.author.id) == "218852384976273418" and player is not None:
                                    await self.skipSong()
                            else:
                                    skips+=1
                                    people = voice.channel.voice_members
                                    number = len(people) -1
                                    needed = math.ceil(number/2) 
                                    if skips >= needed:
                                            await self.skipSong()
                                            await self.bot.say("Song being skipped")
                                    else:
                                            await self.bot.say("Your vote to skip has been noted\nNeed " + str(needed-skips) + " more votes")

	async def skipSong(self):
            global skips
            skips = 0
            player.stop()
            await asyncio.sleep(10)
            await self.nextSong()
            
	@commands.command(pass_context=True)
	async def auto(self, ctx):
            f = open("auto.txt", "r")
            lines = f.read().splitlines()
            f.close()
            length= len(lines)/2
            tempMsg = await self.bot.say("There are " + str(length) + " songs in the autoplaylist.")
            await asyncio.sleep(10)
            await self.bot.delete_message(tempMsg)
            await self.bot.delete_message(ctx.message)
			
	@commands.command(pass_context=True)
	async def switch(self, ctx):
			global auto4
			global switched
			global voice
			if voice is not None:
					channel1 = ctx.message.author.voice.voice_channel
					channel2 = voice.channel
					if channel1 == channel2:
							auto4 = not auto4
							switched = True
							await self.skipSong()
            
	@commands.command(pass_context=True)
	async def restart(self, ctx):
            if str(ctx.message.author.id) == "218852384976273418" or ctx.message.channel.permissions_for(ctx.message.author).kick_members:
                    self.restarted()
                    await self.bot.say("o/ brb")
                    p = Popen("restart.bat", cwd=r"<address>")
                    stdout, stderr = p.communicate()

	@commands.command(pass_context =True)
	async def playlist(self, ctx, *args):
            worked = False
            global voice
            ##Checking to see if the person has a playlist
            try:
                    person = str(ctx.message.author.id)+".txt"
                    f = open(person, "r")
                    f.close()
                    worked = True
            except:
                    worked = False
            ##When the user wants to see their playlist
            if len(args) == 0 or args[0] == " ":
                    if worked:
                            person = str(ctx.message.author.id)+".txt"
                            f = open(person, "r")
                            content = f.read().splitlines()
                            f.close()
                            songs = codecs.encode("")
                            count = 1
                            for x in range(len(content)):
                                    if x %2==1:
                                            songs+= codecs.encode(str(count)) + codecs.encode(": ") +(codecs.encode(content[x]))+ codecs.encode("\n")
                                            count = count + 1
                            embed=discord.Embed(title=(ctx.message.author.name+"'s playlist"),description=("These are the songs in your playlist:\n"+codecs.decode(songs)), color=0x51719f)
                            await self.bot.say(embed=embed)
                    else:
                            embed=discord.Embed(description="You have not added any songs to your playlist.", color=0x51719f)
                            await self.bot.say(embed=embed)
            ##When the user wants to add a song to playlist
            elif str(args[0]) == "add":
                    if len(args) == 1 or args[1] == " ":
                            embed=discord.Embed(description="You did not tell me a song to add.", color=0x51719f)
                            await self.bot.say(embed=embed)
                    else:
                            url = str(args[1])
                            if url.find("&index")>0:
                                    url = url[:url.find("&index")]
                            worked2 = False
                            try:
                                    temp =  await voice.create_ytdl_player(url)
                                    worked2 = True
                            except:
                                    worked2 = False
                            if not worked2:
                                    embed=discord.Embed(description="The song must be a valid youtube link.", color=0x51719f)
                                    await self.bot.say(embed=embed)
                            else:
                                    person = str(ctx.message.author.id)+".txt"
                                    f = open(person, "a+")
                                    temp =  await voice.create_ytdl_player(url)
                                    f.write("\n"+ temp.title + "\n" + url)
                                    f.close()
                                    embed=discord.Embed(description="Your song has been added to the playlist.", color=0x51719f)
                                    await self.bot.say(embed=embed)
            ##When the user wants to play a song from their playlist
            elif str(args[0]) == "play":
                    if voice is not None:
                            channel1 = ctx.message.author.voice.voice_channel
                            channel2 = voice.channel
                            if channel1 == channel2:
                                    if len(args) == 1 or args[1] == " ":
                                            embed=discord.Embed(description="You did not tell me any songs to play.", color=0x51719f)
                                            await self.bot.say(embed=embed)
                                    else:
                                            number = int(str(args[1]))
                                            if not worked:
                                                    embed=discord.Embed(description="You have not added any songs to your playlist.", color=0x51719f)
                                                    await self.bot.say(embed=embed)
                                            else:
                                                    person = str(ctx.message.author.id)+".txt"
                                                    f = open(person, "r")
                                                    content = f.read().splitlines()
                                                    f.close()
                                                    content.pop(0)
                                                    number = (number*2)-1
                                                    worked4 = False
                                                    url = ""
                                                    try:
                                                            url = content[number]
                                                            worked4 = True
                                                    except:
                                                            worked4 = False
                                                    if len(musicList) >=15:
                                                            embed=discord.Embed(description="No more songs can be queued.", color=0x51719f)
                                                            await self.bot.say(embed=embed)
                                                    elif worked4:
                                                            beforeArgs = "-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5" 
                                                            temp =  await voice.create_ytdl_player(url, before_options=beforeArgs, pipe=False, after=lambda: self.my_after())
                                                            musicList.append(temp)
                                                            embed=discord.Embed(description="Your song has been added.", color=0x51719f)
                                                            await self.bot.say(embed=embed)
                                                    else:
                                                            embed=discord.Embed(description="The number was invalid.", color=0x51719f)
                                                            await self.bot.say(embed=embed)
            elif str(args[0]) == "remove":
                    if voice is not None:
                            channel1 = ctx.message.author.voice.voice_channel
                            channel2 = voice.channel
                            if channel1 == channel2:
                                    if len(args) == 1 or args[1] == " ":
                                            embed=discord.Embed(description="You did not tell me any songs to remove.", color=0x51719f)
                                            await self.bot.say(embed=embed)
                                    else:
                                            number = int(str(args[1]))
                                            if not worked:
                                                    embed=discord.Embed(description="You have not added any songs to your playlist.", color=0x51719f)
                                                    await self.bot.say(embed=embed)
                                            else:
                                                    person = str(ctx.message.author.id)+".txt"
                                                    f = open(person, "r")
                                                    content = f.read().splitlines()
                                                    f.close()
                                                    number = (number*2)
                                                    worked4 = False
                                                    url = ""
                                                    try:
                                                            url = content[number]
                                                            worked4 = True
                                                    except:
                                                            worked4 = False
                                                    if worked4:
                                                            content.pop(number)
                                                            content.pop(number-1)
                                                            f = open(person, "w")
                                                            content2 = "\n".join(content)
                                                            print(content2)
                                                            f.write(content2)
                                                            f.close()
                                                    else:
                                                            embed=discord.Embed(description="The number was invalid.", color=0x51719f)
                                                            await self.bot.say(embed=embed)

	def my_after(self):
            asyncio.run_coroutine_threadsafe(self.nextSong(), self.bot.loop)

def setup(bot):
    bot.add_cog(Music(bot))
