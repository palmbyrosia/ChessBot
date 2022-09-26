import discord
from discord.ext import commands
import sqlite3

class General(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self._last_member = None

    @commands.command(brief='Gives the id of a specifified member or yourself')
    async def id(ctx, member : discord.Member = None):
      if member == None:
        await ctx.send("Your id is " + str(ctx.message.author.id))
        return
      await ctx.send("This member's id is " + str(member.id))

    