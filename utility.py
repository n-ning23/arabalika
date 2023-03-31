import discord
from settings import *
from rotation import *
from character import *

def embedRotation(r:Rotation, s:Settings, ctx):
    image = discord.File(r.getImage(),"image.png")
    color = int("0x"+s.color()[1:],16)
    embed = discord.Embed(title=f"{s.d('embedRotation')}{r.getDim()[0]}s", color=color)
    embed.set_author(name=ctx.author.name,icon_url=ctx.author.avatar.url)
    embed.set_image(url="attachment://image.png")
    return embed,image
def embedCharacter(c:Character, s:Settings, ctx):
    image = discord.File(c.getImage(),"image.png")
    color = int("0x"+s.color()[1:],16)
    embed = discord.Embed(title=f"{c.getName()}", color=color)
    embed.set_author(name=ctx.author.name,icon_url=ctx.author.avatar.url)
    embed.set_image(url="attachment://image.png")
    if (c.getDesc() != ""):
        embed.add_field(name=f"{s.d('embedCharacter')}", value=f"{c.getDesc()}", inline = False)
    subs = c.getSubs()
    subs = list(filter(lambda x: x[1] != 0, subs))
    if (len(subs) != 0):
        embed.add_field(name=s.d("effective rolls"), value="", inline = False)
        for sub_key, sub_value in subs:
            embed.add_field(name=sub_key, value=round(sub_value, 2))
    return embed,image