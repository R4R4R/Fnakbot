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
import os

class Logs():
	def __init__(self,bot):
		self.bot = bot
	
	@commands.has_permissions(ban_members=True)
	@commands.command(pass_context =True)
	async def setchannel(self, ctx):
		filename = str(ctx.message.server.id)+"log.txt"
		f = open(filename, "w+")
		f.write(ctx.message.channel.id)
		f.close()
		await self.bot.say("Set " + ctx.message.channel.name + " as log channel")
	
	async def on_message_delete(self, message):
		if(message.author.id is not '364936870938935307'):
			filename = str(message.server.id)+"log.txt"
			f = open(filename, "r+")
			channelid = f.read()
			f.close()
			if channelid == "":
				await self.bot.say("Log channel not set")
			else:
				embed=discord.Embed(title=("Message Deleted by "+ message.author.name), color=0x51719f)
				now = time.ctime(int(time.time()))
				embed.set_author(name=message.author.name, icon_url=message.author.avatar_url)
				embed.set_footer(text=now)
				embed.add_field(name="Channel", value=(message.channel.name))
				embed.add_field(name="UserID", value=("("+message.author.id+")"))
				if len(message.content) > 0:
					embed.add_field(name="Message content", value=(message.content))
				for x in message.attachments:
					embed.add_field(name="attachment", value=(x.get('proxy_url')))
					print(x.get('proxy_url'))
				await self.bot.send_message(self.bot.get_channel(channelid), embed=embed)
				print(message.author.name+"\n"+message.content)
			
	async def on_member_join(self, member):
		filename = str(member.server.id)+"log.txt"
		f = open(filename, "r+")
		channelid = f.read()
		f.close()
		if channelid == "":
			await self.bot.say("Log channel not set")
		else:
			embed=discord.Embed(title=(member.name +" joined"), color=0x51719f)
			embed.set_author(name=member.name, icon_url=member.avatar_url)
			await self.bot.send_message(self.bot.get_channel(channelid), embed=embed)
	
	async def on_member_remove(self, member):
		filename = str(member.server.id)+"log.txt"
		f = open(filename, "r+")
		channelid = f.read()
		f.close()
		if channelid == "":
			await self.bot.say("Log channel not set")
		else:
			embed=discord.Embed(title=(member.name +" left"), color=0x51719f)
			embed.set_author(name=member.name, icon_url=member.avatar_url)
			await self.bot.send_message(self.bot.get_channel(channelid), embed=embed)
	
	async def on_message_edit(self, before, after):
		if(len(before.content) > 0):
			filename = str(before.server.id)+"log.txt"
			f = open(filename, "r+")
			channelid = f.read()
			f.close()
			if channelid == "":
				await self.bot.say("Log channel not set")
			else:
				embed=discord.Embed(title=("Message Edited by "+ before.author.name), color=0x51719f)
				now = time.ctime(int(time.time()))
				embed.set_author(name=before.author.name, icon_url=before.author.avatar_url)
				embed.set_footer(text=now)
				embed.add_field(name="Channel", value=(before.channel.name))
				embed.add_field(name="UserID", value=("("+before.author.id+")"))
				if len(before.content) > 0:
					embed.add_field(name="Before", value=(before.content))
				for x in before.attachments:
					embed.add_field(name="Before (attachment)", value=(x.get('proxy_url')))
					print(x.get('proxy_url'))
				if len(after.content) > 0:
					embed.add_field(name="After", value=(after.content))
				for x in after.attachments:
					embed.add_field(name="After (attachment)", value=(x.get('proxy_url')))
				if before.content is not after.content:
					await self.bot.send_message(self.bot.get_channel(channelid), embed=embed)
				print(before.author.name+"\n"+before.content)
		
	@commands.has_permissions(ban_members=True)
	@commands.command(pass_context =True)
	async def say(self, ctx, words):
		await self.bot.say(words)
	
def setup(bot):
    bot.add_cog(Logs(bot))