from discord.ext.commands import Cog
import sys
#import aiofiles

class Log(Cog,name="Logger"):
	@Cog.listener()
	async def on_message(self,message):
		userline = f"{message.author.display_name}"
		if message.author.bot: userline+=" [BOT]"
		logline = f"[{message.channel.name}] {userline}: {message.clean_content}"
		print(logline)
		sys.stdout.flush()
		sys.stderr.flush()
#		with aiofiles.open("log.txt","a") as f:
#			await f.write(logline+"\n")
#			await f.flush()

async def setup(bot):
	await bot.add_cog(Log())
