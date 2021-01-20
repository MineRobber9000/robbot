from discord.ext.commands import Cog, command, check, is_owner
import os, traceback

class AdminCog(Cog, name="Admin"):
	def __init__(self,bot):
		self.bot=bot

	@command("reload",brief="Reloads modules")
	@is_owner()
	async def reload(self,ctx):
		extensions = list(self.bot.extensions)
		for name in extensions:
			try:
				self.bot.reload_extension(name)
			except:
				await ctx.send("ohno\n```\n"+traceback.format_exc()+"```\n")
				pass
		for module in os.listdir("cogs"):
			if module.endswith(".py"):
				modname = "cogs."+module[:-3]
				if modname in extensions: continue
				try:
					self.bot.load_extension(modname)
				except:
					await ctx.send("ohno\n```\n"+traceback.format_exc()+"```\n")
					pass
		await ctx.send("aight")

	@command("unload",brief="Unloads a given module.")
	@is_owner()
	async def unload(self,ctx,*,ext):
		if ext not in self.bot.extensions:
			await ctx.send("That extension isn't loaded, stupid!")
			return
		self.bot.unload_extension(ext)

	@command("list_modules",brief="Lists loaded modules.")
	async def list_modules(self,ctx):
		await ctx.send("```\nLoaded modules:\n"+"\n".join(self.bot.extensions)+"\n```")

def setup(bot):
	bot.add_cog(AdminCog(bot))
