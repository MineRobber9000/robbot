from discord.ext.commands import Cog, command, check, is_owner
import os, traceback, textwrap

class AdminCog(Cog, name="Admin"):
	def __init__(self,bot):
		self.bot=bot

	@command("reload",brief="Reloads modules")
	@is_owner()
	async def reload(self,ctx):
		extensions = list(self.bot.extensions)
		for name in extensions:
			try:
				await self.bot.unload_extension(name)
			except:
				await ctx.send("ohno\n```\n"+traceback.format_exc()+"```\n")
				pass
		for module in os.listdir("cogs"):
			if module.endswith(".py"):
				modname = "cogs."+module[:-3]
				try:
					await self.bot.load_extension(modname)
				except:
					await ctx.send("ohno\n```\n"+traceback.format_exc()+"```\n")
					pass
		await ctx.send("aight")

	@command("load",brief="Loads a given module.")
	@is_owner()
	async def load(self,ctx,*,ext):
		if ext in self.bot.extensions:
			await ctx.send("That extension is already loaded, stupid!")
			return
		await self.bot.load_extension(ext)
		await ctx.send("aight")

	@command("unload",brief="Unloads a given module.")
	@is_owner()
	async def unload(self,ctx,*,ext):
		if ext not in self.bot.extensions:
			await ctx.send("That extension isn't loaded, stupid!")
			return
		await self.bot.unload_extension(ext)
		await ctx.send("aight")

	@command("list_modules",brief="Lists loaded modules.")
	async def list_modules(self,ctx):
		await ctx.send("```\nLoaded modules:\n"+"\n".join(self.bot.extensions)+"\n```")

	def cleanup_code(self, content):
		"""Automatically removes code blocks from the code."""
		# remove ```py\n```
		if content.startswith('```') and content.endswith('```'):
			return '\n'.join(content.split('\n')[1:-1])

		# remove `foo`
		return content.strip('` \n')

	@command("eval",brief="Evaluate Python code. Only Robert can do this.")
	@is_owner()
	async def robbot_eval(self,ctx,*,code):
		try:
			ns = dict()
			ns["ctx"]=ctx
			ns["bot"]=self.bot
			ns["discord"]=__import__("discord")
			__import__("discord.utils")
			ns.update(globals())
			code = "async def func():\n"+textwrap.indent(self.cleanup_code(code)," "*2)
			exec(code,ns)
			assert "func" in ns
			ret = await ns["func"]()
			await ctx.send("Result:\n```\n"+repr(ret)+"\n```\n")
		except:
			await ctx.send("Result:\n```\n"+traceback.format_exc()+"\n```\n")

	@command("reboot")
	@is_owner()
	async def reboot(self,ctx):
		sys.exit()

async def setup(bot):
	await bot.add_cog(AdminCog(bot))
