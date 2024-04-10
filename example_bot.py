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
api_version = "2024-02-01", 
azure_endpoint="https://charlietest.openai.azure.com/openai/deployments/charlieTestModel/chat/completions?api-version=2024-02-01")
message_text = [{"role":"system","content":"You are StrangerBot, an introduction chatbot. Your job is to interact with two different strangers, and help them get to know each other better. You can do this by recommending them topics to talk about or asking them to share more about themselves. You should start each conversation by introducing yourself, then by asking both people their name and some basic facts about them. You should not have overly lengthy or detailed responses, as the focus of the conversation should be between the two strangers and you want to keep a friendly, casual tone."}]

@client.event
async def on_ready():
    print(f'We have logged in as {client.user}')
    channel = client.get_channel(1169885828265279508)
    await channel.send(f'Logged in as Bot! Time is {datetime.now()}')

last_message = 0
message_times = {}
typing_times = {}

#gets message from openai
async def get_message(channel):
        # send conversation to aclient, await response
        completion = await AIclient.chat.completions.create(
            model="deployment-name",  # e.g. gpt-35-instant
            messages=message_text
        )
        # add to log of conversation
        message_text.append({"role": "assistant", "content" : completion.choices[0].message.content})
        # print(message_text)

        # send aclient message to discord
        # print(completion.choices[0].message.content)
        await channel.send(completion.choices[0].message.content)

@client.event
async def on_message(message):
    global message_text
    global last_message

    if message.author == client.user:
        return

    if message.content.startswith('$hello'):
        await message.channel.send('Hello!')
        return
    
    if message.content.startswith('$message'):
        # call openai api to send messages
        await get_message(message.channel)
        print("messaged")
        return
    
    # Dump conversation to file and quit
    if message.content.startswith('$quit'):
        await message.channel.send('Goodbye!')
        with open("convo.json", "w") as f:
            json.dump(message_text, f, indent=4)
        await client.close()
        return

    # create log of conversation for client
    message_text.append({"role": "user", "content": message.content,})

    # set function to send lull messages for each author
    if(not message.author in message_times):
        print("AUTHOR:" + message.author.display_name)
        message_times[message.author]=time.time()
        await send_message_after_delay(message.author, message.channel)
    else:
        message_times[message.author]=time.time()

    # elif message.content.startswith('$typing'):
    #     channel = client.get_channel(1169885828265279508)
    #     await channel.typing()
    #     await asyncio.sleep(3)
    #     await channel.send('Done typing!')

    # message_to_send = 'You said: "' + message.content + '"'
    # await message.channel.send(message_to_send)

    # if last_message == 0:
    #     await message.channel.send('this is the first message!')
    # else :
    #     await message.channel.send(f'time since last message: {time.time() - last_message} seconds')
    # last_message = time.time()

# @client.event
# async def on_typing(channel, user, when):
#     # time_elapsed = time.time()-last_message
#     await channel.send(f'{user} is typing.')
#     # last_message = time.time()

@client.event
async def on_typing(channel, user, when):
    typing_times[user.name]=time.time()


async def send_message_after_delay(user, channel):
    user_message_last = True
    print("FUNCTION HAS BEEN CALLED")
    while True:
        if(user in message_times):
            remaining_time = 15 - (time.time() - message_times[user])
            if remaining_time > 0:
                await asyncio.sleep(remaining_time)
            else:
                message_times[user] = time.time()
                if(user.name in typing_times and (typing_times[user.name] > time.time()-15)):
                    print("user typing")
                else:
                    print("This message is sent after waiting for 15 seconds.")
                    if user_message_last == True:
                        await get_message(channel)
                        user_message_last = False
                    
        else:
            return

client.run(token)
