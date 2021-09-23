from discord_slash import SlashCommand
import os
from prsaw import RandomStuffV2
import discord
from discord.ext import commands, tasks
from discord.utils import get
import random
import datetime
import asyncio
import re
from keep_alive import keep_alive
import wikipedia
import pyjokes
import requests
import json
import aiohttp
from PIL import Image
from io import BytesIO
import time



player1 = ""
player2 = ""
turn = ""
gameOver = True

board = []

winningConditions = [
    [0, 1, 2],
    [3, 4, 5],
    [6, 7, 8],
    [0, 3, 6],
    [1, 4, 7],
    [2, 5, 8],
    [0, 4, 8],
    [2, 4, 6]
]


api_key = "354ca81d0fc1fee868571f5120b9ac51"
base_url = "http://api.openweathermap.org/data/2.5/weather?"
bot = commands.Bot(command_prefix="hey ", help_command=None)
slash = SlashCommand(bot, sync_commands=True)
word_list = []
ai = RandomStuffV2()
ch1 = [1, 2, 3, 4, 5, 6, 7, 8, 9]
hunti = ["Kitten", "Husky", "Boar", "Wolf", "Rabbit", "Mouse", "Lol, You found nothing noice!", "Lol, You found nothing noice!", "Lol, You found nothing noice!", "Lol, You found nothing noice!", "Lol, You found nothing noice!", "Lol, You found nothing noice!", "Lol, You found nothing noice!", "Lol, You found nothing noice!", "Lol, You found nothing noice!", "Lol, You found nothing noice!", "Lol, You found nothing noice!", "Lol, You found nothing noice!", "Lol, You found nothing noice!", "Lol, You found nothing noice!", "Lol, You found nothing noice!"]

names = ["Farm", "Lava", "Meow", "Man", "Wroom", "Deadly", "Boom", "Crash", "Boieng", "Heat", "Soft", "Swing", "Rock", "Helium", "Lol", "Woof", "Fan", "Hard", "Not", "Hot", "Cold", "Gold", "Bold", "Beutiful", "Stylish", "Handsum", "Noob", "Pro", "Hacker", "Gamer", "Boomer", "Lol", "Head", "less", "Go", "Green", "Tea", "Cofee",  "Stark", "Hero", "Superhero", "farting", "Moo", "Useless", "Evil", "Devil", "God", "Legend", "Computer", "PC", "Mac", "Apple", "Orange", "Jouicy", "Easy", "Peasy", "Lemon", "Squeezy", "Poop", "Jupiter", "Earth", "Universe", "Integer", "Big", "Bang", "Bong", "Tong"]

def search(question):
    search = wikipedia.summary(question, sentences=10)
    return search

@bot.command()
async def wiki(ctx,*,question):
  searchemb = discord.Embed(title="Results from Wikipedia", description=wikipedia.summary(question, sentences=1000, chars=1000))
  searchemb.set_thumbnail(url="https://media.giphy.com/media/SzBlFsQg26JL0s12P9/giphy.gif?cid=ecf05e479tiy88irmjr2jtsmkp4mb8n2pxiqgl3tg5r8qd70&rid=giphy.gif&ct=g")
  await ctx.reply(embed=searchemb)

@bot.event
async def on_ready():
  print("hello")
  while True:
    await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name=f"{len(bot.guilds)} servers!"))

@bot.command()
async def hey(ctx, message:str):
  await ctx.send("Welcome to the World of Listen.it!")
@bot.command()
async def gstart(ctx, mins:int,*, prize:str):
  embed = discord.Embed(title="Giveaway", description=f"{prize}")
  end = datetime.datetime.utcnow() + datetime.timedelta(seconds = mins*60)
  embed.add_field(name ="Ends at", value=f"{end} UTC")
  embed.set_footer(text=f"Ends {mins}  minutes from now!")
  my_msg = await ctx.send(embed=embed)
  await my_msg.add_reaction("🎉")
  await asyncio.sleep(mins*60)
  new_msg = await ctx.channel.fetch_message(my_msg.id)
  users = await new_msg.reactions[0].users().flatten()
  users.pop(users.index(bot.user))
  winner = random.choice(users)
  tadaemb = discord.Embed(title="🎉 | Congratulation!")
  tadaemb.add_field(name="Winner", value=f"{winner.mention}")
  tadaemb.add_field(name="Prize", value=f"{prize}")
  tadaemb.set_image(url="https://media.giphy.com/media/LoNhsW67omuZBnsVRV/giphy.gif")
  tadaemb.set_footer(text="HeyBot")
  await ctx.send(embed=tadaemb)

@bot.command(help="Let's Play a Game")
async def oneortwo(ctx, ans:int = None):
  await open_account(ctx.author)

  users = await get_bank_data()

  user = ctx.author

  earning = random.randrange(101)
  if ans==None:
    await ctx.send("Answer is an required argument which is missing!")
    return
  if ans > 9:
    await ctx.send("Please enter a valid number. Valid Numbers:- 1, 2, 3, 4, 5, 6, 7, 8 , 9")
    return
  if ans < 1:
    await ctx.send("Please enter a valid number. Valid Numbers:- 1, 2, 3, 4, 5, 6, 7, 8 , 9")
    return
  i = random.choice(ch1)
  if ans != i:
    await ctx.send(f"Lol, You losed this minigame because the Answer was {i}!")
  if ans == i:
    await ctx.send(f"Yayy, You Won this minigame because the Answer Was {i} and you earned {earning}")
    users[str(user.id)]["wallet"] += earning
    
    with open("mainbank.json", "w") as f:
      json.dump(users, f)



@bot.command()
async def warn(ctx, target:discord.Member=None, *, Reason="No Reason Provided"):
  if target == None:
    await ctx.send("You need to mention a user to warn!")
    return
  pfp = target.avatar_url
  embed = discord.Embed(title= f"⚠{target} has been Warned", description=f"{target} has been warned!")
  embed.add_field(name = "Reason", value = f"{Reason}")
  embed.set_footer(text = f"Requested by {ctx.author.name}")
  embed.set_thumbnail(url=pfp)
  await ctx.send(embed=embed)

@bot.command()
async def help(ctx):
  embed = discord.Embed(title = "Here you go!")
  embed.add_field(name="⚖️ | Moderation Commands", value="kick, ban, warn, unban")
  embed.add_field(name=" <:partner:871608863336570890> | Fun Commands", value="hunt, oneortwo, meme, joke")
  embed.add_field(name="🛠️ | Tools", value="randomusername, gstart")
  embed.add_field(name="🐶 | Animals", value="kitty, puppy")
  embed.set_footer(text="Use 'hey '  before any command!")
  embed.set_image(url="https://media.giphy.com/media/n9wlqnp1yuNUWaeIGU/giphy.gif?cid=790b7611235c558c53d815a8b3c4fda2589952788e69645c&rid=giphy.gif&ct=g")
  await ctx.send(embed=embed)
@bot.command(description="Unmutes a specified user.")
@commands.has_permissions(manage_messages=True)
async def unmute(ctx, member: discord.Member):
   mutedRole = discord.utils.get(ctx.guild.roles, name="Muted")

   await member.remove_roles(mutedRole)
   await member.send(f" you have unmutedd from: - {ctx.guild.name}")
   embed = discord.Embed(title="unmute", description=f" unmuted-{member.mention}",colour=discord.Colour.light_gray())
   await ctx.send(embed=embed)
@bot.command(description="Mutes the specified user.")
@commands.has_permissions(manage_messages=True)
async def mute(ctx, member: discord.Member, *, reason=None):
    guild = ctx.guild
    mutedRole = discord.utils.get(guild.roles, name="Muted")

    if not mutedRole:
        mutedRole = await guild.create_role(name="Muted")

        for channel in guild.channels:
            await channel.set_permissions(mutedRole, speak=False, send_messages=False, read_message_history=True, read_messages=False)
    embed = discord.Embed(title="muted", description=f"{member.mention} was muted ", colour=discord.Colour.light_gray())
    embed.add_field(name="reason:", value=reason, inline=False)
    await ctx.send(embed=embed)
    await member.add_roles(mutedRole, reason=reason)
    await member.send(f" you have been muted from: {guild.name} reason: {reason}")
@bot.command()
async def randomusername(ctx):
  embed = discord.Embed(title="A new Random Username has appeared!", description=f"{random.choice(names)}{random.choice(names)}{random.randint(1,9)}{random.randint(1,9)}")
  embed.set_footer(text=ctx.author.display_name, icon_url=ctx.author.avatar_url)
  await ctx.send(embed=embed)
@bot.command(aliases=['make_role'])
@commands.has_permissions(manage_roles=True)
async def create_role(ctx, *, name):
	guild = ctx.guild
	await guild.create_role(name=name)
	await ctx.send(f'Role `{name}` has been created')

@bot.event
async def on_server_join(ctx):
    for guild in bot.guilds:
        for channel in guild.text_channels:
            if channel.permissions_for(guild.me).say:
                await ctx.message.channel.send('Thanks for choosing me!')
                break
@bot.command()
async def joke(ctx):
  avtar = ctx.author.avatar_url
  embed = discord.Embed(title="Your Joke", description=pyjokes.get_joke())
  embed.set_thumbnail(url="https://media.giphy.com/media/zuB79BQoLrOdUS8q5I/giphy.gif?cid=ecf05e47hny8c6lmgdkosjtlaejwho14mjhvjeofb3jbd2u9&rid=giphy.gif&ct=s")
  embed.set_footer(text=ctx.author.display_name, icon_url=avtar)
  await ctx.send(embed=embed)

@bot.command(pass_context=True)
async def meme(ctx):
    embed = discord.Embed(title="", description="")

    async with aiohttp.ClientSession() as cs:
        async with cs.get('https://www.reddit.com/r/dankmemes/new.json?sort=hot') as r:
            res = await r.json()
            embed.set_image(url=res['data']['children'] [random.randint(0, 25)]['data']['url'])
            await ctx.send(embed=embed)

@bot.command()
async def rps(ctx):
    rpsGame = ['rock', 'paper', 'scissors']
    await ctx.send(f"Rock, paper, or scissors? Choose wisely...")

    def check(msg):
        return msg.author == ctx.author and msg.channel == ctx.channel and msg.content.lower() in rpsGame

    user_choice = (await bot.wait_for('message', check=check)).content

    comp_choice = random.choice(rpsGame)
    if user_choice == 'rock':
        if comp_choice == 'rock':
            await ctx.send(f'Well, that was weird. We tied.\nYour choice: {user_choice}\nMy choice: {comp_choice}')
        elif comp_choice == 'paper':
            await ctx.send(f'Nice try, but I won that time!!\nYour choice: {user_choice}\nMy choice: {comp_choice}')
        elif comp_choice == 'scissors':
            await ctx.send(f"Aw, you beat me. It won't happen again!\nYour choice: {user_choice}\nMy choice: {comp_choice}")

    elif user_choice == 'paper':
        if comp_choice == 'rock':
            await ctx.send(f'The pen beats the sword? More like the paper beats the rock!!\nYour choice: {user_choice}\nMy choice: {comp_choice}')
        elif comp_choice == 'paper':
            await ctx.send(f'Oh, wacky. We just tied. I call a rematch!!\nYour choice: {user_choice}\nMy choice: {comp_choice}')
        elif comp_choice == 'scissors':
            await ctx.send(f"Aw man, you actually managed to beat me.\nYour choice: {user_choice}\nMy choice: {comp_choice}")

    elif user_choice == 'scissors':
        if comp_choice == 'rock':
            await ctx.send(f'HAHA!! I JUST CRUSHED YOU!! I rock!!\nYour choice: {user_choice}\nMy choice: {comp_choice}')
        elif comp_choice == 'paper':
            await ctx.send(f'Bruh. >: |\nYour choice: {user_choice}\nMy choice: {comp_choice}')
        elif comp_choice == 'scissors':
            await ctx.send(f"Oh well, we tied.\nYour choice: {user_choice}\nMy choice: {comp_choice}")

@bot.command()
async def wanted(ctx, target:discord.Member = None):
  if target == None:
    target = ctx.author

  wanted = Image.open("loll.png")
  asset = target.avatar_url_as(size=128)
  data = BytesIO(await asset.read())
  pfp = Image.open(data)
  pfp.resize((500, 500))
  wanted.paste(pfp, (450, 400))
  wanted.save("profile.jpg")
  await ctx.send(file = discord.File("profile.jpg"))
@bot.command()
async def clear(ctx, amount=5):
	await ctx.channel.purge(limit=amount+1)
  
@slash.slash(description="Shows bot Latency")
async def ping(ctx):
  await ctx.send(f"Bot Speed {round(bot.latency*1000)}")

@bot.command()
async def tictactoe(ctx, p1: discord.Member, p2: discord.Member):
    global count
    global player1
    global player2
    global turn
    global gameOver

    if gameOver:
        global board
        board = [":white_large_square:", ":white_large_square:", ":white_large_square:",
                 ":white_large_square:", ":white_large_square:", ":white_large_square:",
                 ":white_large_square:", ":white_large_square:", ":white_large_square:"]
        turn = ""
        gameOver = False
        count = 0

        player1 = p1
        player2 = p2

        # print the board
        line = ""
        for x in range(len(board)):
            if x == 2 or x == 5 or x == 8:
                line += " " + board[x]
                await ctx.send(line)
                line = ""
            else:
                line += " " + board[x]

        # determine who goes first
        num = random.randint(1, 2)
        if num == 1:
            turn = player1
            await ctx.send("It is <@" + str(player1.id) + ">'s turn.")
        elif num == 2:
            turn = player2
            await ctx.send("It is <@" + str(player2.id) + ">'s turn.")
    else:
        await ctx.send("A game is already in progress! Finish it before starting a new one.")

@bot.command()
async def place(ctx, pos: int):
    global turn
    global player1
    global player2
    global board
    global count
    global gameOver

    if not gameOver:
        mark = ""
        if turn == ctx.author:
            if turn == player1:
                mark = ":regional_indicator_x:"
            elif turn == player2:
                mark = ":o2:"
            if 0 < pos < 10 and board[pos - 1] == ":white_large_square:" :
                board[pos - 1] = mark
                count += 1

                # print the board
                line = ""
                for x in range(len(board)):
                    if x == 2 or x == 5 or x == 8:
                        line += " " + board[x]
                        await ctx.send(line)
                        line = ""
                    else:
                        line += " " + board[x]

                checkWinner(winningConditions, mark)
                print(count)
                if gameOver == True:
                    await ctx.send(mark + " wins!")
                elif count >= 9:
                    gameOver = True
                    await ctx.send("It's a tie!")

                # switch turns
                if turn == player1:
                    turn = player2
                elif turn == player2:
                    turn = player1
            else:
                await ctx.send("Be sure to choose an integer between 1 and 9 (inclusive) and an unmarked tile.")
        else:
            await ctx.send("It is not your turn.")
    else:
        await ctx.send("Please start a new game using the !tictactoe command.")


def checkWinner(winningConditions, mark):
    global gameOver
    for condition in winningConditions:
        if board[condition[0]] == mark and board[condition[1]] == mark and board[condition[2]] == mark:
            gameOver = True

@tictactoe.error
async def tictactoe_error(ctx, error):
    print(error)
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send("Please mention 2 players for this command.")
    elif isinstance(error, commands.BadArgument):
        await ctx.send("Please make sure to mention/ping players (ie. <@688534433879556134>).")

@place.error
async def place_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send("Please enter a position you would like to mark.")
    elif isinstance(error, commands.BadArgument):
        await ctx.send("Please make sure to enter an integer.")

@bot.command(pass_context=True)
async def kitty(ctx):
    async with aiohttp.ClientSession() as cs:
        async with cs.get('https://www.reddit.com/r/cat/new.json?sort=hot') as r:
            res = await r.json()
            embed = discord.Embed(title = res['data']['children'][random.randint(0,25)]["data"]["title"], description="")
            embed.set_image(url=res['data']['children'] [random.randint(0, 25)]['data']['url'])
            await ctx.send(embed=embed)

@bot.command(pass_context=True)
async def puppy(ctx):
    async with aiohttp.ClientSession() as cs:
        async with cs.get('https://www.reddit.com/r/PuppySmiles/new.json?sort=hot') as r:
            res = await r.json()
            embed = discord.Embed(title = res['data']['children'][random.randint(0,25)]["data"]["title"], description="")
            embed.set_image(url=res['data']['children'] [random.randint(0, 25)]['data']['url'])
            await ctx.send(embed=embed)
@slash.slash(description="Returns cute dog images")
async def puppy(ctx):
    async with aiohttp.ClientSession() as cs:
        async with cs.get('https://www.reddit.com/r/PuppySmiles/new.json?sort=hot') as r:
            res = await r.json()
            embed = discord.Embed(title = res['data']['children'][random.randint(0,25)]["data"]["title"], description="")
            embed.set_image(url=res['data']['children'] [random.randint(0, 25)]['data']['url'])
            await ctx.send(embed=embed)

@bot.command()
async def balance(ctx):
  await open_account(ctx.author)
  user = ctx.author
  users = await get_bank_data()
  wallet_amt = users[str(user.id)]["wallet"]
  em = discord.Embed(title="Balance", color=discord.Color.green())
  em.add_field(name= "Wallet", value=wallet_amt)
  await ctx.send(embed=em)

@commands.cooldown(1, 60, commands.BucketType.user)
@bot.command()
async def beg(ctx):
  await open_account(ctx.author)

  users = await get_bank_data()

  user = ctx.author

  earning = random.randrange(101)

  await ctx.send(f"Someone Gave you {earning}")

  users[str(user.id)]["wallet"] += earning

  with open("mainbank.json", "w") as f:
    json.dump(users, f)

async def open_account(user):
  users = await get_bank_data()
  if str(user.id) in users:
    return False
  else:
    users[str(user.id)] = {}
    users[str(user.id)]["wallet"] = 0
    users[str(user.id)]["bank"] = 0
  with open("mainbank.json", "w") as f:
    json.dump(users, f)
  return True

async def get_bank_data():
  with open("mainbank.json", "r") as f:
    users = json.load(f)

  return users


@bot.command()
@commands.cooldown(1, 60*60*24, commands.BucketType.user)
async def daily(ctx):
  await open_account(ctx.author)

  users = await get_bank_data()

  user = ctx.author
  embed=discord.Embed(title="Here is your daily", description="⏣10000 was placed in your wallet", color=discord.Color.green())
  users[str(user.id)]["wallet"] += 10000

  with open("mainbank.json", "w") as f:
    json.dump(users, f)
   
  await ctx.send(embed=embed)
keep_alive()

bot.run("ODc5NjAwNjU2Mjc1NjExNjg5.YSSF8g.FkVOZ8Bk95u3Ha8jkYb2ZlnFXQE")
