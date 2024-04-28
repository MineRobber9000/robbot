from discord.ext.commands import Cog
from unidecode import unidecode
import re

_SMH = re.compile(r"smh(\s+my\s+head)*",re.IGNORECASE)
_WHITESPACE = re.compile(r"\s+")

class SMH(Cog):
	@Cog.listener()
	async def on_message(self, message):
		if message.author.bot: return
		content = unidecode(message.clean_content.lower())
		if (m:=_SMH.search(content)):
			text = _WHITESPACE.sub(m.group(0)," ")+" my head"
			await message.channel.send(text,reference=message,mention_author=False)

async def setup(bot):
	await bot.add_cog(SMH())
