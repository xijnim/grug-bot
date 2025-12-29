import discord
from discord.ext import commands
from dotenv import load_dotenv
import os
import re
import subprocess

load_dotenv()
token = os.getenv('DISCORD_TOKEN') or ''

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix=';', intents=intents)

secret_role = "Gamer"

@bot.event
async def on_ready():
    print(f"We are ready to go in, {bot.user.name}")

@bot.event
async def on_member_join(member):
    await member.send(f"Welcome to the server {member.name}")

@bot.event
async def on_message(message: discord.Message):
    if message.author == bot.user:
        return

    matches = re.search(r";grug[\n]+```grug\n(.*)```", message.content, re.DOTALL)
    if matches != None:
        code = matches.group(1)
        result = subprocess.run(
            ["python3", "grug_eval.py", code],
            capture_output=True,
            text=True
        )
        await message.channel.send(f"{message.author.mention}\n{result.stdout}")

bot.run(token)
