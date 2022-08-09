import discord
from discord.ext import commands
import asyncio
import json
from json.decoder import JSONDecodeError

bot = commands.Bot(command_prefix='!')
last_Ids = []


@bot.event
async def on_ready():
    print('We have logged in as {0.user}'.format(bot))


@bot.event
async def on_disconnect():
    print("déconnecté")


@bot.command()
async def ping(ctx):
    await ctx.channel.send("pong")


@bot.command()
async def embed(ctx):
    embed = discord.Embed(title="Sample Embed", url="https://realdrewdata.medium.com/",
                          description="This is an embed that will show how to build an embed and the different components",
                          color=0xFF5733)
    await ctx.send(embed=embed)


async def displayNewProducts():
    await bot.wait_until_ready()
    channel_tshirts = bot.get_channel(id=980949680655597588)
    channel_sneakers = bot.get_channel(id=980949675714691122)
    channel_pants = bot.get_channel(id=982231045111943218)
    channel_accessories = bot.get_channel(id=982233554668879933)
    channel_3d_swhoosh = bot.get_channel(id=982626172326273084)
    channel_af1 = bot.get_channel(id=984185518025760799)
    while not bot.is_closed():
        try:
            items = json.load(open("data.json"))
            global last_Ids

            for item_list in items:
                for i in range(3):
                    item = items[item_list][i]

                    if item["id"] not in last_Ids:
                        last_Ids.append(item["id"])
                        embed = discord.Embed(title=item["title"], url=item["url"],
                                              color=0xFF5733)
                        try :
                            embed.set_image(url=item["photo"]["full_size_url"])
                        except Exception as e:
                            print(e)
                        embed.add_field(name="Prix", value=item["price"] + " €", inline=True)
                        if item['size_title'] != "": embed.add_field(name="Taille", value=item['size_title'],
                                                                     inline=True)
                        if item['brand_title'] != "": embed.add_field(name="Marque", value=item["brand_title"],
                                                                      inline=False)

                        if item_list == "tshirts":
                            await channel_tshirts.send(embed=embed)
                        if item_list == "sneakers": await channel_sneakers.send(embed=embed)
                        if item_list == "pants": await channel_pants.send(embed=embed)
                        if item_list == "accessories": await channel_accessories.send(embed=embed)
                        if item_list == "3d_swhoosh": await channel_3d_swhoosh.send(embed=embed)
                        if item_list == "af1": await channel_af1.send(embed=embed)

                        if len(last_Ids) > 200:
                            last_Ids.pop()
                            last_Ids.append(item["id"])
                        else:
                            last_Ids.append(item["id"])

            await asyncio.sleep(5)
        except JSONDecodeError:
            await asyncio.sleep(5)
            pass


bot.loop.create_task(displayNewProducts())
bot.run('OTQwMDEyMTAwOTkzMDQ4NTc2.G32YYL.M9ipgBZ5qpqRq9fmVn7cpVKlHAmOIvHtTzce1Q')
