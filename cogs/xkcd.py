from discord.ext.commands import Cog, command

MONTHS = "January February March April May June July August September October November December".split()

class XKCD(Cog):
	def __init__(self,bot):
		self.bot = bot
		self.session = bot.session
	async def xkcd_message(self,ctx,num):
		"""Send a message about an XKCD comic."""
		url = f"https://xkcd.com/{num}/info.0.json"
		if num==0:
			url = "https://xkcd.com/info.0.json"
		async with self.session.get(url) as resp:
			try:
				data = await resp.json()
				if num==0: num = data['num']
				await ctx.send(f"[xkcd {num}: {data['title']} ({MONTHS[int(data['month'])-1]} {data['day']}, {data['year']})](https://xkcd.com/{num}/)")
			except Exception as e:
				raise CommandError(str(e))
	@command(brief="Look up an XKCD by number.")
	async def xkcd(self,ctx,*,num="0"):
		if not num.isdigit():
			raise CommandError("Must be a number!")
		num = int(num)
		await self.xkcd_message(ctx,num)
	async def cog_command_error(self,ctx,err):
		await ctx.send("\N{CROSS MARK} "+str(err))

async def setup(bot):
	await bot.add_cog(XKCD(bot))
