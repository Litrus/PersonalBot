import discord
import os
import asyncio
import requests
import json
from discord.ext import commands
from discord import app_commands
from dotenv import load_dotenv

load_dotenv()
print("Loading tokens..")

def main():
    print("Bot waking up...")
    intents = discord.Intents.all()
    intents.message_content = True
    bot = commands.Bot(command_prefix='/', intents=intents)

    @bot.event
    async def on_ready():
        print(f'{bot.user} is online')
        try:
            synced = await bot.tree.sync()
            print(f"Synced {len(synced)} command(s)")
        except Exception as e:
            print(e)

    @bot.tree.command(name = "hello")
    async def hello(interaction: discord.Interaction):
        await interaction.response.send_message(f"Hello {interaction.user.mention}!")

    @bot.tree.command(name = "weather")
    @app_commands.describe(location = "City to check")
    async def weather(interaction: discord.Interaction, location: str):
        API_KEY = os.getenv("WEATHER_API_KEY")
        try:
            url = f'https://api.openweathermap.org/data/2.5/weather?q={location}&appid={API_KEY}'  #Leaving api_key as ver to be more readable
            print(url)
            response = requests.get(url)  # fetches the data with a http request using the formatted url(json format)
            data = json.loads(response.text)  # creates a dictionary from the response JSON returned
            weather = data['weather'][0]['description']
            country = data['sys']['country']
            temperature = round(float(data['main']['temp']) - 273.15)  #kelvin to c
            feelslike = round(float(data['main']['feels_like']) - 273.15)
            humidity = data['main']['humidity']
            message = f"The weather in {country}, {location} is {weather}. \nThe temperature is {temperature}\N{DEGREE SIGN}C and feels like {feelslike}\N{DEGREE SIGN}C. \nThe humidity is {humidity}%."
            print("Fetched successfully: ", response)
            await interaction.response.send_message(message)
        except Exception as e:
            print("Unsuccessful fetch: invalid location, API key is not working or openweather API is down.")

    # showing edited messages
    @bot.event
    async def on_message_edit(before, after):
        if after.author == bot.user:
            return

        username = str(after.author)
        prev = before.content
        post = after.content
        channel = str(after.channel)
        print(f"{username} edited a message in '{channel}. Prior to edit: '{prev}' after edit: '{post}'")

    bot.run(os.getenv('DISCORD_TOKEN'))

asyncio.run(main(), debug=True)

'''TO DO
    Remove main, run bot from just this one python file
    
    Figure out cogs, create a voice module that will control voice channel activities such as: join, leave and audio processing such as
    reading/playing audio files. Incorporate spotipy and play a song from a playlist.
    
    Maybe: api cog for any api calls if adding more api commands.
    
    Daily checklist that spawns at x time. should have: checklist with items that can be ticked and unticked,
    a submission button to acknowledge that everything is done for the day. Create a database to store
    finished tasks, etc.
    
    '''