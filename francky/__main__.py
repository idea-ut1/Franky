import discord
import os
from dotenv import load_dotenv
from .bot import Bot

def main():
    load_dotenv()
    TOKEN = os.getenv('TOKEN')
    GUILD_ID = os.getenv('GUILD_ID')
    intents = discord.Intents.all()
    bot = Bot(command_prefix='!', intents=intents, guild_id=GUILD_ID)
    bot.run(TOKEN)

if __name__ == '__main__':
    main()