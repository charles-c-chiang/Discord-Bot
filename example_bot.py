# This example requires the 'message_content' intent.

import discord
import json
import asyncio
import time
from datetime import datetime
from discord.ext import tasks, commands
from openai import AsyncAzureOpenAI

f = open('auth.json')
token = json.load(f)['BOT_TOKEN']
f = open('auth.json')
OPENAI_API_KEY = json.load(f)['OPENAI_API_KEY']

intents = discord.Intents.default()
intents.message_content = True

client = discord.Client(intents=intents)

AIclient = AsyncAzureOpenAI(api_key = OPENAI_API_KEY,
api_version = "2023-07-01-preview", 
azure_endpoint="https://charlietest.openai.azure.com/openai/deployments/charlieTestModel/chat/completions?api-version=2023-07-01-preview")
message_text = [{"role":"system","content":"You are StrangerBot, an introduction chatbot. Your job is to interact with two different strangers, and help them get to know each other better. You can do this by recommending them topics to talk about or asking them to share more about themselves. You should start each conversation by introducing yourself, then by asking both people their name and some basic facts about them. You should not have overly lengthy or detailed responses, as the focus of the conversation should be between the two strangers and you want to keep a friendly, casual tone. "}]

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

    """AI STUFF HERE"""
    completion = await AIclient.chat.completions.create(
        model="deployment-name",  # e.g. gpt-35-instant
        messages=[
            {"role": "user", "content": message.content,},
        ],
    )
    print(completion.choices[0].message.content)
    await message.channel.send(completion.choices[0].message.content)
    """END AI STUFF"""

    # if message.content.startswith('$hello'):
    #     await message.channel.send('Hello!')

    # elif message.content.startswith('$typing'):
    #     channel = client.get_channel(1169885828265279508)
    #     await channel.typing()
    #     await asyncio.sleep(3)
    #     await channel.send('Done typing!')

    # else :
    #     message_to_send = 'You said: "' + message.content + '"'
    #     await message.channel.send(message_to_send)
    #     if last_message == 0:
    #         await message.channel.send('this is the first message!')
    #     else :
    #         await message.channel.send(f'time since last message: {time.time() - last_message} seconds')
    #     last_message = time.time()

# @client.event
# async def on_typing(channel, user, when):
#     # time_elapsed = time.time()-last_message
#     await channel.send(f'{user} is typing.')
#     # last_message = time.time()



client.run(token)
