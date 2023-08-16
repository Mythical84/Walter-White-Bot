import os

import discord
from discord.ext import tasks
from discord import app_commands

from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = os.getenv('BOT_TOKEN')

intents = discord.Intents.all()
intents.message_content = True

client = discord.Client(intents=intents)

tree = app_commands.CommandTree(client)

@client.event
async def on_ready() :
    print(f'logged in as {client.user}')
    await tree.sync(guild=discord.Object(id=1141414137826660483))
    # admin.start()

@tasks.loop(seconds=600)
async def admin():
    channel = client.get_channel(1141417808744431656)
    await channel.send('Aldo give me admin')

@admin.before_loop
async def before_admin():
    await client.wait_until_ready()

@tree.command(name="admin", description="ask aldo for admin", guild=discord.Object(id=1141414137826660483))
async def ask_admin(interaction: discord.Interaction, ping: bool = False):
    if ping:
        await interaction.response.send_message(f'<@525349767853899776> give <@{interaction.user.id} admin')
    else:
        await interaction.response.send_message(f'Aldo give <@{interaction.user.id}> admin')

client.run(BOT_TOKEN)
