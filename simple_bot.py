# This example requires the 'message_content' intent.

import discord
import json
import asyncio
import time
from datetime import datetime
from discord.ext import tasks, commands

f = open('auth.json')
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
wait_time = 16.28
message_time = time.time()
typing_times = time.time()
bot_message_last = False
activity_points = {}

#gets message from openai *CHANGE TO GET BACKGROUND FROM FORM*
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
        activity_points[message.author] = len(message.content)
        print(str(message.author.name) + ": " + str(activity_points[message.author]))
    else:
        activity_points[message.author] = len(message.content)
        print(str(message.author.name) + ": " + str(activity_points[message.author]))

    # set function to send lull messages for each author
    if(not message.author in message_times):
        message_times[message.author]=time.time()
        user_message_last = True
        await send_message_after_delay(message.author, message.channel)
    else:
        user_message_last = True
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
    while True:
        if(user in message_times):
            remaining_time = wait_time - (time.time() - message_times[user])
            if remaining_time > 0:
                await asyncio.sleep(remaining_time)
            else:
                if(user.name in typing_times and (typing_times[user.name] > time.time()-wait_time)):
                    print("user typing")
                    message_times[user] = typing_times[user.name]
                    user_message_last = True
                else:
                    print("This message is sent after waiting for "+str(wait_time)+" seconds.")
                    message_times[user] = time.time()
                    bot_message_last = True
                    # if user_message_last == True:
                    #     user_message_last = False
                    await get_message(channel)
                    
        else:
            return

client.run(token)
