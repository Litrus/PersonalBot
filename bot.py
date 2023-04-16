import discord
import os
import asyncio
from discord.ext import commands, tasks
from dotenv import load_dotenv

import bot

load_dotenv()
print("Loading tokens..")


def run_discord_bot():
    print("Waking up...")
    TOKEN = os.getenv('DISCORD_TOKEN')
    intents = discord.Intents.default()
    intents.message_content = True
    bot = commands.Bot(command_prefix='/', intents=intents)

    @bot.event
    async def on_ready():
        print(f'{bot.user} is now running!')

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

