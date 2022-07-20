import os
import sys
from textwrap import indent
import discord

from dotenv import load_dotenv
from discord.ext import commands

from io import StringIO
from contextlib import redirect_stderr, redirect_stdout

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

client = discord.Client()

lines = ''
indent_mode = False

@client.event
async def on_ready():
    print(f'{client.user.name} has connected to Discord!')

@client.event
async def on_message(message):
    global lines
    global indent_mode
    if message.author == client.user:
        return

    if 'q' in message.content:
        await message.delete()
        redirected_output = sys.stdout = StringIO()
        try:
            exec(lines, globals())
        except Exception as err:
            await message.channel.send(f'`{err}`')
        if redirected_output.getvalue():
            await message.channel.send(f'`{redirected_output.getvalue()}`')
        
        indent_mode = False

    message_start = message.content.startswith('`')
    message_end = message.content.endswith('`') 

    if message_start and message_end:
        line = message.content.strip('`')
        if not indent_mode:
            lines = line + '\n'
        redirected_output = sys.stdout = StringIO()

        if line.endswith(':'):
            indent_mode = True
            return

        if indent_mode:
            lines += line + '\n'
            return

        try:
            exec(lines, globals())
        except Exception as err:
            await message.channel.send(f'`{err}`')
        if redirected_output.getvalue():
            await message.channel.send(f'`{redirected_output.getvalue()}`')

client.run(TOKEN)