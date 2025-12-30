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

def try_match_req(content: str) -> re.Match[str] | None:
    matches = re.search(r";grug[\n]+```grug\n(.*)```", content, re.DOTALL)
    if matches == None:
        matches = re.search(r";grug[\n]+```rs\n(.*)```", content, re.DOTALL)
    if matches == None:
        matches = re.search(r";grug[\n]+```py\n(.*)```", content, re.DOTALL)
    return matches

def grug_eval(code: str) -> str:
    idx = 0
    while True:
        path = os.path.join(
            tempfile.gettempdir(),
            f"grug-eval-context-{idx}"
        )
        if not os.path.exists(path):
            break
        idx += 1
    result = subprocess.run(
        ["python3", "grug_eval.py", code, path],
        capture_output=True,
        text=True
    ).stdout
    result = f"```\n{result}```"
    shutil.rmtree(path)
    return result

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

    matches = try_match_req(message.content)

    if matches != None:
        result = grug_eval(matches.group(1))
        await message.reply(result)


@bot.event
async def on_message_edit(before: discord.Message, after: discord.Message):
    if before.content == after.content:
        return
    previous_reply: discord.Message | None = None
    async for msg in before.channel.history(limit=32):
        if msg.reference and msg.reference.message_id == before.id and msg.author == bot.user:
            previous_reply = msg

    if previous_reply is None:
        return
    match = try_match_req(after.content)
    if match is None:
        return

    code = match.group(1)
    result = grug_eval(code)
    await previous_reply.edit(content=result)

bot.run(token)
