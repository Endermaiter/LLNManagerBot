#!/usr/bin/env python3.10
import ast
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

# Discord bot preconfiguration
bot = commands.Bot(command_prefix="!", intents=discord.Intents.all())


# Check discord bot is up and running
@bot.event
async def on_ready():
    print(f"Conectado como: {bot.user}")


@bot.command()
async def helpLLN(ctx):
    embed = discord.Embed(title="Guia de comandos de LLN", description="")
    embed.add_field(name="`!participantes`", value="Muestra la lista de todos los participantes del torneo.",
                    inline=False)
    embed.add_field(name="`!equipos`",
                    value="Muestra la imagen oficial de todos los equipos que conforman el torneo, asi como sus respectivos capitanes.",
                    inline=False)
    embed.add_field(name="`!lol invocador hastag region`",
                    value="Muestra algunas estadisticas del jugador y proporciona el enlace a su **op.gg**\n"
                          "- `invocador`: \n"
                          "   Nombre de invocador del jugador. Si el nombre que deseas introducir tiene espacios, por favor, añade '-' para separar las palabras. \n"
                          "   (Ej: Nombre -> ABC DEF -> ABC-DEF)\n"
                          "- `hastag`: \n"
                          "   Hastag del jugador. Debe contener el '#' al principio del mismo, seguido de 3/4 caracteres (Ej: #ABCD)\n"
                          "- `region`: \n"
                          "   Region donde la cuenta del jugador esté registrada. Posibles opciones:\n"
                          " - NA, EUW, BR, JP, KR, EUNE, LAN, LAS, OC, RU, TR", inline=False)
    embed.add_field(name="`!redes`", value="Muestra las redes oficiales de LLN", inline=False)
    embed.add_field(name="`!otaku`", value="Boca chango, simplemente", inline=False)
    embed.set_thumbnail(
        url="https://cdn.discordapp.com/attachments/844311976888893440/1204121772966944819/Imagen_de_WhatsApp_2023-11-10_a_las_10.png?ex=65dccf4a&is=65ca5a4a&hm=c3e6aebfdf01fabe2a9211301e9401456bd8a56b7337a7949f8b5cf7bcd86318&")
    await ctx.send(embed=embed)


@bot.command()
async def redes(ctx):
    embed = discord.Embed(title="Redes Sociales de LLN", description="")
    embed.add_field(name="Instagram", value="- 📷 | [@la_liga_del_norte](https://www.instagram.com/la_liga_del_norte/)",
                    inline=False)
    embed.add_field(name="Twitter", value="- ‎ ‎𝕏 ‎ | [@la_liga_del_norte](https://twitter.com/liga_del_norte)",
                    inline=False)
    embed.add_field(name="Twitch", value="- 🔴 | [@laligadelnorte](https://www.twitch.tv/laligadelnorte)", inline=False)
    embed.set_thumbnail(
        url="https://cdn.discordapp.com/attachments/844311976888893440/1204121772966944819/Imagen_de_WhatsApp_2023-11-10_a_las_10.png?ex=65dccf4a&is=65ca5a4a&hm=c3e6aebfdf01fabe2a9211301e9401456bd8a56b7337a7949f8b5cf7bcd86318&")
    embed.set_image(
        url="https://socialblade.com/blog/wp-content/uploads/2017/07/social-blade-adds-twitter-instagram-twitch.jpg")
    await ctx.send(embed=embed)


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
              "**Posición**\n¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯\n")
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
async def otaku(ctx):
    url = "https://cdn.discordapp.com/attachments/1027500125670604843/1208458086495420507/SaveTube.App-Caballo_habla_como_mona_china_entrevista-1080p60.mp4?ex=65e35b4b&is=65d0e64b&hm=6fff917e323357dfb07b83e3084b4d8fd73ab6b952774dcb1ecd7b61e0cf0d06&"
    img_name = Path(urlparse(url).path).name

    async with aiohttp.ClientSession() as session:
        async with session.get(url) as resp:
            buffer = io.BytesIO(await resp.read())
            buffer.seek(0)
            file = discord.File(buffer, filename=img_name)
    await ctx.send(file=file)


@bot.command()
async def lol(ctx, search: str, hastag: str, region: str):
    try:
        opgg = OPGG(region=region)
        checkHastag = True
        searchEdited = search.replace("-", " ")
        if hastag.__contains__("#"):
            hastag = hastag.replace("#", "")
        else:
            checkHastag = False
            await ctx.send("El hastag debe contener '#' al principcio")

        if opgg.cached_page_props:
            page_props = opgg.cached_page_props
        else:
            page_props = opgg.get_page_props(searchEdited, region)
            opgg.cached_page_props = page_props

        opgg.get_all_seasons(region, page_props)
        opgg.get_all_champions(region, page_props)
        summoner = Summoner
        for id in page_props['summoners']:
            opgg.summoner_id = id["summoner_id"]
            summoner = opgg.get_summoner()

        summoner_name = summoner.level
        profile_image = summoner.profile_image_url
        summoner_level = summoner.level
        stats = summoner.league_stats
        seasons = summoner.previous_seasons
        recentGames = summoner.recent_game_stats
        # Last updated timestamp
        updatedWithoutFormat = summoner.updated_at
        date = datetime.datetime.fromisoformat(str(updatedWithoutFormat))
        updateTimeStamp = date.strftime("%d/%m/%Y %H:%M:%S")
        # Indexando la lista de stats
        statsIndexed = stats[:3]
        eloTier = [league_stats.tier_info.tier for league_stats in statsIndexed]
        eloDivision = [league_stats.tier_info.division for league_stats in statsIndexed]
        eloLPs = [league_stats.tier_info.lp for league_stats in statsIndexed]
        win = [league_stats.win for league_stats in statsIndexed]
        lose = [league_stats.lose for league_stats in statsIndexed]
        # Indexando la lista de games
        gamesIndexed = recentGames[:10]
        kills = [game_stats.kill for game_stats in gamesIndexed]
        deaths = [game_stats.death for game_stats in gamesIndexed]
        assists = [game_stats.assist for game_stats in gamesIndexed]
        positions = [game_stats.position for game_stats in gamesIndexed]
        is_win = [game_stats.is_win for game_stats in gamesIndexed]
        # Indexando la lista de games
        seasonsIndexed = seasons[:10]
        seasonTier = [season_stats.tier_info.tier for season_stats in seasonsIndexed]
        seasonDivision = [season_stats.tier_info.division for season_stats in seasonsIndexed]
        seasonLPs = [season_stats.tier_info.lp for season_stats in seasonsIndexed]

        gamesRankedSolo = 0
        gamesRankedFlex = 0
        winRateSolo = 0
        winRateFlex = 0
        if summoner_name == "":
            await ctx.send("El jugador no existe, intentalo de nuevo")
        elif checkHastag:
            if search.__contains__("-"):
                urlSearch = search.replace("-", "%20")
            else:
                urlSearch = search
            urlOPGG = f"https://www.op.gg/summoners/{region.lower()}/{urlSearch}-{hastag}"
            if win[0] is None and lose[0] is not None:
                win[0] = 0
                gamesRankedSolo = win[0] + lose[0]
                gamesRankedFlex = win[1] + lose[1]
                winRateSolo = (win[0] / gamesRankedSolo) * 100
                winRateFlex = (win[1] / gamesRankedFlex) * 100
            elif win[0] is not None and lose[0] is None:
                lose[0] = 0
                gamesRankedSolo = win[0] + lose[0]
                gamesRankedFlex = win[1] + lose[1]
                winRateSolo = (win[0] / gamesRankedSolo) * 100
                winRateFlex = (win[1] / gamesRankedFlex) * 100
            elif win[0] is None and lose[0] is None:
                win[0] = 0
                lose[0] = 0
                gamesRankedSolo = win[0] + lose[0]
                gamesRankedFlex = win[1] + lose[1]
                winRateSolo = 0
                winRateFlex = (win[1] / gamesRankedFlex) * 100
            elif win[1] is None and lose[1] is not None:
                win[1] = 0
                gamesRankedSolo = win[0] + lose[0]
                gamesRankedFlex = win[1] + lose[1]
                winRateSolo = (win[0] / gamesRankedSolo) * 100
                winRateFlex = (win[1] / gamesRankedFlex) * 100
            elif win[1] is not None and lose[1] is None:
                lose[1] = 0
                gamesRankedSolo = win[0] + lose[0]
                gamesRankedFlex = win[1] + lose[1]
                winRateSolo = (win[0] / gamesRankedSolo) * 100
                winRateFlex = (win[1] / gamesRankedFlex) * 100
            elif win[1] is None and lose[1] is None:
                win[1] = 0
                lose[1] = 0
                gamesRankedSolo = win[0] + lose[0]
                gamesRankedFlex = win[1] + lose[1]
                winRateSolo = (win[0] / gamesRankedSolo) * 100
                winRateFlex = 0
            elif win[0] is None and lose[0] is None and win[0] is None and lose[0] is None:
                win[0] = 0
                lose[0] = 0
                win[1] = 0
                lose[1] = 0
                gamesRankedSolo = win[0] + lose[0]
                gamesRankedFlex = win[1] + lose[1]
                winRateSolo = 0
                winRateFlex = 0

            separation = "‎‎ ‎ ‎ ‎ ‎ ‎‎‎ ‎ ‎ ‎ ‎ ‎‎‎ ‎ ‎ ‎ ‎ ‎‎‎ ‎‎ ‎‎"
            embed = discord.Embed(title=search.replace("-", " ") + " #" + hastag,
                                  url=urlOPGG,
                                  description="> Nivel: " + str(summoner_level))
            embed.add_field(name="\n‎", value="\n‎", inline=False)
            if eloTier[0] is None or eloDivision[0] is None or eloLPs[0] is None:
                embed.add_field(name="Ranked Solo/Duo" + separation + separation,
                                value="`UNRANKED`\n" +
                                      str(gamesRankedSolo) + "G " + str(win[0]) + "W " + str(
                                    lose[0]) + "L ║ WR -> " + str(
                                    round(winRateSolo, 2)) + "% ", inline=True)
            else:
                embed.add_field(name="Ranked Solo/Duo" + separation + separation,
                                value="`" + str(eloTier[0]) + " " + str(eloDivision[0]) + "` - **" + str(
                                    eloLPs[0]) + "** LPs\n" +
                                      str(gamesRankedSolo) + "G " + str(win[0]) + "W " + str(
                                    lose[0]) + "L ║ WR -> " + str(
                                    round(winRateSolo, 2)) + "% ", inline=True)
            if eloTier[1] is None or eloDivision[1] is None or eloLPs[1] is None:
                embed.add_field(name="Ranked Flex",
                                value="`UNRANKED`\n" +
                                      str(gamesRankedFlex) + "G " + str(win[0]) + "W " + str(
                                    lose[0]) + "L ║ WR -> " + str(
                                    round(winRateFlex, 2)) + "% ", inline=True)
            else:
                embed.add_field(name="Ranked Flex",
                                value="`" + str(eloTier[1]) + " " + str(eloDivision[1]) + "` - **" + str(
                                    eloLPs[1]) + "** LPs\n" +
                                      str(gamesRankedFlex) + "G " + str(win[1]) + "W " + str(
                                    lose[1]) + "L ║ WR -> " + str(
                                    round(winRateFlex, 2)) + "% ", inline=True)
            embed.add_field(name="\n‎", value="", inline=False)
            embed.add_field(name="Historial de partida (Solo/Duo)", value="Ultimas 10 partidas", inline=True)

            contadorVictorias = 0
            contadorDerrotas = 0
            for i in range(0, len(gamesIndexed)):
                if is_win[i]:
                    embed.add_field(name="",
                                    value="🔵 | `" + str(kills[i]) + "/" + str(deaths[i]) + "/" + str(
                                        assists[i]) + "` - " + str(positions[i]),
                                    inline=False)
                    contadorVictorias = contadorVictorias + 1
                else:
                    embed.add_field(name="",
                                    value="🔴 | `" + str(kills[i]) + "/" + str(deaths[i]) + "/" + str(
                                        assists[i]) + "` - " + str(positions[i]),
                                    inline=False)
                    contadorDerrotas = contadorDerrotas + 1
            contadorPartidas = contadorVictorias + contadorDerrotas
            embed.add_field(name="Resumen: " + str(contadorPartidas) + "G " + str(contadorVictorias) + "W " + str(
                contadorDerrotas) + "L",
                            value="", inline=False)
            embed.add_field(name="\n‎", value="", inline=False)
            embed.add_field(name="Ultimas seasons (Solo/Duo)", value="", inline=False)
            contadorSeasons = 13
            for i in range(0, len(seasonsIndexed)):
                embed.add_field(name="", value="Season: " + str(contadorSeasons) +
                                               " - `" + str(seasonTier[i]) + " " + str(seasonDivision[i]) +
                                               "` | **" + str(seasonLPs[i]) + "** LPs", inline=False)
                contadorSeasons = contadorSeasons - 1
            embed.set_thumbnail(url=profile_image)
            embed.set_footer(text="Última actualización de datos: " + updateTimeStamp)
            await ctx.send(embed=embed)

    except Exception as e:
        await ctx.send(f"No se ha encontrado al jugador, vuelve a intentarlo"
                       f"\nPython debugging (Beta): {e}")


# Discord bot up
bot.run(os.environ["TOKEN_TEST"])
