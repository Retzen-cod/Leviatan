from discord.ext import commands
import logging

logger = logging.getLogger(__name__)
class PingCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        logger.debug(f"PingCog initialized for bot: {bot.user if bot.user else 'Not connected'}")

    @commands.command(name="ping")
    async def ping(self, ctx):
        logger.debug(f"Ping command executed by {ctx.author} in {ctx.guild}")
        latency = round(self.bot.latency * 1000)
        await ctx.send(f"Pong! Latency: {latency}ms")

async def setup(bot):
    logger.debug("Setting up PingCog")
    await bot.add_cog(PingCog(bot))
    logger.debug("PingCog setup completed")
