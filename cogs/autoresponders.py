from discord.ext.commands import Cog, command, CommandError
import sys, argparse, json
from os.path import exists as file_exists
from unidecode import unidecode
#import aiofiles

class RaiseCommandError(argparse.ArgumentParser):
	def error(self,*args):
		raise CommandError(*args)
	def exit(self,*args):
		return

RESPONSES = {}

def load_responses():
	RESPONSES.clear()
	if file_exists("responses.json"):
		with open("responses.json") as f:
			RESPONSES.update(json.load(f))

def save_responses():
	with open("responses.json","w") as f:
		json.dump(RESPONSES,f)

class Autoresponder(Cog,name="Autoresponder"):
	@Cog.listener()
	async def on_message(self,message):
		if message.author.bot: return
		content = unidecode(message.clean_content.lower())
		if content.startswith("!addresponse"): return
		for keyword in RESPONSES:
			if keyword in unidecode(message.clean_content.lower()):
				await message.channel.send(RESPONSES[keyword])
	@command(brief="Add response.")
	async def addresponse(self,ctx,*_args):
		"""
		Adds an auto response. Auto-responses trigger when a word or phrase is spoken.
		Usage: !addresponse [keyword] [response]
		"""
		parser = RaiseCommandError(add_help=False)
		parser.add_argument("keyword")
		parser.add_argument("response")
		parser.add_argument("-h","--help",action="store_true")
		try:
			args = parser.parse_args(_args)
		except SystemExit:
			return
		except CommandError as e:
			await ctx.send("\N{CROSS MARK} Error in parsing arguments (if your keyword or response has a space in it, put quotes around it)\nSpecific error: "+str(e))
			return
		if args.help:
			await ctx.send(f"```\n{self.addresponse.help}\n```")
			return
		keyword = unidecode(args.keyword.lower())
		if keyword in RESPONSES:
			await ctx.send(f"\N{CROSS MARK} There is already a response for {keyword}: \"{RESPONSES[keyword]}\". Remove the previous response before adding a new one.")
			return
		RESPONSES[keyword] = args.response
		save_responses()
		await ctx.send(f"\N{WHITE HEAVY CHECK MARK} Messages that contain {keyword} shall now be responded to with {RESPONSES[keyword]}.")
	@command(brief="Remove response.")
	async def removeresponse(self,ctx,*_args):
		"""
		Removes an auto response. Auto-responses trigger when a word or phrase is spoken.
		Usage: !removeresponse [keyword]
		"""
		parser = RaiseCommandError(add_help=False)
		parser.add_argument("keyword")
		parser.add_argument("-h","--help",action="store_true")
		try:
			args = parser.parse_args(_args)
		except SystemExit:
			return
		except CommandError as e:
			await ctx.send("\N{CROSS MARK} Error in parsing arguments (if your keyword or response has a space in it, put quotes around it)\nSpecific error: "+str(e))
			return
		if args.help:
			await ctx.send(f"```\n{self.addresponse.help}\n```")
			return
		keyword = unidecode(args.keyword.lower())
		if keyword not in RESPONSES:
			await ctx.send(f"\N{CROSS MARK} There is no response for {keyword}.")
			return
		del RESPONSES[keyword]
		save_responses()
		await ctx.send(f"\N{WHITE HEAVY CHECK MARK} Messages that contain {keyword} shall no longer be responded to.")

async def setup(bot):
	load_responses()
	await bot.add_cog(Autoresponder())
