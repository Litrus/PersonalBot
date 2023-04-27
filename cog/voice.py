import discord
from discord import app_commands, VoiceClient, VoiceState
from discord.ext import commands


class voiceFunctions(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot: commands.Bot = bot
        print("Voice Functions loaded")

    @app_commands.command(name = "join")
    async def join(self, interaction: discord.Interaction):
        try:
            await interaction.user.voice.channel.connect()
            await interaction.response.send_message("Joined channel", ephemeral=True)
            print(f"{self.bot.user} joined channel {interaction.user.voice.channel}")
        except Exception as e:
            print(e)
            await interaction.response.send_message("You are not in a voice channel", ephemeral=True)

    @app_commands.command(name = "leave")
    async def leave(self, interaction: discord.Interaction):
        try:
            voiceClient = interaction.guild.voice_client #voice_client only exists if the bot has joined a voice channel
            await voiceClient.disconnect(force=True)
            await interaction.response.send_message("Left channel", ephemeral=True)
            print(f"{self.bot.user} left channel {interaction.user.voice.channel}")
        except Exception as e:
            print(e)

"""
set up spotipy/look at library.
Figure out how to play an audio file first?
"""

async def setup(bot):
    await bot.add_cog(voiceFunctions(bot))

async def teardown(bot):
    await bot.remove_cog(voiceFunctions(bot))