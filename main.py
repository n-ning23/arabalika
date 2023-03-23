import discord
import os 
from discord import Option
from discord.ext import commands
from dotenv import load_dotenv
from rotation import *

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
GUILD = os.getenv('DISCORD_GUILD')
bot = commands.Bot()
user_rStart = {}

@bot.event
async def on_ready():
    for g in bot.guilds:
        if g.name == GUILD:
            break
    print(f"{bot.user.name} has connected to Discord Server {g.name}(id: {g.id})")

rotation = bot.create_group("rotation", "Create and edit a rotation.")

'''RSTART COMMAND
name:str, seconds:int, columns:int
Bot sends an embed that creates the start
'''
@rotation.command(name="start", description="Start rotation", pass_context=True)
@discord.option(
    "name",
    description="Name of the team",
    required=True
)
@discord.option(
    "seconds",
    description="# of seconds in the rotation",
    required=True
)
@discord.option(
    "columns",
    description="# of columns",
    required=False,
    default=1
)
async def start(
    ctx: discord.ApplicationContext,
    name: str,
    seconds: int,
    columns: int 
):
    if (ctx.author.id not in user_rStart):
        user_rStart[ctx.author.id]=Rotation()
    r:Rotation = user_rStart[ctx.author.id]
    try:
        r.rStart(seconds,columns,name)
    except Exception as e:
        await ctx.respond(f"ERROR: {e}")
        raise Exception(e)
    embed = discord.Embed(title=r.rGetTitle(),description="Current Rotation",color=0xFF00FF)
    embed.set_author(name=ctx.author.name,icon_url=ctx.author.avatar.url)
    embed.add_field(name=f"Rotation Duration: {seconds}s", value=f"```{r.rGetText()}```")
    await ctx.respond(f"You have created the following rotation:", embed=embed, delete_after=10)

'''RADD COMMAND
desc:str, interval:str, column:int
Bot sends an embed after adding
'''
@rotation.command(name="add", description="Add to rotation", pass_context=True)
@discord.option(
    "desc",
    description="Character name and skills used",
    required=True
)
@discord.option(
    "interval",
    description="time interval in the format 'startTime-endTime'",
    required=True
)
@discord.option(
    "column",
    description="# of column",
    required=False,
    default=1
)
async def add(
    ctx: discord.ApplicationContext,
    desc: str,
    interval: str,
    column: int 
):
    try:
        r:Rotation = user_rStart[ctx.author.id]
    except:
        await ctx.respond(f"ERROR: please use rotation start first")
    try:
        if ('-' in interval):
            start,end = interval.split("-")
        else:
            start = interval
            end = interval
        r.rAdd(desc,int(start),int(end),column)
    except Exception as e:
        await ctx.respond(f"ERROR: {e}")
        raise Exception(e)
    embed = discord.Embed(title=r.rGetTitle(),description=f"Current Rotation",color=0xFF00FF)
    embed.set_author(name=ctx.author.name,icon_url=ctx.author.avatar.url)
    embed.add_field(name=f"Rotation Duration: {r.rGetDim()[0]}s", value=f"```{r.rGetText()}```")
    await ctx.respond(f"After adding an action:", embed=embed, delete_after=10)

'''RREMOVE COMMAND
interval:str, column:int
Bot sends an embed after removing
'''
@rotation.command(name="remove", description="Remove from rotation", pass_context=True)
@discord.option(
    "interval",
    description="time interval in the format 'startTime-endTime'",
    required=True
)
@discord.option(
    "column",
    description="# of column",
    required=False,
    default=1
)
async def remove(
    ctx: discord.ApplicationContext,
    interval: str,
    column: int 
):
    try:
        r:Rotation = user_rStart[ctx.author.id]
    except:
        await ctx.respond(f"ERROR: please use rotation start first")
    try:
        if ('-' in interval):
            start,end = interval.split("-")
        else:
            start = interval
            end = interval
        r.rRemove(int(start),int(end),column)
    except Exception as e:
        await ctx.respond(f"ERROR: {e}")
        raise Exception(e)
    embed = discord.Embed(title=r.rGetTitle(),description=f"Current Rotation",color=0xFF00FF)
    embed.set_author(name=ctx.author.name,icon_url=ctx.author.avatar.url)
    embed.add_field(name=f"Rotation Duration: {r.rGetDim()[0]}s", value=f"```{r.rGetText()}```")
    await ctx.respond(f"After removing an action:", embed=embed, delete_after=10)

'''RADDCOL COMMAND
column:int
Bot sends an embed after adding a column
'''
@rotation.command(name="addcol", description="Add a column", pass_context=True)
@discord.option(
    "column",
    description="# of column",
    required=True
)
async def addcol(
    ctx: discord.ApplicationContext,
    column: int 
):
    try:
        r:Rotation = user_rStart[ctx.author.id]
    except:
        await ctx.respond(f"ERROR: please use rotation start first")
    try:
        r.rAddColumn(column)
    except Exception as e:
        await ctx.respond(f"ERROR: {e}")
        raise Exception(e)
    embed = discord.Embed(title=r.rGetTitle(),description=f"Current Rotation",color=0xFF00FF)
    embed.set_author(name=ctx.author.name,icon_url=ctx.author.avatar.url)
    embed.add_field(name=f"Rotation Duration: {r.rGetDim()[0]}s", value=f"```{r.rGetText()}```")
    await ctx.respond(f"After adding a column:", embed=embed, delete_after=10)

'''RREMOVECOL COMMAND
column:int
Bot sends an embed after removing a column
'''
@rotation.command(name="removecol", description="Remove a column", pass_context=True)
@discord.option(
    "column",
    description="# of column",
    required=True
)
async def removecol(
    ctx: discord.ApplicationContext,
    column: int 
):
    try:
        r:Rotation = user_rStart[ctx.author.id]
    except:
        await ctx.respond(f"ERROR: please use rotation start first")
    try:
        r.rRemoveColumn(column)
    except Exception as e:
        await ctx.respond(f"ERROR: {e}")
        raise Exception(e)
    embed = discord.Embed(title=r.rGetTitle(),description=f"Current Rotation",color=0xFF00FF)
    embed.set_author(name=ctx.author.name,icon_url=ctx.author.avatar.url)
    embed.add_field(name=f"Rotation Duration: {r.rGetDim()[0]}s", value=f"```{r.rGetText()}```")
    await ctx.respond(f"After removing a column:", embed=embed, delete_after=10)

'''RDISPLAY COMMAND
Bot sends an embed
'''
@rotation.command(name="display", description="Display your rotation", pass_context=True)
async def display(
    ctx: discord.ApplicationContext,
):
    try:
        r:Rotation = user_rStart[ctx.author.id]
    except:
        await ctx.respond(f"ERROR: please use rotation start first")
        raise Exception(e)
    embed = discord.Embed(title=r.rGetTitle(),description=f"Current Rotation",color=0xFF00FF)
    embed.set_author(name=ctx.author.name,icon_url=ctx.author.avatar.url)
    embed.add_field(name=f"Rotation Duration: {r.rGetDim()[0]}s", value=f"```{r.rGetText()}```")
    await ctx.respond(f"", embed=embed)

bot.run(TOKEN)