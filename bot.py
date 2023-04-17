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

def run_discord_bot():
    print("Bot waking up...")
    TOKEN = os.getenv('DISCORD_TOKEN')
    intents = discord.Intents.all()
    intents.message_content = True
    bot = commands.Bot(command_prefix='/', intents=intents)

    @bot.event
    async def on_ready():
        print(f'{bot.user} is now running!')
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
            url = f'https://api.openweathermap.org/data/2.5/weather?q={location}&appid={API_KEY}'  # takes a city and api key
            response = requests.get(url)  # fetches the data with a http request using the formatted url(json format)
            data = json.loads(response.text)  # creates a dictionary from the response JSON returned
            weather = data['weather'][0]['description']
            country = data['sys']['country']
            temperature = round(float(data['main']['temp']) - 273.15)  # kelvin to c
            feelslike = round(float(data['main']['feels_like']) - 273.15)
            humidity = data['main']['humidity']
            message = f"The weather in {country}, {location} is a/an {weather}. \nThe temperature is {temperature}\N{DEGREE SIGN}C and feels like {feelslike}\N{DEGREE SIGN}C. \nThe humidity is {humidity}%."
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

    bot.run(TOKEN)


'''
async def send_message(message, user_message, is_private):
    try:
        response = await responses.handle_responses(user_message, message)
        await message.author.send(response) if is_private else await message.channel.send(response)
    except Exception as e:
        print(e)

    @bot.command
    async def on_message(message):
        if message.author == bot.user:
            return
        #prevents the bot from sending messages in response to itself

        username = str(message.author)
        user_message = str(message.content)
        channel = str(message.channel)

        #if user prefixes their message with a '?' bot will send a private DM and respond based on the message
        #content sent after the '?'
        #otherwise send the response in the same channel as the message sent
        print(f"{username} said: '{user_message}' in ({channel})")
        if user_message[0] == '?':
            user_message = user_message[1:]
            await send_message(message, user_message, is_private=True)

        if message.content in react_words:
            await message.add_reaction('\U0001F60E')
        else:
            await send_message(message, user_message, is_private=False)
'''

