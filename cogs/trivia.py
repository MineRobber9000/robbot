from discord.ext.commands import Cog, command, CommandError
import argparse
import asyncio
import base64
import random
import time
import traceback
from urllib.parse import urlencode

ALPHABET = "abcdefghijklmnopqrstuvwxyz"

class RaiseCommandError(argparse.ArgumentParser):
	def error(self,*args):
		raise CommandError(*args)
	def exit(self,*args):
		return

CATEGORIES = {'General Knowledge': 9, 'Books': 10, 'Film': 11, 'Music': 12, 'Musicals & Theatres': 13, 'Television': 14, 'Video Games': 15, 'Board Games': 16, 'Science & Nature': 17, 'Computers': 18, 'Mathematics': 19, 'Mythology': 20, 'Sports': 21, 'Geography': 22, 'History': 23, 'Politics': 24, 'Art': 25, 'Celebrities': 26, 'Animals': 27, 'Vehicles': 28, 'Comics': 29, 'Gadgets': 30, 'Japanese Anime & Manga': 31, 'Cartoon & Animations': 32}

class NoSuchCategory(CommandError):
	def __init__(self,input):
		super(NoSuchCategory,self).__init__(f"No such category \"{input}\".")

class AmbiguousCategory(CommandError):
	def __init__(self,input,possibly=["ohno"]):
		possibly = ", ".join(map(lambda s: f'"{s}"',possibly))
		super(AmbiguousCategory,self).__init__(f"\"{input}\" is ambiguous. Do you mean: {possibly}?")

class InvalidDifficulty(CommandError):
	def __init__(self,input):
		super(InvalidDifficulty,self).__init__(f"Invalid difficulty \"{input}\".")

FIRST_ITEM = lambda l: next(iter(l))

def resolve_category(partial):
	global CATEGORIES
	for category in CATEGORIES.keys():
		if category.lower()==partial.lower():
			return CATEGORIES[category]
	possible_categories = [name for name in CATEGORIES.keys() if partial.lower() in name.lower()]
	if len(possible_categories)==0:
		raise NoSuchCategory(partial)
	elif len(possible_categories)>1:
		raise AmbiguousCategory(partial,possible_categories)
	else: # len(possible_categories)==1
		return CATEGORIES[FIRST_ITEM(possible_categories)]

def resolve_difficulty(partial):
	if partial.lower()=="ez": return "easy"
	possible_difficulties = [difficulty for difficulty in ["easy","medium","hard"] if difficulty.startswith(partial.lower())]
	if len(possible_difficulties)==0: raise InvalidDifficulty(partial)
	return FIRST_ITEM(possible_difficulties)

def clean_category_name(catname):
	if ": " in catname: return catname.split(": ",1)[1]
	return catname

def parse(d):
	for key in d.keys():
		if type(d[key])==list:
			for i, v in enumerate(d[key]):
				d[key][i]=base64.b64decode(v).decode()
		elif type(d[key])==str:
			d[key]=base64.b64decode(d[key]).decode()
	return d

class TriviaCog(Cog,name="Trivia"):
	def __init__(self,bot):
		self.bot = bot
		self.session = bot.session
		self.token = None
		self.token_use_time = 0

	@command(brief="A trivia command. Takes extra arguments, check help command for more info")
	async def trivia(self,ctx,*_args):
		"""
		Asks you a trivia question. Arguments:
			- `-d/--difficulty <easy/medium/hard>` - Affects the difficulty of the question.
			- `-c/--category <category>` - A specific category to ask for. Use "list" to list the categories.
		"""
		parser = RaiseCommandError(add_help=False)
		parser.add_argument("-d","--difficulty")
		parser.add_argument("-c","--category")
		parser.add_argument("-h","--help",action="store_true")
		try:
			args = parser.parse_args(_args)
		except SystemExit:
			return
		except CommandError as e:
			await ctx.send("\N{CROSS MARK} Error in parsing arguments (if your category has a space in it, put quotes around it)\nSpecific error: "+str(e))
			return
		if args.help:
			await ctx.send(f"```\n{self.trivia.help}\n```") # i guess???
			return
		api_args = {"amount":1,"encode":"base64"}
		if args.difficulty is not None: api_args["difficulty"]=resolve_difficulty(args.difficulty)
		if args.category=="list":
			await ctx.send("Categories:" + ", ".join(CATEGORIES.keys()))
			return
		elif args.category is not None: api_args["category"]=resolve_category(args.category)
		if self.token is None or (time.time()-self.token_use_time)>=(6*60*60):
			async with self.session.get("https://opentdb.com/api_token.php?command=request") as response:
				resp = await response.json()
				assert resp["response_code"]==0, "Error getting new token!"
				self.token = resp["token"]
		api_args["token"]=self.token
		self.token_use_time=time.time()
		async with self.session.get("https://opentdb.com/api.php?"+urlencode(api_args)) as response:
			try:
				data = await response.json()
				if data["response_code"]==3: # Token not found
					self.token = None
					await self.trivia(ctx,*_args)
					return
				elif data["response_code"]==4: # Token needs refreshing
					async with self.session.get("https://opentdb.com/api_token.php?command=reset&token="+self.token) as response:
						resp = await response.json()
						assert resp["response_code"]==0, "Error refreshing token!"
						await self.trivia(ctx,*_args)
						return
				elif data["response_code"]!=0:
					raise Exception(["No results for that query","Invalid parameter (the bot is borken?)","This shouldn't happen","This shouldn't happen"][data["response_code"]-1])
				assert len(data["results"])==1, "The API gave me too many questions (or not enough)"
				question = parse(FIRST_ITEM(data["results"]))
				timeout = 60
				if question['difficulty']=='medium':
					timeout = 30
				elif question['difficulty']=='easy':
					timeout = 15
				await ctx.send(f"Alright! Here's a {question['difficulty']} question from the category \"{clean_category_name(question['category'])}\". You have {timeout} seconds.")
				if question["type"]=="boolean":
					await ctx.send(f"True or False: {question['question']}")
					answers = ["True","False"]
				else:
					answers = question["incorrect_answers"]+[question["correct_answer"]]
					random.shuffle(answers)
					answers_str = ""
					for i, answer in enumerate(answers):
						answers_str += f"{ALPHABET[i]}. {answer.strip()}\n"
					await ctx.send(f"{question['question']}\n\n{answers_str}")
				answered = []
				def _check(m):
					if m.content.lower()=="!skip": return True
					if m.author in answered: return False
					if m.channel!=ctx.channel: return False
					if question["type"]=="boolean":
						return m.content.lower().startswith("t") or m.content.lower().startswith("f")
					else:
						return m.content.lower() in ALPHABET and ALPHABET.index(m.content.lower())<len(answers)
				incorrect_answers = len(answers)-1
				end = time.time()+timeout
				prev_inc = []
				while True:
					try:
						msg = await ctx.bot.wait_for("message",check=_check,timeout=max(end-time.time(),.001))
					except asyncio.TimeoutError:
						await ctx.send(f"Time's up! The answer was {question['correct_answer']}.")
						return
					answered.append(msg.author)
					if msg.content.lower()=="!skip":
						answer = None
					elif question["type"]=="boolean":
						answer = "True" if msg.content.lower().startswith("t") else "False"
					else:
						answer = answers[ALPHABET.index(msg.content.lower())]
					if answer==question["correct_answer"]:
						await ctx.send(f"Correct! Good job {msg.author.mention}!")
						return
					else:
						if answer is not None: await ctx.send(f"Ooh, I'm sorry! That's not correct.")
						else: incorrect_answers=0
						if answer not in prev_inc:
							prev_inc.append(answer)
							incorrect_answers-=1
							if incorrect_answers<=0:
								if question["type"]=="boolean": return
								await ctx.send(f"The answer was {question['correct_answer']}.")
								return
						else:
							await ctx.send("...I already said that answer was wrong...")
							answered.remove(msg.author)
			except Exception as e:
				raise CommandError("Error getting question from trivia database! Specific error: "+str(e))

	async def cog_command_error(self,ctx,err):
		await ctx.send("\N{CROSS MARK} "+str(err))

async def setup(bot):
	await bot.add_cog(TriviaCog(bot))
