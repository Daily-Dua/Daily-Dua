import os
import logging
import discord
from discord.ext import commands, tasks
from discord import Embed
from datetime import datetime, timedelta
import random
import database  # Import the database module

# Initialize the database
database.init_db()

# Setup logging
logging.basicConfig(level=logging.INFO)

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix='/', intents=intents)

# Function to read Duas from text file and add them to the database
def read_duas_from_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        lines = file.readlines()

    duas = []
    current_dua = {}
    for line in lines:
        line = line.strip()
        if line:
            if 'Arabic Text' in line:
                current_dua['text'] = lines[lines.index(line) + 1].strip()
            elif 'Translation' in line:
                current_dua['translation'] = lines[lines.index(line) + 1].strip()
            else:
                current_dua['name'] = line
        else:
            if current_dua:
                duas.append(current_dua.copy())
                current_dua.clear()

    return duas

# Path to the text file with Duas
duas_file_path = 'duas.txt'

# Read Duas from file
duas = read_duas_from_file(duas_file_path)

# Add Duas to the database
for dua in duas:
    database.add_dua(dua['name'], dua['text'], dua['translation'])

@bot.event
async def on_ready():
    logging.info(f'We have logged in as {bot.user}')
    send_daily_dua.start()  # Start the daily Dua task

@tasks.loop(hours=24)
async def send_daily_dua():
    # Get the channel ID from the database
    channel_id = database.get_config('channel_id')
    if not channel_id:
        logging.error("Channel ID not set.")
        return

    channel = bot.get_channel(int(channel_id))
    if not channel:
        logging.error("Channel not found.")
        return

    # Get a random Dua from the database
    dua = database.get_random_dua()
    if not dua:
        logging.error("No Duas found in the database.")
        return

    name, text, translation = dua

    # Create an embedded message with Markdown
    embed = Embed(title=f"**{name}**", description=f"**Arabic:**\n{text}\n\n**Translation:**\n{translation}", color=0x00ff00)
    embed.set_footer(text="Islamic Daily Dua Bot")

    # Send the embedded message
    await channel.send(embed=embed)

@send_daily_dua.before_loop
async def before():
    await bot.wait_until_ready()
    now = datetime.utcnow()
    target_time = now.replace(hour=0, minute=0, second=0, microsecond=0) + timedelta(days=1)
    seconds_until_target = (target_time - now).total_seconds()
    await discord.utils.sleep_until(target_time)
    send_daily_dua.change_interval(hours=24, seconds=seconds_until_target)

@bot.command(name='setchannel')
@commands.has_permissions(administrator=True)
async def set_channel(ctx, channel_id: int):
    database.set_config('channel_id', str(channel_id))
    await ctx.send(f"Channel ID set to {channel_id}")

@bot.command(name='listduas')
async def list_duas(ctx):
    duas = database.get_duas()
    if not duas:
        await ctx.send("No Duas found.")
        return
    message = "\n".join([f"{dua[0]}: {dua[1]}" for dua in duas])
    await ctx.send(f"Duas:\n{message}")

try:
    token = os.getenv("MTI1NjAwNTYwMjQ5NzI2NTc3OA.GsPD9y.B8MHZmuC8im3z2T2IanK75-nQfSjPKBwJ3Q_EI")
    if not token:
        raise ValueError("No token found. Please add your token to the environment variables.")
    bot.run(token)
except discord.HTTPException as e:
    if e.status == 429:
        logging.error("The Discord servers denied the connection for making too many requests")
        logging.error("Get help from https://stackoverflow.com/questions/66724687/in-discord-py-how-to-solve-the-error-for-toomanyrequests")
    else:
        raise e
except ValueError as e:
    logging.error(e)
