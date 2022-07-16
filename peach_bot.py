import os
import sys
import discord

from dotenv import load_dotenv
from discord.ext import commands

from io import StringIO
from contextlib import redirect_stderr, redirect_stdout

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

bot = commands.Bot(command_prefix='*')
cli = discord.Client()

@bot.event
async def on_ready():
    print(f'{bot.user.name} has connected to Discord!')

lines = ''
last_msg = None

def read_from(path):
    f = open('to_do.txt', 'r')
    return f.read()

def write_to(path, content):
    f = open('to_do.txt', 'a')
    f.write(content)

@bot.command(name='py')
async def execute(ctx, *args):
    global last_msg
    async for message in ctx.history(limit = 1000):
        if '```py\n# ' + args[0] in message.content:
            codeString = message.content.strip('```')
            codeString = codeString.strip('py')
            codeObject = compile(codeString, 'sumstring', 'exec')
            redirected_output = sys.stdout = StringIO()
            exec(codeObject)
            if redirected_output.getvalue() and args[1:]:
                await clear(ctx, '*')
                if last_msg:
                    await last_msg.delete()
                last_msg = await ctx.send(f'> **__todo__**'.upper() + f':\n```{redirected_output.getvalue()}```')
            elif redirected_output.getvalue():
                await ctx.send(f'> **__output__**'.upper() + f':\n```{redirected_output.getvalue()}```')

@bot.command(name='cls')
async def clear(ctx, *args):
    async for message in ctx.history(limit = 1000):
        if not args and not message.content.startswith('```py'):
            await message.delete()
        if args and args[0] == '*' and message.content.startswith('*'):
            await message.delete()
bot.run(TOKEN)