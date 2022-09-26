import discord
from discord.ext import commands
import sqlite3

conn = sqlite3.connect("main.db")
c = conn.cursor()

class Currency(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self._last_member = None

    