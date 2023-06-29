import os, sys, asyncio, aiohttp
from discord.ext import commands
from discord import Intents
import config
# add this directory to the python module path
sys.path.insert(1,os.path.dirname(os.path.realpath(__file__)))

class IgnoreBotsBot(commands.Bot):
	async def on_message(self,message):
		if message.author.bot: return
		await self.process_commands(message)
	async def setup_hook(self):
		self.session = aiohttp.ClientSession()
		for module in os.listdir("cogs"):
			# if it's a python file, load it as an extension
			if module.endswith(".py"):
				await bot.load_extension("cogs."+module[:-3])
	async def close(self):
		await super().close()
		await self.session.close()

bot = IgnoreBotsBot("!",intents=Intents.all())

bot.run(config.token)
