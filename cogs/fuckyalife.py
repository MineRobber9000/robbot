from discord.ext.commands import Cog
import sys
from unidecode import unidecode
#import aiofiles

class FuckYaLife(Cog,name="Fuck Ya Life (Bing Bong)"):
	@Cog.listener()
	async def on_message(self,message):
		if message.author.bot: return
		if "fuck ya life" in unidecode(message.clean_content.lower()):
			await message.channel.send("BING BONG")

async def setup(bot):
	await bot.add_cog(FuckYaLife())
