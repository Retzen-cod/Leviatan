import discord
from discord.ext import commands
from src.commandhandler import CommandHandler
from ASCII_animation import show_startup_animation
import os
from dotenv import load_dotenv
import logging

load_dotenv()

class LeviatanBot(commands.Bot):
    def __init__(self, application_id):
        # Cargar prefijo desde .env, usar '!' como valor por defecto
        command_prefix = os.getenv('COMMAND_PREFIX', '!')
        # Pasa application_id al constructor para evitar MissingApplicationID
        super().__init__(command_prefix=command_prefix, intents=discord.Intents.all(), application_id=application_id)
        self.command_handler = CommandHandler(self)
        logging.basicConfig(level=logging.INFO)
        self.logger = logging.getLogger(__name__)
        self.logger.info(f"Bot initialized with prefix: {command_prefix}")
    # Se remueve setup_hook para dejar la carga de comandos explícita en main

async def main():
    # Primero, cargar token, prefijo y application_id desde .env
    token = os.getenv('DISCORD_TOKEN')
    application_id = os.getenv('APPLICATION_ID')
    prefix = os.getenv('COMMAND_PREFIX', '!')
    print(f'Application ID: {application_id}')
    print(f'Command prefix: {prefix}')

    # Crear bot con application_id, lo que carga commandhandler.py en __init__
    bot = LeviatanBot(application_id)
    # Cargar comandos manualmente (antes de iniciar el bot)
    await bot.command_handler.load_commands()
    
    @bot.event
    async def on_ready():
        # Sincroniza el tree de comandos una vez que el bot está listo
        await bot.tree.sync()
        show_startup_animation()
        print(f'Bot conectado como {bot.user}')
        
    await bot.start(token)

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
