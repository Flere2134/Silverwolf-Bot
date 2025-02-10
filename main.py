import discord
from discord.ext import commands
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import asyncio

scope = ["https://www.googleapis.com/auth/spreadsheets"]
creds = ServiceAccountCredentials.from_json_keyfile_name('C:/Users/aaron/Desktop/Aaron/SW Bot credentials/silverwolf-bot-acc2.json', scopes=scope)
client = gspread.authorize(creds)

sheetid = "1hjXI9lh6im_kkRmvSJ-FO7Ucp5sKcJEZCCRvoxz2Ix8"
sheet = client.open_by_key(sheetid).sheet1

bot = commands.Bot(command_prefix="sw!", intents=discord.Intents.all())

@bot.event
async def on_ready():
    print("Silverwolf ready!")

@bot.command()
async def char(ctx, name):
    records = sheet.get_all_records()
    matched_record = None

    for record in records:
        if record['Name'].lower().startswith(name.lower()):
            matched_record = record
            break
    if matched_record:
        rarity = matched_record['Rarity']
        path = matched_record['Path']
        element = matched_record['Element']
        speed = matched_record['Base Speed']
        energy = matched_record['Max Energy']
        image = matched_record['Art']
        basic_atk = matched_record['Basic ATK']
        skill = matched_record['Skill']
        ult = matched_record['Ultimate']
        talent = matched_record['Talent']
        technique = matched_record['Technique']
        trace1 = matched_record['Trace 1']
        trace2 = matched_record['Trace 2']
        trace3 = matched_record['Trace 3']
        stat_bonus = matched_record['Stat Bonus']
        eidolon1 = matched_record['Eidolon 1']
        eidolon2 = matched_record['Eidolon 2']
        eidolon3 = matched_record['Eidolon 3']
        eidolon4 = matched_record['Eidolon 4']
        eidolon5 = matched_record['Eidolon 5']
        eidolon6 = matched_record['Eidolon 6']
        memospriteskill = matched_record['Memosprite Skill']
        memospritetalent = matched_record['Memosprite Talent']

        embed1 = discord.Embed(
            title=matched_record['Name'].upper(),
            color=discord.Color.random()
        )
        path_emotes = {
            "Preservation": "<:preservation:1338545325895323651>",
            "Nihility": "<:nihility:1338551372198576198>",
            "Harmony": "<:harmony:1338551463491801160>",
            "Abundance": "<:abundance:1338551252598128690>",
            "Erudition": "<:erudition:1338551296214700093>",
            "The Hunt": "<:thehunt:1338551280720674919>",
            "Destruction": "<:destruction:1338551338149089331>",
            "Remembrance": "<:remembrance:1338551266497925160>",
        }
        element_emotes ={
            "Fire": "<:fire:1338557624072933467>",
            "Wind": "<:wind:1338557764368339116>",
            "Ice": "<:ice:1338557786208079914>",
            "Lightning": "<:lightning:1338557796186193981>",
            "Physical": "<:physical:1338558004135727195>",
            "Quantum": "<:quantum:1338557834308223047>",
            "Imaginary": "<:imaginary:1338557804897636392>",
        }
        emote1 = path_emotes.get(path, "")
        emote2 = element_emotes.get(element, "")
        embed1.add_field(name="Rarity", value=rarity, inline=True)
        embed1.add_field(name="Path", value=f"{path}{emote1}", inline=True)
        embed1.add_field(name="Element", value=f"{element}{emote2}", inline=True)
        embed1.add_field(name="Base Speed", value=speed, inline=True)
        embed1.add_field(name="Max Energy", value=energy, inline=True)
        embed1.add_field(name="Basic ATK", value=basic_atk, inline=False)
        embed1.add_field(name="Skill", value=skill, inline=False)
        embed1.add_field(name="Ultimate", value=ult, inline=False)
        embed1.set_image(url=image)

        embed2 = discord.Embed(
            title=matched_record['Name'].upper(),
            color=discord.Color.random()
        )
        embed2.add_field(name="Talent", value=talent, inline=False)
        embed2.add_field(name="Technique", value=technique, inline=False)
        embed2.add_field(name="Trace 1", value=trace1, inline=False)
        embed2.add_field(name="Trace 2", value=trace2, inline=False)
        embed2.add_field(name="Trace 3", value=trace3, inline=False)
        embed2.add_field(name="Trace Stat Bonus", value=stat_bonus, inline=False)
        embed2.set_image(url=image)

        embed3 = discord.Embed(
            title=matched_record['Name'].upper(),
            color=discord.Color.random()
        )
        embed3.add_field(name="Eidolon 1", value=eidolon1, inline=False)
        embed3.add_field(name="Eidolon 2", value=eidolon2, inline=False)
        embed3.add_field(name="Eidolon 3", value=eidolon3, inline=False)
        embed3.add_field(name="Eidolon 4", value=eidolon4, inline=False)
        embed3.add_field(name="Eidolon 5", value=eidolon5, inline=False)
        embed3.add_field(name="Eidolon 6", value=eidolon6, inline=False)
        embed3.set_image(url=image)

        embeds = [embed1, embed2, embed3]

        if memospriteskill.strip() and memospritetalent.strip():
            embed4 = discord.Embed(
            title=matched_record['Name'].upper(),
            color=discord.Color.random()
            )
            embed4.add_field(name="Memosprite Skill", value=memospriteskill, inline=False)
            embed4.add_field(name="Memosprite Talent", value=memospritetalent, inline=False)
            embed4.set_image(url=image)

            embeds.append(embed4)

        message = await ctx.send(embed=embeds[0])

        await message.add_reaction("◀️")
        await message.add_reaction("▶️")

        def check(reaction, user):
            return user == ctx.author and str(reaction.emoji) in ["◀️", "▶️"] and reaction.message.id == message.id
            
        current_page = 0
        while True:
            try:
                reaction, user = await bot.wait_for("reaction_add", timeout=60.0, check=check)
                if str(reaction.emoji) == "▶️":
                    current_page += 1
                    if current_page >= len(embeds):
                        current_page = 0
                elif str(reaction.emoji) == "◀️":
                    current_page -= 1
                    if current_page < 0:
                        current_page = len(embeds) - 1

                await message.edit(embed=embeds[current_page])
                await message.remove_reaction(reaction, user)

            except asyncio.TimeoutError:
                break

        await message.clear_reactions()

    else:
        await ctx.send("Character not found!")

with open("C:/Users/aaron/Desktop/Aaron/SW Bot credentials/token.txt") as file:
    token = file.read()

bot.run(token) #run bot