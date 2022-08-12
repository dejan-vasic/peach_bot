import os
import sys
from io import StringIO
import json
import asyncio
import discord
import googletrans

from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

intents = discord.Intents.all()
client = discord.Client(intents=intents)

setBotJsonFile = open('set_bot.json', 'r+')
setBotData = json.load(setBotJsonFile)

class set_bot:
    class channels_list(list):
        def append(self, __object) -> None:
            if not __object in setBotData["channels"]:
                setBotData["channels"].append(__object)
            setBotJsonFile.seek(0)
            json.dump(setBotData, setBotJsonFile)
            setBotJsonFile.truncate()
            return super().append(__object)

        def remove(self, __value) -> None:
            setBotData["channels"].remove(__value)
            setBotJsonFile.seek(0)
            json.dump(setBotData, setBotJsonFile)
            setBotJsonFile.truncate()
            return super().remove(__value)
    channels = channels_list()
    class modes:
        exe = True
        quiz = False
        lang = False

msg = None
channel = None

async def exe(code):
    global msg
    out = sys.stdout = StringIO()
    try:
        eval_code = eval(code, globals())
        if eval_code != None: print(eval_code)
    except:
        try:
            exec(code, globals())
        except Exception as err:
            await channel.send(f'`{err}`')
    if out.getvalue():
        await channel.send(f'`{out.getvalue()}`')

async def cls():
    msg_hst = await channel.history(limit=1000).flatten()
    for msg in msg_hst:
        if msg.content == 'cls' or msg.author == client.user:
            await msg.delete()

async def timer(t):
    msg = None
    for dt in range(0, t):
        if msg:
            await msg.delete()
        msg = await channel.send(dt)
        asyncio.sleep(1)

@client.event
async def on_ready():
    global channel
    await client.wait_until_ready()
    for channel_id in setBotData['channels']:
        set_bot.channels.append(channel_id)
    print(f'{client.user.name} has connected to Discord!')

@client.event
async def on_message(message):
    global channel
    if message.author == client.user:
        return

    msg_cont = message.content

    if msg_cont.startswith('set_bot') and message.author.name == 'dejan.vasic':
        args = msg_cont.split(' ')[1:]
        if args[0] == 'channel':
            if args[1] == 'on':
                set_bot.channels.append(message.channel.id)
            elif args[1] == 'off':
                channel = None
                set_bot.channels.remove(message.channel.id)
    
    if not message.channel.id in set_bot.channels:
        return
    elif message.channel.id in set_bot.channels:
        channel = message.channel

    if set_bot.modes.exe:

        if msg_cont == 'timer':
            await timer(5)

        if msg_cont == 'cls':
            await cls()
            pass

        if msg_cont.startswith('`') and msg_cont.endswith('`'):
            code = msg_cont.strip('`')
            if code.startswith('py'):
                code = code.strip('py')
            await exe(code)

    if set_bot.modes.quiz:
        pass

    if set_bot.modes.lang:
        pass
                
@client.event
async def on_raw_message_edit(payload):
    global channel
    
    message = payload.cached_message

    if not message:
        channel = client.get_channel(payload.channel_id)
        message = await channel.fetch_message(payload.message_id)

    if message.author == client.user:
        return

    msg_cont = message.content

    if not message.channel.id in set_bot.channels:
        return
    elif message.channel.id in set_bot.channels:
        channel = message.channel

    if set_bot.modes.exe:
        if msg_cont.startswith('`') and msg_cont.endswith('`'):
            code = msg_cont.strip('`')
            if code.startswith('py'):
                code = code.strip('py')
            await exe(code)

client.run(TOKEN)
