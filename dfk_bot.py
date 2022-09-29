import discord #for the discord bot
from discord.ext import commands #for the discord bot to work
from web_scraper import * #Where we make practice buys
import datetime
import time
from discord.ext import tasks
import threading

client = discord.Client()

client = commands.Bot(command_prefix='!')


@client.event
async def on_ready(): 
    print('WE have logged in as {0.user}'.format(client))

@client.event
async def on_guild_join(guild): 
    #Creates a role for members to see the rsi bot channel
    role_perms = discord.Permissions(send_messages=False, read_messages=True)
    #name = channel name, permissions = persmissions user has, https://discordpy.readthedocs.io/en/stable/api.html#permissions
    await guild.create_role(name = 'Bot User', permissions = role_perms)
    newCat = await guild.create_category_channel(name = 'Sparkybot') # saves created category into variable 

    overwrites = {
        guild.default_role: discord.PermissionOverwrite(read_messages = True, send_messages = False),
    }

    channel = await guild.create_text_channel('Bot Comamnds', overwrites = overwrites, category = newCat)

async def display_hero():
    await client.wait_until_ready()
    channel = client.get_channel(id = 937369402020605963) # Channel ID it sends the message in
    while not client.is_closed():
        heros = make_data()
        for hero_data in heros:
            print(hero_data)
            if(hero_data):
                if(hero_data != 'E'):
                    if(hero_data[3] == 'Common'):
                        color = discord.Colour.dark_grey()
                    if(hero_data[3] == 'Uncommon'):
                        color = discord.Colour.green()
                    if(hero_data[3] == 'Rare'):
                        color = discord.Colour.blue()
                    if(hero_data[3] == 'Legendary'):
                        color = discord.Colour.orange()
                    if(hero_data[3] == 'Mythic'):
                        color = discord.Colour.purple()
                    embed = discord.Embed(
                        title = hero_data[0],
                        description = hero_data[1],
                        colour = color
                        )
                    embed.set_image(url = 'https://i.gyazo.com/5cb1d59872de240f250b2462a3e9272e.png')

                    top_right = 'https://i.gyazo.com/ebcfbd1b5e50a6ea86bdbe30feb9630c.png'
                    embed.set_thumbnail(url = top_right)

                    embed.set_author(name = hero_data[2],
                    icon_url = 'https://cdn.discordapp.com/attachments/863202522193592320/863222849665630228/https3A2F2Fd1e00ek4ebabms.png')

                    embed.add_field(name='Profession Value:', value = hero_data[8], inline=False)
                    embed.add_field(name='Level:', value = hero_data[5], inline=False)
                    embed.add_field(name='Gen:', value = hero_data[6], inline=False)
                    embed.add_field(name='Summons:', value = hero_data[7], inline=False)
                    embed.add_field(name='Boosts:', value = hero_data[4], inline=False)
                    embed.set_footer(text = hero_data[9])
                    await channel.send(embed=embed)
                else:
                    time.sleep(60)



client.loop.create_task(display_hero())
client.run('ODYwNzQ2ODQxNTE1MzYwMjc3.YN_u9g.YBEfkB0xQgg7sxaq_uzYMdVU3c4')

