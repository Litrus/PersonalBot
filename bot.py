import discord
import os
import asyncio
from discord.ext import commands
from dotenv import load_dotenv

class myBot(commands.Bot):
    def __init__(self, *, intents: discord.Intents):
        super().__init__(command_prefix = '/', intents = intents, help_command=None, )

    async def setup_hook(self) -> None:
        await self.load_extension('cog.apiFunctions')
        await self.load_extension('cog.voice')
    async def close(self) -> None:
        await super().close()

async def main():
    load_dotenv()
    print("Loading tokens in main..")

    async with myBot(intents = discord.Intents.all()) as bot:
        @bot.event
        async def on_ready():
            print(f'{bot.user} is online')
            try:
                synced = await bot.tree.sync()
                print(f"Synced {len(synced)} command(s)")
            except Exception as e:
                print(e)

        #Reload all cogs
        @commands.is_owner()
        @bot.tree.command(name = "reload")
        async def reload_cogs(interaction: discord.Interaction):
            print("Reloading cogs...")
            cogs = list(bot.extensions.keys())
            for cog in cogs:
                await bot.reload_extension(cog)
                print(f"User {interaction.user} has reloaded {cog} ")
            await interaction.response.send_message("Reloaded all cogs", ephemeral=True)

        @bot.tree.command(name = "hello")
        async def hello(interaction: discord.Interaction):
            await interaction.response.send_message(f"Hello {interaction.user.mention}!")

        await bot.start(os.getenv('DISCORD_TOKEN'))#Accesses default aenter method of the bot class

asyncio.run(main(), debug = True)