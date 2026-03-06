import discord
import os
from discord.ext import commands
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv("BOT_TOKEN")

class MyBot(commands.Bot):
    def __init__(self):
        intents = discord.Intents.default()
        intents.message_content = True
        intents.members = True 
        super().__init__(command_prefix='!', intents=intents)

    async def setup_hook(self):
        for filename in os.listdir('./cogs'):
            if filename.endswith('.py'):
                await self.load_extension(f'cogs.{filename[:-3]}')
                print(f'Módulo {filename} carregado.')

        await self.tree.sync()
        print('Comandos de barra sincronizados!')

bot = MyBot()

@bot.event
async def on_ready():
    print(f'Bot logado como {bot.user}')

bot.run(TOKEN)