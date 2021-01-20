from discord.ext.commands import Cog, command
import re, random

class DNDCog(Cog, name="D&D"):
	DICE = re.compile(r"(\d+)d(\d+)([+-]\d+)?")
	def __init__(self,bot):
		self.bot=bot
	@command(brief="Roll dice via D&D specifier",help="Roll dice via D&D specifier. Format is {n}d{s}[\N{PLUS-MINUS SIGN}{mod}], where n is the number of dice to roll, s is the number of sides on each die, and mod is the modifier.")
	async def roll(self,ctx,*,dice):
		if not (m:=self.DICE.match(dice)):
			await ctx.send("\N{CROSS MARK} That's not a valid dice specifier.")
			return
		n, s, mod = m.groups()
		n = int(n)
		s = int(s)
		# default to modifier of 0
		mod = int(mod or '0')
		rolls = [random.randint(1,s) for i in range(n)]
		await ctx.send("Result: **"+str(sum(rolls)+mod)+"** ("+", ".join(map(str,rolls))+" plus mod of "+str(mod)+")")
	@command(brief="Roll a D&D character using 4d6dl.")
	async def roll_character(self,ctx):
		stats = []
		for i in range(6):
			rolls = sorted([random.randint(1,6) for i in range(4)])
			stats.append(sum(rolls[1:]))
		await ctx.send("Rolled stats: "+", ".join(map(str,sorted(stats))))

def setup(bot):
	bot.add_cog(DNDCog(bot))
