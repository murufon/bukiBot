from discord.ext import commands
import logging
import cogs.ttscog as ttscog
import os
from os.path import join, dirname
from dotenv import load_dotenv

logging.basicConfig(level=logging.INFO)

bot = commands.Bot(command_prefix=commands.when_mentioned_or("!"),
                   description='Relatively simple music bot example')

@bot.event
async def on_ready():
    ttscog.setup(bot)
    print('Logged in as {0} ({0.id})'.format(bot.user))
    print('------')

if "BOT_TOKEN" not in os.environ:
    dotenv_path = join(dirname(__file__), '.env')
    load_dotenv(dotenv_path)
BOT_TOKEN = os.environ.get("BOT_TOKEN")
bot.run(BOT_TOKEN)
