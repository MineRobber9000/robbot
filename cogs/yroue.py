from discord.ext.commands import Cog
import sys
from unidecode import unidecode
#import aiofiles

class Yroue(Cog,name="Yro'ue"):
	@Cog.listener()
	async def on_message(self,message):
		if message.author.bot: return
		if "yro'ue" in unidecode(message.clean_content.lower()):
			await message.channel.send("https://tenor.com/view/clone-drone-in-the-danger-zone-yroue-gif-22600859")

async def setup(bot):
	await bot.add_cog(Yroue())
