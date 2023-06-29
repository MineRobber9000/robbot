from discord.ext.commands import Cog, command

class RandCog(Cog, name="Random Stuff"):
	def __init__(self,bot):
		self.bot=bot
	@command(brief="Look at the source code of the bot")
	async def source(self,ctx):
		await ctx.send("https://github.com/MineRobber9000/robbot")
#	@command(brief="Look at the Trello board")
#	async def trello(self,ctx):
#		await ctx.send("https://trello.com/b/N22i5bkH/robbot")

async def setup(bot):
	await bot.add_cog(RandCog(bot))
