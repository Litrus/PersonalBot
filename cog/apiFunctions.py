import discord
from discord import app_commands
from discord.ext import commands
import requests
import json
from dotenv import load_dotenv
import os

class apiFunctions(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot: commands.Bot = bot
        print("API Functions loaded")

    load_dotenv()
    print("Loading tokens in apiFunctions..")

    @app_commands.command(name = "weather", description="Enter location/city")
    async def weather(self, interaction: discord.Interaction, location: str):
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

async def setup(bot):
    await bot.add_cog(apiFunctions(bot))

async def teardown(bot):
    await bot.remove_cog(apiFunctions(bot))