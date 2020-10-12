import discord
import sys
import time
import os, signal
from discord.ext import commands
import asyncio
import random
from datetime import datetime
from urllib.request import urlopen
import json

with open("mep.txt") as f:
    TOKEN = f.readline().strip()

fname = str(datetime.now()).replace(" ", "-")
client = commands.Bot(command_prefix="-")

TOBLER = '<@!415672488488599553>'
NOTTOBLER = '<@621520802038153256>'

ABHI = '<@!280925106685870082>'
NICO = '<@!331696147896860673>'
TONY = '<@!149467477477294080>'

greetings = ['Hi', 'Hey', 'How\'s it going', 'Hi there', 'What\'s up', 'Hiya', 'How are things']

with open('badwords.txt', 'r') as f:
    badwords = f.readlines()
for x in range(len(badwords)):
    badwords[x] = badwords[x].strip("\n")

with open('UserRoles', 'r') as file:
    users = file.read().split("\n")

for x in range(len(users)):
    users[x] = users[x].split(":")

userDict = {}
for x in users:
    userDict.update({x[0] : x[1]})

print (userDict)

url = 'https://api.nasa.gov/planetary/apod?api_key=3qfmY2tH6m9dE5P7j6EGOfnwKvALcdcIcXegUn9c'
@client.command()
async def fact(ctx):
    response = urlopen(url)
    data = response.read().decode("utf-8")
    q = json.loads(data)
    await ctx.message.channel.send(q["url"])
    await ctx.message.channel.send(q["explanation"])


@client.command(name="coinflip", aliases=["CoinFlip", "Coinflip"])
async def coinflip(ctx):
    await ctx.message.channel.send(random.choice(["It's Heads!","It's Tails!"]))

@client.command()
async def latex(ctx, *t):
    if not t:
        await ctx.message.channel.send(f"Usage: -latex *valid latex expression*\nExample: -latex x^2 + 5\nFor further commands:\nhttp://tug.ctan.org/info/undergradmath/undergradmath.pdf")
        return
        
    url = f"https://latex.codecogs.com/gif.latex?%5Cdpi%7B150%7D%20%5Cbg_white%20%5Clarge%20"
    text = "%20".join(t)
    a = url+text
    """
    e = discord.Embed(title="Here ya go!")
    e.setImage(url=a)
    e.setThumbnail(url=a)
    """
    
    await ctx.message.channel.send(a)



@client.command()
async def resetquestions(ctx):
    global q
    global qcurrent
    global questionDict
    if (ctx.message.author.mention == ABHI):
        q = []
        with open("KinematicsQuestions") as f:
            q = f.read().split("@@@\n")
        for x in range(len(q)):
            q[x] = q[x].split("$$$\n")
        for x in range(len(q)):
            q[x][1] = q[x][1].replace("\n", "").replace("@@@", "").replace("$$$", "").split(", ")
    
        questionDict["kinematics"] = q
        await ctx.message.channel.send("Questions reloaded")
    else:
        print("NOT AUTHORIZED")
    


@client.command()
async def renick(ctx, user, name):
    if((ctx.message.author.mention == TOBLER) or (ctx.message.author.mention == ABHI)):
        print(user[3:-1])
        await ctx.message.channel.send(user + " nickname changed to " + name)
        await ctx.message.mentions[0].edit(nick=name);

@client.command()
async def info(ctx):
    author = ctx.message.author
    channel = ctx.message.channel
    msg = 'Hey! Welcome to the MCHS Physics Server ' + author.mention + '\nRight now I don\'t do much but I\'m working on it'
    await channel.send(msg)

with open("KinematicsQuestions") as f:
    q = f.read().split("\n@@@\n")

for x in range(len(q)):
    q[x] = q[x].split("$$$\n")

for x in range(len(q)):
    q[x][1] = q[x][1].strip("\n").strip("@@@").strip("$$$").split(", ")

questionDict = {}
questionDict.update({"kinematics" : q})
qcurrent = [False, "", []]

@client.command()
async def question(ctx, *t):
    if not qcurrent[0]:
        if len(t) == 1:
            temp = random.choice(questionDict[t[0].lower()])
            qcurrent[2] = temp[1]
            qcurrent[1] = temp[0]
            qcurrent[0] = True
            print(q)
            print (qcurrent)
            await ctx.message.channel.send(qcurrent[1] + "\nHow to answer example: -answer 12.5")
        else:
            await ctx.message.channel.send("Specify question type. Example -question kinematics")
    else:
        await ctx.message.channel.send("A question already exists" + "\n" + qcurrent[1])

@client.command()
async def answer(ctx, answer):
    global qcurrent
    print("answer ++++ " + answer)
    if qcurrent[0]:
        if answer in qcurrent[2]:
            await ctx.message.channel.send("That\'s correct " + ctx.message.author.mention + "!")
            qcurrent = [False, "", []]
        else:
            await ctx.message.channel.send("Nope " + ctx.message.author.mention + "...")
    else:
        await ctx.message.channel.send("No active question")

@client.command()
async def skipquestion(ctx):
    global qcurrent
    qcurrent = [False, "", []]
    await ctx.message.channel.send("Question skipped...")

@client.command()
async def cr(ctx, newreddit):
    global redditurl, redditstring, redditstuff
    redditstring = newreddit
    redditurl = "https://www.reddit.com/r/" + redditstring + "/top.json"
 
    os.system("wget -N " + redditurl)
    with open("top.json", "r") as f:
        data = f.read()
    q = json.loads(data)
    temp = []
    for child in q["data"]["children"]:
        if not child["data"]["over_18"]:
            temp.append([child["data"]["title"], child["data"]["url"]])

    redditstuff[1] = temp
    #redditstuff[1] = [[child["data"]["title"],child["data"]["url"]]for child in q["data"]["children"]]
    redditstuff[2] = len(redditstuff[1])
    redditstuff[0] = 0


    await ctx.message.channel.send("Set reddit link to: " + redditurl)



@client.command()
async def timeout(ctx, user):
    if((ctx.message.author.mention == TOBLER) or (ctx.message.author.mention == ABHI)):
        #if((user == ABHI) or (user == NOTTOBLER)):
        if((user == NOTTOBLER)):
            await ctx.message.channel.send("Nice try lol...")
            return
        else:
            #print (ctx.message.mentions[0])
            role = discord.utils.get(ctx.message.guild.roles, id=621493016150016007)
            ti = int(userDict[str(ctx.message.mentions[0].id)])
            originalrole = discord.utils.get(ctx.message.guild.roles, id=ti)
            await ctx.message.mentions[0].add_roles(role)
            await ctx.message.mentions[0].remove_roles(originalrole)

@client.command()
async def untimeout(ctx, user):
    if((ctx.message.author.mention == TOBLER) or (ctx.message.author.mention == ABHI)):
        role = discord.utils.get(ctx.message.guild.roles, id=621493016150016007)
        ti = int(userDict[str(ctx.message.mentions[0].id)])
        originalrole = discord.utils.get(ctx.message.guild.roles, id=ti)
        await ctx.message.mentions[0].remove_roles(role)
        await ctx.message.mentions[0].add_roles(originalrole)

@client.command()
async def meme(ctx):
    embed=discord.Embed(title=redditstuff[1][redditstuff[0]][0], color=0x00ff00).set_image(url=redditstuff[1][redditstuff[0]][1])
    await ctx.message.channel.send(embed=embed)
    redditstuff[0] = redditstuff[0] + 1
    if redditstuff[0] >= redditstuff[2]:
        redditstuff[0] = 0

@client.command(name="8ball", aliases=['8Ball', "8-ball", '8-Ball'])
async def eight_ball(ctx):
    await ctx.message.channel.send([
    "It is certain",
    "It is decidedly so",
    "Most likely",
    "Outlook good",
    "Signs point to yes",
    "Reply hazy, try again",
    "Ask again later",
    "Cannot predict now",
    "Concentrate and ask again",
    "Don't count on it",
    "My reply is no",
    "My sources say no",
    "Outlook not so good",
    "Very doubtful"
][random.randint(0,13)])


@client.event
async def on_message(message):
    if isinstance(message.author, discord.user.User):
        print("DIRECT MESSAGE")
        if (str(message.author.id) == ABHI[3:-1]):
            if message.content == "terminate z1x2":
                sys.exit()
            if message.content.split()[0].isdigit():
                await client.get_channel(int(message.content.split()[0])).send(" ".join(message.content.split()[1:]))

    if message.guild.id != 619566375756628027:
        return

    author = message.author
    channel = message.channel
    if author == client.user:
        return

    
    if message.content.startswith(NOTTOBLER):
        if author.mention == TOBLER:
            msg = ''
        msg = random.choice(greetings) + ' {0.author.mention}'.format(message)
        await channel.send(msg)
        print(msg)


    content = str(channel) + "@" + str(author) + ": " + str(message.content).lower()
    print(content)

    with open(fname, "a+") as f:
        f.write(content + "\n")

    for word in badwords:
        if word in message.content.lower().split():
            msg = 'Hey! Watch it {0.author.mention} - {1} sees all... Pay the Dragon!'.format(message, TOBLER)
            await channel.send(msg)

    await client.process_commands(message)  

tvShows = ["Friends", "Game of Thrones", "The Office", "Breaking Bad", "Parks and Recreation", "Criminal Minds", "Brooklyn 99", "The Walking Dead", "Person of Interest", "Agents of S.H.I.E.L.D.", "The Good Place", "Better Call Saul", "Grey's Anatomy", "Gotham"]
async def statusChange():
    while True:
        await client.change_presence(activity=discord.Activity(name=random.choice(tvShows), type=discord.ActivityType.watching))
        await asyncio.sleep(400)

redditstuff = [0, [], 999]
redditstring = "trebuchetmemes"
redditurl = "https://www.reddit.com/r/" + redditstring + "/top.json"
@client.event
async def on_ready():
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('------')
    channel = client.get_channel(619566533638881290)
    #await channel.send('me 4')
    """
    response = urlopen("https://www.reddit.com/r/trebuchetmemes/top.json")
    data = response.read().decode("utf-8")
    q = json.loads(data)
    redditstuff[1] = [child["data"]["url"] for child in q["data"]["children"]]
    redditstuff[2] = len(redditstuff[1])
    """
    os.system("wget -N " + redditurl)
    with open("top.json", "r") as f:
        data = f.read()
    q = json.loads(data)
    temp = []
    for child in q["data"]["children"]:
        if not child["data"]["over_18"]:
            temp.append([child["data"]["title"], child["data"]["url"]])

    redditstuff[1] = temp
    #redditstuff[1] = [[child["data"]["title"],child["data"]["url"]]for child in q["data"]["children"]]
    redditstuff[2] = len(redditstuff[1])

    #await client.loop.create_task(statusChange())
    await client.change_presence(activity=discord.Activity(name="with a trebuchet", type=discord.ActivityType.playing))

client.run(TOKEN)
