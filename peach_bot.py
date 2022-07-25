import re
import os
import sys
from io import StringIO
import discord

from dotenv import load_dotenv
#from discord.ui import Button, View

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

intents = discord.Intents.all()
client = discord.Client(intents=intents)

lines = []
loops = ('for', 'while')

@client.event
async def on_ready():
    print(f'{client.user.name} has connected to Discord!')

#region Discord
@client.event
async def on_message_edit(before, after):

    msg = after.content
    if msg.startswith('`') and msg.endswith('`'):
        line = msg.strip('`')
        if line.startswith('py'):
            line = line.strip('py')
        if line.startswith(loops):
            pass
        lines.append(line)
        out = sys.stdout = StringIO()
        try:
            exec(line, globals())
        except Exception as err:
            await after.channel.send(f'`{err}`')
        if out.getvalue():
            await after.channel.send(f'`{out.getvalue()}`')


@client.event
async def on_message(message):
    if message.author == client.user:
        return

    msg = message.content
    if msg.startswith('`') and msg.endswith('`'):
        line = msg.strip('`')
        if line.startswith('py'):
            line = line.strip('py')
        if line.startswith(loops):
            pass
        lines.append(line)
        out = sys.stdout = StringIO()
        try:
            exec(line, globals())
        except Exception as err:
            await message.channel.send(f'`{err}`')
        if out.getvalue():
            await message.channel.send(f'`{out.getvalue()}`')
#endregion


#region Tests
# @client.event
# async def on_message(message):
#     if message.author == client.user:
#         return
    
#     button = Button(
#         label='hello',
#         style=discord.ButtonStyle.blurple
#     )

#     async def button_callback(ineraction):
#         await ineraction.response.send_message(button.label)

#     button.callback = button_callback
#     view = View()
#     view.add_item(button)
#     await message.channel.send(view=view)
#endregion

client.run(TOKEN)
