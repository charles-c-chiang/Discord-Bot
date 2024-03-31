import discord
from discord.ext import commands
import openai
from openai import AsyncAzureOpenAI
import os
import json
import asyncio

# get API key from auth.json
f = open('auth.json')
OPENAI_API_KEY = json.load(f)['OPENAI_API_KEY']

class Messages(commands.Cog) :
    def __init__(self, aclient):
        self.aclient = aclient

    @commands.Cog.listener()
    async def on_member_join(self, member):
        channel = member.guild.system_channel
        if channel is not None:
            await channel.send(f'Welcome {member.mention}.')
    
    # @commands.command()
    # async def messagehandler(self, ctx : )