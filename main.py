import discord
import os
import time
import discord.ext
from discord.utils import get
from discord.ext import commands, tasks
from discord.ext.commands import has_permissions,  CheckFailure, check
import requests
import chess
import sqlite3
from chess import Chess
import general
from general import General
import init
import currency
from currency import Currency

client = discord.Client()
client = commands.Bot(command_prefix = 'cb!')

init.init()

@client.event
async def on_ready():
    print("bot online") 

client.add_cog(Chess(client))
client.add_cog(General(client))
client.add_cog(Currency(client))

client.run(os.environ["token"])
