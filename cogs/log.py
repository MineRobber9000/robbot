from discord.ext.commands import Cog
#import aiofiles

class Log(Cog,name="Logger"):
	@Cog.listener()
	async def on_message(self,message):
		logline = f"[{message.channel.name}] {message.author.display_name}: {message.clean_content}"
		print(logline)
#		with aiofiles.open("log.txt","a") as f:
#			await f.write(logline+"\n")
#			await f.flush()

def setup(bot):
	bot.add_cog(Log())
