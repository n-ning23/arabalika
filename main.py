import discord
import os 
import io
from discord import Option
from discord.ext import commands
from dotenv import load_dotenv
from consts import *
from views import *
from utility import *
from settings import *
from teamdps import *
from rotation import *
from character import *

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
GUILD = os.getenv('DISCORD_GUILD')
bot = commands.Bot()
user_t = {}
user_r = {}
user_c = {}
user_s = {"default":Settings()}

command_description = DESCRIPTION[COMMAND_LANGUAGE]

@bot.event
async def on_ready():
    for g in bot.guilds:
        if g.name == GUILD:
            break
    print(f"{bot.user.name} has connected to Discord Server {g.name}(id: {g.id})")

@bot.before_invoke
async def on_command(ctx: commands.Context):
    try:
        s = user_s[ctx.author.id]
    except:
        s = Settings()
        user_s[ctx.author.id] = s

general = bot.create_group("general", command_description["GENERAL"])
teamdps = bot.create_group("teamdps", command_description["TEAMDPS"])
rotation = bot.create_group("rotation", command_description["ROTATION"])
character = bot.create_group("character", command_description["CHARACTER"])

@general.command(name="help", description=command_description["general help"], pass_context=True)
async def help(ctx: discord.ApplicationContext):
    s:Settings = user_s[ctx.author.id]
    await ctx.respond(f"{s.d('general help response')}")

@general.command(name="settings", decription=command_description["general settings"], pass_context=True)
async def settings(ctx: discord.ApplicationContext):
    s:Settings = user_s[ctx.author.id]
    view = SettingsView(timeout = TIME)
    view.create(s)
    await ctx.respond(f"", view=view, ephemeral=True)

#TEAMDPS----------------------------------------------------------------------------------------------------

'''CREATE COMMAND
name:str, desc:str
Bot creates the team dps embed.
'''
@teamdps.command(name="create", description=command_description["teamdps create"], pass_context=True)
@discord.option(
    "name",
    description=command_description["teamdps name"],
    required=True
)
@discord.option(
    "desc",
    description=command_description["teamdps description"],
    required=True
)
async def create(
    ctx: discord.ApplicationContext,
    name: str,
    desc: str 
):
    if (ctx.author.id not in user_t):
        user_t[ctx.author.id]=Team()
    t:Team = user_t[ctx.author.id]
    try:
        t.create(name,desc)
    except Exception as e:
        await ctx.respond(f"ERROR: {e}")
        raise Exception(e)
    s:Settings = user_s[ctx.author.id]
    await ctx.respond(f"{s.d('teamdps create response')}", ephemeral=True)

#ROTATION----------------------------------------------------------------------------------------------------

'''CREATE COMMAND
seconds:int, columns:int
Bot sends an embed that creates the rotation
'''
@rotation.command(name="create", description=command_description["rotation create"], pass_context=True)
@discord.option(
    "seconds",
    description=command_description["rotation seconds"],
    required=True
)
@discord.option(
    "columns",
    description=command_description["rotation columns"],
    required=False,
    default=1
)
async def create(
    ctx: discord.ApplicationContext,
    seconds: int,
    columns: int 
):
    if (ctx.author.id not in user_r):
        user_r[ctx.author.id]=Rotation()
    r:Rotation = user_r[ctx.author.id]
    try:
        s:Settings = user_s[ctx.author.id]
        r.create(s, seconds,columns)
    except Exception as e:
        await ctx.respond(f"ERROR: {e}")
        raise Exception(e)
    embed, image = embedRotation(r, s, ctx)
    await ctx.respond(f"{s.d('rotation create response')}", embed=embed, file=image, ephemeral=True)

'''ADD COMMAND
desc:str, interval:str, column:int
Bot sends an embed after adding
'''
@rotation.command(name="add", description=command_description["rotation add"], pass_context=True)
@discord.option(
    "desc",
    description=command_description["rotation description"],
    required=True
)
@discord.option(
    "interval",
    description=command_description["rotation interval"],
    required=True
)
@discord.option(
    "column",
    description=command_description["rotation column"],
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
        r:Rotation = user_r[ctx.author.id]
    except:
        await ctx.respond(f"ERROR: please use rotation create first")
        raise Exception("Rotation not found.")
    try:
        if ('-' in interval):
            start,end = interval.split("-")
        else:
            start = interval
            end = interval
        r.add(desc,int(start),int(end),column)
    except Exception as e:
        await ctx.respond(f"ERROR: {e}")
        raise Exception(e)
    s:Settings = user_s[ctx.author.id]
    embed, image = embedRotation(r, s, ctx)
    await ctx.respond(f"{s.d('rotation add response')}", embed=embed, file=image, ephemeral=True)

'''REMOVE COMMAND
interval:str, column:int
Bot sends an embed after removing
'''
@rotation.command(name="remove", description=command_description["rotation remove"], pass_context=True)
@discord.option(
    "interval",
    description=command_description["rotation interval"],
    required=True
)
@discord.option(
    "column",
    description=command_description["rotation column"],
    required=False,
    default=1
)
async def remove(
    ctx: discord.ApplicationContext,
    interval: str,
    column: int 
):
    try:
        r:Rotation = user_r[ctx.author.id]
    except:
        await ctx.respond(f"ERROR: please use rotation create first")
        raise Exception("Rotation not found.")
    try:
        if ('-' in interval):
            start,end = interval.split("-")
        else:
            start = interval
            end = interval
        r.remove(int(start),int(end),column)
    except Exception as e:
        await ctx.respond(f"ERROR: {e}")
        raise Exception(e)
    s:Settings = user_s[ctx.author.id]
    embed, image = embedRotation(r, s, ctx)
    await ctx.respond(f"{s.d('rotation remove response')}", embed=embed, file=image, ephemeral=True)

'''ADDCOL COMMAND
column:int
Bot sends an embed after adding a column
'''
@rotation.command(name="addcol", description=command_description["rotation addcol"], pass_context=True)
@discord.option(
    "column",
    description=command_description["rotation column"],
    required=True
)
async def addcol(
    ctx: discord.ApplicationContext,
    column: int 
):
    try:
        r:Rotation = user_r[ctx.author.id]
    except:
        await ctx.respond(f"ERROR: please use rotation create first")
        raise Exception("Rotation not found.")
    try:
        r.addColumn(column)
    except Exception as e:
        await ctx.respond(f"ERROR: {e}")
        raise Exception(e)
    s:Settings = user_s[ctx.author.id]
    embed, image = embedRotation(r, s, ctx)
    await ctx.respond(f"{s.d('rotation addcol response')}", embed=embed, file=image, ephemeral=True)

'''REMOVECOL COMMAND
column:int
Bot sends an embed after removing a column
'''
@rotation.command(name="removecol", description=command_description["rotation removecol"], pass_context=True)
@discord.option(
    "column",
    description=command_description["rotation column"],
    required=True
)
async def removecol(
    ctx: discord.ApplicationContext,
    column: int 
):
    try:
        r:Rotation = user_r[ctx.author.id]
    except:
        await ctx.respond(f"ERROR: please use rotation create first")
        raise Exception("Rotation not found.")
    try:
        r.removeColumn(column)
    except Exception as e:
        await ctx.respond(f"ERROR: {e}")
        raise Exception(e)
    s:Settings = user_s[ctx.author.id]
    embed, image = embedRotation(r, s, ctx)
    await ctx.respond(f"{s.d('rotation removecol response')}", embed=embed, file=image, ephemeral=True)

'''DISPLAY COMMAND
Bot sends an embed
'''
@rotation.command(name="display", description=command_description["rotation display"], pass_context=True)
async def display(
    ctx: discord.ApplicationContext
):
    try:
        r:Rotation = user_r[ctx.author.id]
    except:
        await ctx.respond(f"ERROR: please use rotation create first")
        raise Exception("Rotation not found.")
    try:
        r.display()
    except Exception as e:
        await ctx.respond(f"ERROR: {e}")
        raise Exception(e)
    s:Settings = user_s[ctx.author.id]
    embed, image = embedRotation(r, s, ctx)
    await ctx.respond(f"", embed=embed, file=image)

#CHARACTER----------------------------------------------------------------------------------------------------

'''CREATE COMMAND
name:str, desc:str
Bot sends a message that the character is created
'''
@character.command(name="create", description=command_description["character create"], pass_context=True)
@discord.option(
    "name",
    description=command_description["character name"],
    required=True
)
@discord.option(
    "desc",
    description=command_description["character description"],
    required=False,
    default=""
)
async def create(
    ctx: discord.ApplicationContext,
    name: str,
    desc: str
):
    if (ctx.author.id not in user_c):
        user_c[ctx.author.id]=[Character()]
    elif (len(user_c[ctx.author.id]) == 4):
        user_c[ctx.author.id]=[Character()]
    else:
        user_c[ctx.author.id].append(Character())
    c:Character = user_c[ctx.author.id][-1]
    try:
        s:Settings = user_s[ctx.author.id]
        c.create(s, name, desc)
    except Exception as e:
        await ctx.respond(f"ERROR: {e}")
        raise Exception(e)
    embed, image = embedCharacter(c, s, ctx)
    await ctx.respond(f"{s.d('character create response')}{name}.", embed=embed, file=image, ephemeral=True)

'''EDIT COMMAND
id:int, name:str, desc:str
Bot sends a message that the character has been edited
'''
@character.command(name="edit", description=command_description["character edit"], pass_context=True)
@discord.option(
    "id",
    description="",
    required=False,
    default=0
)
@discord.option(
    "name",
    description=command_description["character name"],
    required=False,
    default=""
)
@discord.option(
    "desc",
    description=command_description["character description"],
    required=False,
    default=""
)
async def edit(
    ctx: discord.ApplicationContext,
    id: int,
    name: str,
    desc: str
):
    try:
        c = user_c[ctx.author.id][id]
    except:
        await ctx.respond(f"ERROR: character not found")
        raise Exception("Character not found.")
    try:
        if (name != ""):
            c.setName(name)
        if (description != ""):
            c.setDesc(description)
    except Exception as e:
        await ctx.respond(f"ERROR: {e}", delete_after=10)
        raise Exception(e)
    s:Settings = user_s[ctx.author.id]
    await ctx.respond(f"{s.d('character edit response')}{c.getName()}.", ephemeral=True)

'''LIST COMMAND
Bot sends an embed that lists all current characters
'''
@character.command(name="list", description=command_description["character list"], pass_context=True)
async def listAll(
    ctx: discord.ApplicationContext
):
    try:
        clist:[Character] = user_c[ctx.author.id]
    except Exception as e:
        await ctx.respond(f"ERROR: please use character create first")
        raise Exception(e)
    s:Settings = user_s[ctx.author.id]
    overall = discord.Embed(title=f"{s.d('character list response')}{len(clist)}")
    for c_index in range(0,len(clist)):
        c = clist[c_index]
        embed, image = embedCharacter(c, s, ctx)
        await ctx.respond(f"", embed=embed, file=image)
        overall.add_field(name=f"ID:{c_index}", value=c.getName(), inline = False)
    await ctx.respond(f"", embed=overall)

'''BASE COMMAND
id:int, hp:int, atk:int, def:int, em:int, crate:float, cdmg:float, er:float, ele:float, heal:float
Bot sends a message that returns the stats of the character
'''
@character.command(name="base", description=command_description['character base'], pass_context=True)
@discord.option(
    "id",
    description="",
    required=False,
    default=0
)
@discord.option(
    "health",
    description=command_description["hp"],
    required=False,
    default=-1
)
@discord.option(
    "attack",
    description=command_description["base atk"],
    required=False,
    default=-1
)
@discord.option(
    "defense",
    description=command_description["def"],
    required=False,
    default=-1
)
@discord.option(
    "em",
    description=command_description["em"],
    required=False,
    default=-1
)
@discord.option(
    "crate",
    description=command_description["crate"],
    required=False,
    default=-1
)
@discord.option(
    "cdmg",
    description=command_description["cdmg"],
    required=False,
    default=-1
)
@discord.option(
    "er",
    description=command_description["er"],
    required=False,
    default=-1
)
@discord.option(
    "ele",
    description=command_description["ele"],
    required=False,
    default=-1
)
@discord.option(
    "heal",
    description=command_description["heal"],
    required=False,
    default=-1
)
async def base(
    ctx: discord.ApplicationContext,
    id: int,
    health: int,
    attack: int,
    defense: int,
    em: int,
    crate: float,
    cdmg: float,
    er: float,
    ele: float,
    heal: float
):
    try:
        c = user_c[ctx.author.id][id]
    except:
        await ctx.respond(f"ERROR: character not found")
        raise Exception("Character not found.")
    try:
        c.base(health, attack, defense, em, crate, cdmg, er, ele, heal)
    except Exception as e:
        await ctx.respond(f"ERROR: {e}", delete_after=10)
        raise Exception(e)
    s:Settings = user_s[ctx.author.id]
    embed, image = embedCharacter(c, s, ctx)
    await ctx.respond(f"{s.d('character base response')}{c.getName()}.", embed=embed, file=image, ephemeral=True)
    
'''ARTIFACTS COMMAND
id:int, hp:int, atk:int, def:int, em:int, crit:int, er:int
Bot sends a message that returns the stats of the character
'''
@character.command(name="artifacts", description=command_description["character artifacts"], pass_context=True)
@discord.option(
    "id",
    description="",
    required=False,
    default=0
)
@discord.option(
    "health",
    description=command_description["hp"],
    required=False,
    default=-1
)
@discord.option(
    "attack",
    description=command_description["atk"],
    required=False,
    default=-1
)
@discord.option(
    "defense",
    description=command_description["def"],
    required=False,
    default=-1
)
@discord.option(
    "em",
    description=command_description["em"],
    required=False,
    default=-1
)
@discord.option(
    "crate",
    description=command_description["crate"],
    required=False,
    default=-1
)
@discord.option(
    "cdmg",
    description=command_description["cdmg"],
    required=False,
    default=-1
)
@discord.option(
    "er",
    description=command_description["er"],
    required=False,
    default=-1
)
async def artifacts(
    ctx: discord.ApplicationContext,
    id: int,
    health: float,
    attack: float,
    defense: float,
    em: float,
    crate: float,
    cdmg: float,
    er: float
):
    try:
        c = user_c[ctx.author.id][id]
    except:
        await ctx.respond(f"ERROR: character not found.")
        raise Exception("Character not found.")
    try:
        c.subs(health, attack, defense, em, crate, cdmg, er)
    except Exception as e:
        await ctx.respond(f"ERROR: {e}")
        raise Exception(e)
    s:Settings = user_s[ctx.author.id]
    view = ArtifactView(timeout = TIME)
    view.create(c, s, ctx)
    embed, image = embedCharacter(c, s, ctx)
    await ctx.respond(f"{s.d('character artifacts response')}{c.getName()}...", embed=embed, file=image, view=view, ephemeral=True)

'''PERCENT COMMAND
id:int, hp:float, atk:float, def:float
Bot sends a message that returns the stats of the character
'''
@character.command(name="percent", description=command_description["character percent"], pass_context=True)
@discord.option(
    "id",
    description="",
    required=False,
    default=0
)
@discord.option(
    "health",
    description=command_description["hp"],
    required=False,
    default=-1
)
@discord.option(
    "attack",
    description=command_description["atk"],
    required=False,
    default=-1
)
@discord.option(
    "defense",
    description=command_description["def"],
    required=False,
    default=-1
)
async def percent(
    ctx: discord.ApplicationContext,
    id: int,
    health: float,
    attack: float,
    defense: float
):
    try:
        c = user_c[ctx.author.id][id]
    except:
        await ctx.respond(f"ERROR: character not found")
        raise Exception("Character not found.")
    try:
        c.percent(health, attack, defense)
    except Exception as e:
        await ctx.respond(f"ERROR: {e}", delete_after=10)
        raise Exception(e)
    s:Settings = user_s[ctx.author.id]
    embed, image = embedCharacter(c, s, ctx)
    await ctx.respond(f"{s.d('character percent response')}{c.getName()}.", embed=embed, file=image, ephemeral=True)

'''FLAT COMMAND
id:int, hp:int, atk:int, def:int, em:int, crate:float, cdmg:float, er:float, ele:float, heal:float
Bot sends a message that returns the stats of the character
'''
@character.command(name="flat", description=command_description["character flat"], pass_context=True)
@discord.option(
    "id",
    description="",
    required=False,
    default=0
)
@discord.option(
    "health",
    description=command_description["hp"],
    required=False,
    default=-1
)
@discord.option(
    "attack",
    description=command_description["atk"],
    required=False,
    default=-1
)
@discord.option(
    "defense",
    description=command_description["def"],
    required=False,
    default=-1
)
@discord.option(
    "em",
    description=command_description["em"],
    required=False,
    default=-1
)
@discord.option(
    "crate",
    description=command_description["crate"],
    required=False,
    default=-1
)
@discord.option(
    "cdmg",
    description=command_description["cdmg"],
    required=False,
    default=-1
)
@discord.option(
    "er",
    description=command_description["er"],
    required=False,
    default=-1
)
@discord.option(
    "ele",
    description=command_description["ele"],
    required=False,
    default=-1
)
@discord.option(
    "heal",
    description=command_description["heal"],
    required=False,
    default=-1
)
async def flat(
    ctx: discord.ApplicationContext,
    id: int,
    health: int,
    attack: int,
    defense: int,
    em: int,
    crate: float,
    cdmg: float,
    er: float,
    ele: float,
    heal: float
):
    try:
        c = user_c[ctx.author.id][id]
    except:
        await ctx.respond(f"ERROR: character not found")
        raise Exception("Character not found.")
    try:
        c.flat(health, attack, defense, em, crate, cdmg, er, ele, heal)
    except Exception as e:
        await ctx.respond(f"ERROR: {e}", delete_after=10)
        raise Exception(e)
    s:Settings = user_s[ctx.author.id]
    embed, image = embedCharacter(c, s, ctx)
    await ctx.respond(f"{s.d('character flat response')}{c.getName()}.", embed=embed, file=image, ephemeral=True)

'''OPTCRIT COMMAND
id:int
Bot sends a message that returns the stats of the character
'''
@character.command(name="optcrit", description=command_description["character optcrit"], pass_context=True)
@discord.option(
    "id",
    description="",
    required=False,
    default=0
)
async def optcrit(
    ctx: discord.ApplicationContext,
    id: int
):
    try:
        c = user_c[ctx.author.id][id]
    except:
        await ctx.respond(f"ERROR: character not found")
        raise Exception("Character not found.")
    try:
        c.optimizeCrit()
    except Exception as e:
        await ctx.respond(f"ERROR: {e}", delete_after=10)
        raise Exception(e)
    s:Settings = user_s[ctx.author.id]
    embed, image = embedCharacter(c, s, ctx)
    await ctx.respond(f"{s.d('character optcrit response')}{c.getName()}", embed=embed, file=image, ephemeral=True)

'''ENERGY COMMAND
id:int, burst:int, onSame:int, offSame:int, onDiff:int, offDiff:int, onNone:int, offNone:int, fixed:int
Bot sends a message that returns the stats of the character
'''
@character.command(name="energy", description=command_description["character energy"], pass_context=True)
@discord.option(
    "burst",
    description=command_description["character burst"],
    required=True
)
@discord.option(
    "onsame",
    description=command_description["character onsame"],
    required=False,
    default=0
)
@discord.option(
    "offsame",
    description=command_description["character offsame"],
    required=False,
    default=0
)
@discord.option(
    "ondiff",
    description=command_description["character ondiff"],
    required=False,
    default=0
)
@discord.option(
    "offdiff",
    description=command_description["character offdiff"],
    required=False,
    default=0
)
@discord.option(
    "onnone",
    description=command_description["character onnone"],
    required=False,
    default=0
)
@discord.option(
    "offnone",
    description=command_description["character offnone"],
    required=False,
    default=0
)
@discord.option(
    "fixed",
    description=command_description["character fixed"],
    required=False,
    default=0
)
@discord.option(
    "id",
    description="",
    required=False,
    default=0
)
async def flat(
    ctx: discord.ApplicationContext,
    burst: int,
    onsame: int,
    offsame: int,
    ondiff: int,
    offdiff: int,
    onnone: int,
    offnone: int,
    fixed: int,
    id: int
):
    try:
        c = user_c[ctx.author.id][id]
    except:
        await ctx.respond(f"ERROR: character not found")
        raise Exception("Character not found.")
    try:
        req = c.energy(burst, onsame, offsame, ondiff, offdiff, onnone, offnone, fixed)
    except Exception as e:
        await ctx.respond(f"ERROR: {e}", delete_after=10)
        raise Exception(e)
    s:Settings = user_s[ctx.author.id]
    embed = discord.Embed(title=f"{c.getName()}", color=s.color())
    embed.add_field(name=s.d("character current energy"), value=f"{c.getStats()[6]}", inline = False)
    embed.add_field(name=s.d("character required energy"), value=f"{req}", inline = False)
    await ctx.respond(f"", embed=embed, ephemeral=True)

# RUNNING THE BOT

bot.run(TOKEN)