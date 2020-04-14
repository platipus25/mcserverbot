# bot.py
import os
import io
import subprocess
from pathlib import Path
from time import sleep

import discord
from discord.ext import commands
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
GUILD = os.getenv('GUILD')

bot = commands.Bot(command_prefix="&")

src_path = Path(__file__).resolve().parent
server_path = Path(src_path).parent / "server"

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

@bot.command()
async def server(ctx, *arg):
  async with ctx.typing():
    result = subprocess.run([src_path/"minecraft_server.sh", *arg], capture_output=True, cwd=server_path)
    print(result)
    await ctx.send(result.stdout.decode("unicode_escape"))


detach = False
@bot.command()
async def attach(ctx):
  with open(server_path/"logs/latest.log", "r") as f:
    await ctx.send("Attaching...")
    f.seek(0, io.SEEK_END)
    while True:
      line = f.readline()
      print("another line read")
      sleep(1)
      if line:
        print(line)
        await ctx.send(line)

@bot.command()
async def detach(ctx):
  detach = True


@bot.command(name="/")
async def command(ctx, *, arg):
  with open(server_path/"logs/latest.log", "r") as f:
    f.seek(0, io.SEEK_END)
    with open(server_path/"mcfifo", "w") as fifo:
      fifo.write(arg)
      fifo.write("\n")
      fifo.flush()
    sleep(1)
    for line in f:
      print(line)
      await ctx.send(line)


bot.run(TOKEN)
