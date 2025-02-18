import os
from discord.ext import commands
from discord import app_commands
import importlib.util
import logging
import inspect

class CommandHandler:
    def __init__(self, bot):
        self.bot = bot
        self.commands_dir = os.path.join(os.path.dirname(__file__), 'commands')
        
        # Configurar logging más detallado
        self.logger = logging.getLogger(__name__)
        self.logger.setLevel(logging.DEBUG)
        
        # Añadir handler para consola con formato detallado
        console_handler = logging.StreamHandler()
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        console_handler.setFormatter(formatter)
        self.logger.addHandler(console_handler)
        
        self.logger.debug(f"CommandHandler initialized with directory: {self.commands_dir}")

    async def convert_to_slash_command(self, cmd):
        self.logger.debug(f"Converting command to slash command: {cmd.name}")
        
        # Crear un comando de aplicación basado en el comando existente
        @app_commands.command(
            name=cmd.name,
            description=cmd.help or f"No description available for {cmd.name}"
        )
        async def slash_command(interaction, *args, **kwargs):
            ctx = await commands.Context.from_interaction(interaction)
            await cmd.callback(ctx, *args, **kwargs)
            
        return slash_command

    async def load_command_file(self, filename):
        try:
            module_name = filename[:-3]
            file_path = os.path.join(self.commands_dir, filename)
            
            self.logger.debug(f"=== Starting load process for {filename} ===")
            self.logger.debug(f"Full path: {file_path}")
            self.logger.debug(f"Module name: {module_name}")
            
            # Verificar que el archivo existe
            if not os.path.exists(file_path):
                self.logger.error(f"File does not exist: {file_path}")
                return
            
            # Load module dynamically
            spec = importlib.util.spec_from_file_location(module_name, file_path)
            module = importlib.util.module_from_spec(spec)
            self.logger.debug(f"Created module spec: {spec}")
            
            spec.loader.exec_module(module)
            self.logger.debug(f"Executed module: {module}")

            # Intentar llamar al setup si existe
            if hasattr(module, 'setup'):
                self.logger.debug("Found setup function, calling it")
                await module.setup(self.bot)
                return

            # Si no hay setup, buscar Cogs
            # Debug del contenido del módulo
            self.logger.debug("Module contents:")
            for name, obj in inspect.getmembers(module):
                self.logger.debug(f" - {name}: {type(obj)}")
            
            # Look for Cog classes
            cog_count = 0
            for item_name, item in inspect.getmembers(module):
                if isinstance(item, type) and issubclass(item, commands.Cog) and item != commands.Cog:
                    self.logger.debug(f"Found Cog class: {item_name}")
                    cog = item(self.bot)
                    
                    # Convertir comandos normales a slash commands
                    for cmd_name, cmd in inspect.getmembers(cog):
                        if isinstance(cmd, commands.Command):
                            self.logger.debug(f"Converting command: {cmd_name}")
                            slash_cmd = await self.convert_to_slash_command(cmd)
                            cog.app_commands.append(slash_cmd)
                    
                    await self.bot.add_cog(cog)
                    self.logger.info(f"Successfully loaded Cog: {item_name} from {module_name}")
                    cog_count += 1
            
            if cog_count == 0:
                self.logger.warning(f"No Cog classes found in {filename}")
            
            self.logger.debug(f"=== Finished loading {filename} ===")
            
        except Exception as e:
            self.logger.error(f"Error loading command {filename}: {str(e)}", exc_info=True)
            raise

    async def load_commands(self):
        try:
            self.logger.debug("=== Starting command loading process ===")
            
            if not os.path.exists(self.commands_dir):
                self.logger.error(f"Commands directory does not exist: {self.commands_dir}")
                return
            
            files = os.listdir(self.commands_dir)
            self.logger.debug(f"Found files in directory: {files}")
            
            py_files = [f for f in files if f.endswith('.py')]
            self.logger.info(f"Found {len(py_files)} Python files: {py_files}")
            
            for filename in py_files:
                await self.load_command_file(filename)
            
            # Remover o comentar la sincronización temprana:
            # await self.bot.tree.sync()
            
            self.logger.debug("=== Command loading process completed ===")
                    
        except Exception as e:
            self.logger.error("Error in load_commands", exc_info=True)
            raise
