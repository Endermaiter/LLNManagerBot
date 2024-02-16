#!/usr/bin/env python3.10

import datetime
import os
import io

import discord
from discord.ext import commands
from urllib.parse import urlparse
import aiohttp
from pathlib import Path
from opgg.opgg import OPGG
from opgg.summoner import Summoner
from opgg.params import Region

# Discord bot preconfiguration
bot = commands.Bot(command_prefix="!", intents=discord.Intents.all())


# Check discord bot is up and running
@bot.event
async def on_ready():
    print(f"Conectado como: {bot.user}")


# List of players command
@bot.command()
async def participantes(ctx):
    author_nickname = ctx.author.nick
    if author_nickname is None:
        author_name = ctx.author.name
    else:
        author_name = author_nickname

    header = ("Lista detallada con todos los participantes del torneo:\n"
              "\n**Nombre DC**‎‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ "
              "**Nombre Riot**‎‎ ‎ ‎ ‎  ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ "
              "**ELO**‎‎ ‎ ‎ ‎ ‎ ‎ ‎‎ ‎ ‎ ‎ ‎ ‎ ‎  ‎ ‎ ‎ ‎ "
              "**Posición**\n---------------------------------------------------------------------\n")
    roicetee = "\nRoicetee      MNC Roicetee    Hierro 1  JGL/SUPP"
    endermaiter = "\nEndermaiter   Endermaiter     Oro 1     ADC/TOP"
    alex = "\nalex132       alex132mini     Plata 3   TOP/JGL"
    dani = "\ndrd91         NeoZoro91       Bronce 4  MID/TOP"
    victor = "\nVictor        Calp17a         Bronce 3  MID/SUPP"
    neisan = "\nNath          M4NIN           Esmd 2    JGL/MID"
    ion = "\nIontxas       Iontxas         Bronce 4  ADC/SUPP"
    jeff = "\nel jefelson   MNC Je1feR      Bronce 1  MID/JGL"
    daniC = "\nDanicoru23    Danicoru23      Bronce 4  TOP/SUPP"
    janai = "\njanaihdez     MNC Tom Baker   Plata 2   SUPP/MID"
    rast = "\nelRast        xXelRastXx      Bronce 3  JGL/TOP"
    wolframe = "\nWOLFR4ME      Wolfr4me        Esmd 2    JGL/MID"
    geko = "\ngeko          Geko            Bronce 2  MID/JGL"
    yatekomo = "\nYatekomo      yateloquisimo   Hierro 1  JGL/TOP"
    neno = "\nAleja IV      LordRevelius    Plata 4   MID/TOP"
    daniR = "\ndanirumbo     JULIAN ROSS     Bronce 2  ADC/MID"
    abdiel = "\nAbdiel        stoyknsadojefe  Hierro 1  MID"
    pepis = "\nEl Pepis      unix989         Oro 2     BOT/ TOP"
    ferroviario = "\nFerroviario   Ferroviario     Bronce 4  BOT/TOP"
    ale = "\nAle           alejandro100000 Plata 3   JGL/SUPP"
    erlitam = "\nErlitam       erlitam         Bronce 2  ADC/SUPP"
    Mouk = "\nMouk          MoyKQ           Hierro 3  MID/TOP"
    izan = "\nIzan          OledorDeAxilas  Hierro 3  TOP/JGL"
    chopi = "\nchopi         ChopiTHEpro1    Hierro 4  N/A"
    andoni = "\nAndoni        PFAndoni        Hierro 4  JGL/TOP"
    url_image = "https://cdn.discordapp.com/attachments/1027500125670604843/1205254709179449394/image.png?ex=65d7b3eb&is=65c53eeb&hm=e0bda835cd7be084aa7f5b1d29a34b5ff86d50236ba6ac9142bde6d2df45fe6e&"
    url_icon = "https://cdn.discordapp.com/attachments/844311976888893440/1204121772966944819/Imagen_de_WhatsApp_2023-11-10_a_las_10.png?ex=65d394ca&is=65c11fca&hm=c3c76a99234ad5b7c582c8f0153fc584a8433e54bfcb787a5ced69d694fc4566&"

    embed = discord.Embed(title="Participantes del torneo",
                          description=header +
                                      "```" +
                                      roicetee +
                                      endermaiter +
                                      alex +
                                      dani +
                                      victor +
                                      neisan +
                                      ion +
                                      jeff +
                                      daniC +
                                      janai +
                                      rast +
                                      wolframe +
                                      geko +
                                      yatekomo +
                                      neno +
                                      daniR +
                                      abdiel +
                                      pepis +
                                      ferroviario +
                                      ale +
                                      erlitam +
                                      Mouk +
                                      izan +
                                      chopi +
                                      andoni +
                                      "\n```",
                          colour=0xff0000,
                          timestamp=datetime.datetime.now())
    embed.set_author(name=f"Hola {author_name}!")
    embed.set_image(
        url=url_image)
    embed.set_footer(text="LLN Manager",
                     icon_url=url_icon)

    await ctx.send(embed=embed)

@bot.command()
async def equipos(ctx):
    url = "https://media.discordapp.net/attachments/1202377573506482247/1207665350230020169/BANNER_FINAL.png?ex=65e07900&is=65ce0400&hm=377cfb35301580b3f34005169acd7171cd39f8cf64a3ed4b16961cfd09a5219e&=&format=webp&quality=lossless&width=1202&height=676"
    img_name = Path(urlparse(url).path).name

    async with aiohttp.ClientSession() as session:
        async with session.get(url) as resp:
            buffer = io.BytesIO(await resp.read())
            buffer.seek(0)
            file = discord.File(buffer, filename=img_name)
    await ctx.send(file=file)

@bot.command()
async def lol(ctx, search: str, region: str):
    opgg = OPGG(region=region)

    summoner: Summoner
    for summoner in opgg.search(summoner_names=search, region=region):
        await ctx.send(str(summoner.name))

# Discord bot up
bot.run(os.environ["TOKEN"])
