import discord
from discord.ext import commands
import requests
import sqlite3

conn = sqlite3.connect("main.db")
c = conn.cursor()

def linkuser(id, username):
  sql = """INSERT INTO link(user_id, username)
            VALUES(?,?)"""
  vals = (id, username)
  c.execute(sql, vals)
  conn.commit()

def getusername(id):
  sql = """SELECT username FROM link WHERE user_id=?"""
  c.execute(sql, (id,))
  test = c.fetchall()
  if len(test)>0:
    return test[0][0]
  else:
    return None

class Chess(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self._last_member = None

    @commands.command(brief='Converts a lichess rating into an adjusted approximate chess.com rating')
    async def li2chess(self, ctx, rate, typeof="rapid"): 
      rating = int(rate)
      if 3000<rating<100:
        await ctx.send("Please send a valid rating")
      elif typeof == "rapid":
        await ctx.send("**Adjusted Rating for Chess.com:** "+str(rating*1.025-277)+ " (Change of "+str((rating*1.025-277)-rating)+" or "+ str(((rating*1.025-277)/rating)*100-100) +"%)")
      elif typeof == "blitz":
        await ctx.send("**Adjusted Rating for Chess.com:** "+str(rating*1.138-665)+ " (Change of "+str((rating*1.138-665)-rating)+" or "+ str(((rating*1.138-665)/rating)*100-100) +"%)")
      elif typeof == "bullet":
        await ctx.send("**Adjusted Rating for Chess.com:** "+str(rating*1.162-624)+ " (Change of "+str((rating*1.162-624)-rating)+" or "+ str(((rating*1.162-624)/rating)*100-100) +"%)")
      else:
        await ctx.send("Please pass in a valid type of rating (rapid, blitz, bullet) or for rapid do not pass anything at all. (Second Argument)")
    @commands.command(brief='Converts a chess.com rating into an adjusted approximate lichess rating')
    async def chess2li(self, ctx, rate, typeof="rapid"): 
      rating = int(rate)
      if 3000<rating<100:
        await ctx.send("Please send a valid rating")
      elif typeof == "rapid":
        await ctx.send("**Adjusted Rating for Lichess**: "+str((rating+277)/1.025)+ " (Change of "+str(((rating+277)/1.025)-rating)+" or "+ str((((rating+277)/1.025)/rating)*100-100) +"%)")
      elif typeof == "blitz":
        await ctx.send("**Adjusted Rating for Lichess**: "+str((rating+665)/1.138)+ " (Change of "+str(((rating+665)/1.138)-rating)+" or "+ str((((rating+665)/1.138)/rating)*100-100) +"%)")
      elif typeof == "bullet":
        await ctx.send("**Adjusted Rating for Lichess**: "+str((rating+624)/1.162)+ " (Change of "+str(((rating+624)/1.162)-rating)+" or "+ str((((rating+624)/1.162)/rating)*100-100) +"%)")
      else:
        await ctx.send("Please pass in a valid type of rating (rapid, blitz, bullet) or for rapid do not pass anything at all. (Second Argument)")
    @commands.command(brief='Allows you to change the account of your link')
    async def update_link(self, ctx, username=None):
      if getusername(ctx.message.author.id) == None:
        await ctx.send(f'You have no already linked account, just use the regular cb!link command')
        return

      response = requests.get('https://api.chess.com/pub/player/' + username + '/stats')
      obj = response.json()

      if "code" in obj.keys():
        await ctx.send(f'The username **{username}** is an invalid chess.com username. Please try again!')
        return

      sql = '''UPDATE link
              SET username=?
              WHERE user_id=?'''
      vals = (username, ctx.author.id)
      c.execute(sql, vals)
      conn.commit()
      

    @commands.command(brief='Allows you to link your chess.com rating to your account')
    async def link(self, ctx, username=None):
      if username == None:
        await ctx.send("You have not passed in a chess.com username")
        return

      response = requests.get('https://api.chess.com/pub/player/' + username + '/stats')
      obj = response.json()
      
      if "code" in obj.keys():
        await ctx.send(f'The username **{username}** is an invalid chess.com username. Please try again!')
        return

      if not getusername(ctx.message.author.id) == None:
        await ctx.send(f'Account **{getusername(ctx.message.author.id)}** is already linked to your account')
        return

      linkuser(ctx.message.author.id, username)
      await ctx.send(f'The username **{username}** was successfully linked')

      
    @commands.command(brief='Shows the ratings of a specified chess.com username or a chess.com account linked to your discord')
    async def ratingof(self, ctx, member : discord.Member):
      username = None
      if getusername(member.id) == None:
        await ctx.send('The member you passed in does not have a linked chess.com account')
        return
      username = getusername(member.id)
      response = requests.get('https://api.chess.com/pub/player/' + username + '/stats')
      obj = response.json()
      
      if "code" in obj.keys():
        await ctx.send(f'The username **{username}** is an invalid chess.com username. Please try again!')
        return

      response = requests.get('https://api.chess.com/pub/player/' + username)
      obj1 = response.json()
      
      embedVar = discord.Embed(title="Chess.com Stats for "+username)
      try:
        embedVar.add_field(name="Rapid", value=obj['chess_rapid']['last']['rating'], inline=False)
      except:
        embedVar.add_field(name="Rapid", value=0, inline=False)

      try:
        embedVar.add_field(name="Blitz", value=obj['chess_blitz']['last']['rating'], inline=False)
      except:
        embedVar.add_field(name="Blitz", value=0, inline=False)

      try:
        embedVar.add_field(name="Bullet", value=obj['chess_bullet']['last']['rating'], inline=False)
      except:
        embedVar.add_field(name="Bullet", value=0, inline=False)

      try:
        embedVar.add_field(name="Title", value=obj1['title'], inline=False)
      except:
        print("Dis boi don't have a title")

      await ctx.send(embed=embedVar)

    @commands.command(brief='Shows the ratings of a specified chess.com username or a chess.com account linked to your discord')
    async def rating(self, ctx, usernam = None):
      username = usernam
      if username == None and getusername(ctx.author.id) == None:
        await ctx.send("You have not setup chess.com account linking. Please pass in a **chess.com username** or **link your account with cb!link <chess.com username>**")
        return   
      elif username == None and not getusername(ctx.author.id) == None:
        username = getusername(ctx.author.id)
      
      response = requests.get('https://api.chess.com/pub/player/' + username + '/stats')
      obj = response.json()
      
      if "code" in obj.keys():
        await ctx.send(f'The username **{username}** is an invalid chess.com username. Please try again!')
        return

      
          

      response = requests.get('https://api.chess.com/pub/player/' + username)
      obj1 = response.json()
      
      embedVar = discord.Embed(title="Chess.com Stats for "+username)
      try:
        embedVar.add_field(name="Rapid", value=obj['chess_rapid']['last']['rating'], inline=False)
      except:
        embedVar.add_field(name="Rapid", value=0, inline=False)

      try:
        embedVar.add_field(name="Blitz", value=obj['chess_blitz']['last']['rating'], inline=False)
      except:
        embedVar.add_field(name="Blitz", value=0, inline=False)

      try:
        embedVar.add_field(name="Bullet", value=obj['chess_bullet']['last']['rating'], inline=False)
      except:
        embedVar.add_field(name="Bullet", value=0, inline=False)

      try:
        embedVar.add_field(name="Title", value=obj1['title'], inline=False)
      except:
        print("Dis boi don't have a title")

      await ctx.send(embed=embedVar)

      if usernam == None:
        member = ctx.author
        ratingrole = []
        ratingrole.append(discord.utils.find(lambda r: r.id == 843931363949805600, ctx.message.guild.roles))
        ratingrole.append(discord.utils.find(lambda r: r.id == 843933305853837312, ctx.message.guild.roles))
        ratingrole.append(discord.utils.find(lambda r: r.id == 843938079064588319, ctx.message.guild.roles))
        ratingrole.append(discord.utils.find(lambda r: r.id == 843938170679984138, ctx.message.guild.roles))
        ratingrole.append(discord.utils.find(lambda r: r.id == 843938230423388180, ctx.message.guild.roles))
        ratingrole.append(discord.utils.find(lambda r: r.id == 843938306802581584, ctx.message.guild.roles))
        ratingrole.append(discord.utils.find(lambda r: r.id == 843938403480764466, ctx.message.guild.roles))
        ratingrole.append(discord.utils.find(lambda r: r.id == 843938548872642600, ctx.message.guild.roles))

        for i in ratingrole:
          await member.remove_roles(i)
        rating = obj['chess_rapid']['last']['rating']
        if not rating or rating<=600:
          await member.add_roles(ratingrole[0])
        elif rating<=800:
          await member.add_roles(ratingrole[1])
        elif rating<=1000:
          await member.add_roles(ratingrole[2])
        elif rating<=1200:
          await member.add_roles(ratingrole[3])
        elif rating<=1400:
          await member.add_roles(ratingrole[4])
        elif rating<=1600:
          await member.add_roles(ratingrole[5])
        elif rating<=1800:
          await member.add_roles(ratingrole[6])
        else:
          await member.add_roles(ratingrole[7])
          