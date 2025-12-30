import shutil
import discord
from discord.ext import commands
from dotenv import load_dotenv
import tempfile
import os
import re
import subprocess

load_dotenv()
token = os.getenv('DISCORD_TOKEN') or ''

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix=';', intents=intents)

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
    if matches == None:
        matches = re.search(r";grug[\n]+```rs\n(.*)```", message.content, re.DOTALL)
    if matches == None:
        matches = re.search(r";grug[\n]+```py\n(.*)```", message.content, re.DOTALL)

    if matches != None:
        idx = 0
        while True:
            path = os.path.join(
                tempfile.gettempdir(),
                f"grug-eval-context-{idx}"
            )
            if not os.path.exists(path):
                break
            idx += 1
        code = matches.group(1)
        result = subprocess.run(
            ["python3", "grug_eval.py", code, path],
            capture_output=True,
            text=True
        )
        shutil.rmtree(path)
        await message.channel.send(f"{message.author.mention}\n{result.stdout}")

bot.run(token)
