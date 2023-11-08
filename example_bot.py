# This example requires the 'message_content' intent.

import discord
import json
import asyncio
import time
from datetime import datetime

f = open('enviro.json')
token = json.load(f)['BOT_TOKEN']

intents = discord.Intents.default()
intents.message_content = True

client = discord.Client(intents=intents)

@client.event
async def on_ready():
    print(f'We have logged in as {client.user}')
    channel = client.get_channel(1169885828265279508)
    await channel.send(f'Logged in as Bot! Time is {datetime.now()}')

last_message = 0
@client.event
async def on_message(message):
    if message.author == client.user:
        return

    global last_message

    if message.content.startswith('$hello'):
        await message.channel.send('Hello!')

    elif message.content.startswith('$typing'):
        channel = client.get_channel(1169885828265279508)
        await channel.typing()
        await asyncio.sleep(3)
        await channel.send('Done typing!')

    else :
        message_to_send = 'You said: "' + message.content + '"'
        await message.channel.send(message_to_send)
        if last_message == 0:
            await message.channel.send('this is the first message!')
        else :
            await message.channel.send(f'time since last message: {time.time() - last_message} seconds')
        last_message = time.time()

@client.event
async def on_typing(channel, user, when):
    # time_elapsed = time.time()-last_message
    await channel.send(f'{user} is typing.')
    # last_message = time.time()


client.run(token)
