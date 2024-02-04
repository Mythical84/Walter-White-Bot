import os
import random
import threading

from datetime import datetime, timedelta

import discord
from discord.ext import tasks
from discord import app_commands

from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = os.getenv('BOT_TOKEN')

FFMPEG_PATH = os.getenv('FFMPEG_PATH')

intents = discord.Intents.default()
intents.message_content = True
intents.members = True

client = discord.Client(intents=intents)

tree = app_commands.CommandTree(client)

walter_time = datetime.today()
next_walter_decision = datetime.today()

# toggles the random join timer
timer = True

muted_players = []

# Checks if the bot was told to join
toldJoin = False

@client.event
async def on_ready():
    # await tree.sync(guild=discord.Object(id=1141414137826660483))
    print(f'logged in as {client.user}')
    walter_join.start()

@tasks.loop(seconds=15)
async def walter_join():
    if (toldJoin): return
    if timer == False: return
    if not len(client.voice_clients) == 0:
        vc = client.voice_clients[0]
        await vc.disconnect()
    if random.randrange(0,10000) > 0:
        return
    guild = client.get_guild(1141414137826660483)
    members = guild.members
    voice_state = []
    for m in members:
        if not m.voice == None:
            voice_state.append(m)
    chosen: discord.Member = random.choice(voice_state)
    channel = chosen.voice.channel
    await channel.connect()
    vc = client.voice_clients[0]
    vc.play(discord.FFmpegPCMAudio(source='breaking.mp3', executable=FFMPEG_PATH))

@tree.command(name="admin", description="ask aldo for admin", guild=discord.Object(id=1141414137826660483))
async def ask_admin(interaction: discord.Interaction, ping: bool = False):
    if interaction.channel_id != 1141417808744431656:
        await interaction.response.send_message("This command does not work in this channel", ephemeral=True)
        return
    if ping:
        await interaction.response.send_message(f'<@525349767853899776> give {interaction.user.display_name} admin')
    else:
        await interaction.response.send_message(f'Aldo give {interaction.user.display_name} admin')

@tree.command(name="debug", description="debug commands for bot development", guild=discord.Object(id=1141414137826660483))
async def debug(interaction: discord.Interaction, command: str, args: str = ""):
    global toldJoin
    args = args.split(", ")
    if command == "join":
        if args[0] == "":
            interaction.message.author.voice.channel.id
        else:
            c = int(args[0])
        channel = client.get_channel(c)
        toldJoin = True
        await channel.connect()
        await interaction.response.send_message("Joining vc")

    if command == "name":
        await interaction.guild.edit(name=args[0])
        await interaction.response.send_message("changing name")

    if command == "get icon":
       url = interaction.guild.icon.url
       await interaction.response.send_message(url) 

    if command == "set icon":
        with open(f"{args[0]}.png", "rb") as f:
            icon = f.read()
        await interaction.guild.edit(icon=icon)
        await interaction.response.send_message("changing icon")

    if command == "play":
        vc = client.voice_clients[0]
        vc.play(discord.FFmpegPCMAudio(source=f'./{args[0]}.mp3', executable=FFMPEG_PATH))
        await interaction.response.send_message(f"playing {args[0]}")

    if command == "pause":
        vc = client.voice_clients[0]
        vc.pause()
        await interaction.response.send_message("pausing")

    if command == "disconnect":
        vc = client.voice_clients[0]
        toldJoin = False
        await vc.disconnect()
        await interaction.response.send_message("leaving")

    if command == "create channels":
        guild = interaction.guild
        category = await guild.create_category("test")
        await guild.create_voice_channel("test-voice", category=category)
        text = await guild.create_text_channel("test-text", category=category)
        await text.send("Hello guys i am walter white")

    if command == "list channels":
        guild = client
        for channel in guild.channels:
            print(channel.name, channel.type)

    if command == "toggle":
        global timer
        if timer == True:
            timer = False
        else:
            timer = True

    if command == "mute":
        if len(args) < 1: return
        if args[0] == 547588299552718848: return
        guild = client.get_guild(1141414137826660483)
        player = guild.get_member(int(args[0]))
        add_role = discord.utils.get(guild.roles, id=1185598499555913788)
        remove_role = discord.utils.get(guild.roles,id=1141416281669644319)
        await player.remove_roles(remove_role)
        await player.add_roles(add_role)
        await player.edit(mute=True)
        await interaction.response.send_message("Player muted")

    if command == "unmute":
        if len(args) < 1: return
        guild = client.get_guild(1141414137826660483)
        player = guild.get_member(int(args[0]))
        remove_role = discord.utils.get(guild.roles, id=1185598499555913788)
        add_role = discord.utils.get(guild.roles,id=1141416281669644319)
        await player.add_roles(add_role)
        await player.remove_roles(remove_role)
        await player.edit(mute=False)
        await interaction.response.send_message("Player unmuted")

    if command == "admin":
        if len(args) < 1: return
        guild = client.get_guild(1141414137826660483)
        player = guild.get_member(int(args[0]))
        role = discord.utils.get(guild.roles, id=1141416281669644319)
        await player.add_roles(role)
        await interaction.response.send_message("Admin granted")

@client.event
async def on_voice_state_update(member, before, after):
    global toldJoin
    if after.channel is None and member==client.user:
        toldJoin = False

client.run(BOT_TOKEN)