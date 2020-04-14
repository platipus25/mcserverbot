# bot.py
import os

import discord
from discord.ext import commands
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
GUILD = os.getenv('GUILD')

bot = commands.Bot(command_prefix="&")

@bot.event
async def on_ready():
    guild = discord.utils.get(bot.guilds, name=GUILD)
    print(
      f'{bot.user} has connected to Discord!\n'
      f'Guild: {guild.name}(id: {guild.id})'
    )

@bot.command()
async def helloworld(ctx, arg):
  await ctx.send(arg)

bot.run(TOKEN)
