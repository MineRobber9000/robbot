from discord.ext.commands import Cog, group
import traceback

class FanficChallengeCog(Cog,name="Fanfiction Challenge"):
	def __init__(self,bot):
		self.bot = bot
		self.session = bot.session

	@group("ffc",brief="Play the Fanfiction Challenge",invoke_without_command=True)
	async def ffc(self,ctx,*args):
		await ctx.send("```\nCommands:\n  pick - Pick a random pairing from a given fandom\n  list - List the fandoms you can pick from.\n```")

	@ffc.command(usage="[fandom]",help="Picks a random pairing of characters from a given fandom. If no fandom ID is specified, a list of fandoms will be printed.",brief="Choose a fandom, or get a list of fandoms")
	async def pick(self,ctx,*,fandom=None):
		if fandom is None:
			async with self.session.get("https://khuxkm.tilde.team/fanfic/list.cgi") as response:
				try:
					fandoms = await response.json()
					out = []
					for fandom in fandoms:
						fobj = fandoms[fandom]
						s = 's' if fobj["characters"]!=1 else ''
						out.append(f"{fobj['name']} (`{fandom}`, {fobj['characters']} character{s})")
					await ctx.send("Fandoms: "+", ".join(out))
				except:
					await ctx.send("ohno\n```\n"+traceback.format_exc()+"```\n")
			return
		async with self.session.get("https://khuxkm.tilde.team/fanfic/pick.cgi",params=dict(fandom=fandom)) as r:
			try:
				resp = await r.json()
				if resp["error"] is None:
					await ctx.send("\N{WHITE HEAVY CHECK MARK}"+f" Your pairing is: {resp['pairing']}")
				else:
					await ctx.send("\N{CROSS MARK}"+f" Error: {resp['error']}")
			except:
				await ctx.send("ohno\n```\n"+traceback.format_exc()+"```\n")

	@ffc.command("list",help="Lists the fandoms you can play the Fanfiction Challenge with. Effectively the same as using pick with no arguments.",brief="Lists the fandoms you can play the Challenge with.")
	async def list_fandoms(self,ctx,*_):
		async with self.session.get("https://khuxkm.tilde.team/fanfic/list.cgi") as response:
			try:
				fandoms = await response.json()
				out = []
				for fandom in fandoms:
					fobj = fandoms[fandom]
					s = 's' if fobj["characters"]!=1 else ''
					out.append(f"{fobj['name']} (`{fandom}`, {fobj['characters']} character{s})")
				await ctx.send("Fandoms: "+", ".join(out))
			except:
				await ctx.send("ohno\n```\n"+traceback.format_exc()+"```\n")

import aiohttp
setup_session=False
def setup(bot):
	global setup_session
	if not hasattr(bot,'session'):
		bot.session=aiohttp.ClientSession(loop=bot.loop)
		setup_session=True
	bot.add_cog(FanficChallengeCog(bot))

def teardown(bot):
	if setup_session:
		bot.session.close()
		del bot.session
