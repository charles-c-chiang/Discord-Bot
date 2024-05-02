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
intents.members = True 

client = discord.Client(intents=intents)

AIclient = AsyncAzureOpenAI(api_key = OPENAI_API_KEY,
api_version = "2024-02-01", 
azure_endpoint="https://charlietest.openai.azure.com/openai/deployments/charles-4/chat/completions?api-version=2024-02-01")
message_text = [{"role":"system","content":"You are StrangerBot, an introduction chatbot. Your job is to interact with two different strangers, and help them get to know each other better. You can do this by recommending them topics to talk about or asking them to share more about themselves. You should start each conversation by introducing yourself, then by asking both people some basic facts about them. The strangers want to be anonymous, so you should refer to them by their username and not ask their name. You should not have overly lengthy or detailed responses, as the focus of the conversation should be between the two strangers and you want to keep a friendly, casual tone."}]

check_balance_time = 30
end_warning_time = 120
balance_threshold= 20
activity_points = {}

async def run_on_interval(func, channel, time):
    while True:
        await asyncio.sleep(time)
        await func(channel)

async def check_balance(channel):
    members = list(activity_points.keys())
    if(abs(activity_points[members[0]]-activity_points[members[1]]) > balance_threshold):
        if(activity_points[members[0]] > activity_points[members[1]]):
            await channel.send(f"{members[1]} talk more pls")
        else:
            await channel.send(f"{members[0]} talk more pls")
    activity_points[members[0]] = 0
    activity_points[members[1]] = 0

async def end_warning(channel):
    await channel.send("One minute remaining!")

@client.event
async def on_ready():
    print(f'We have logged in as {client.user}')
    channel = client.get_channel(1169885828265279508)
    await channel.send(f'Logged in as Bot! Time is {datetime.now()}')
    # Call the function to send a message from OpenAI
    await get_message(channel)
    members = channel.members
    for member in members:
        if member.name != 'TestIntroBot':
            activity_points[member.name] = 0
    await run_on_interval(check_balance, channel, check_balance_time)
    await run_on_interval(end_warning, channel, end_warning_time)

last_message = 0
wait_time = 16.28
message_time = time.time()
typing_time = time.time()
bot_message_last = True
members = []

#gets message from openai
async def get_message(channel):
        # send conversation to aclient, await response
        completion = await AIclient.chat.completions.create(
            model="charles-4",  # e.g. gpt-35-instant
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
    global bot_message_last 
    global message_time
    global typing_time
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
    message_text.append({"role": "user", "content": str(message.author.name) + ": " + message.content,})
    if(not message.author in activity_points):
        activity_points[message.author.name] = len(message.content)
    else:
        activity_points[message.author.name] = len(message.content)

    # set function to send lull messages for each author
    message_time=time.time()
    if(bot_message_last):
        bot_message_last = False
        await send_message_after_delay(message.channel)


@client.event
async def on_typing(channel, user, when):
    global typing_time
    typing_time=time.time()


async def send_message_after_delay(channel):
    global bot_message_last
    global message_time
    global typing_time
    while True:
        remaining_time = wait_time - (time.time() - message_time)
        if remaining_time > 0:
            await asyncio.sleep(remaining_time)
        else:
            message_time = time.time()
            if(typing_time > time.time()-wait_time):
                print("user typing")
                message_time = typing_time
            else:
                print("This message is sent after waiting for "+str(wait_time)+" seconds.")
                bot_message_last = True
                await get_message(channel)      
                return;



client.run(token)
