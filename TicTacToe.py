import traceback
import sys
from discord.ext import commands
import discord


gameOn = False

class TicTacToe:
	def __init__(self, bot):
		self.bot = bot
	
	@commands.command(pass_context =True)
	async def ttt(self, ctx):
		gameon = True
		await self.bot.say("Time for a game of Tic Tac Toe")
		await self.bot.say("Say 'join' to join the game with " + ctx.message.author.nick )
	
	

def setup(bot):
	bot.add_cog(TicTacToe(bot))