# importing required dependencies
import discord
from discord.ext import commands
import os
import asyncio
import cogs._json
import logging
from pathlib import Path
import json

# Printing and storing the path of the bot.py file
cwd = Path(__file__).parents[0]
cwd = str(cwd)
print(f"{cwd}\n-----")


def get_prefix(bot, message):
    data = cogs._json.read_json('prefixes')
    if not str(message.guild.id) in data:
        return commands.when_mentioned_or('tut!')(bot, message)
    return commands.when_mentioned_or(data[str(message.guild.id)])(bot, message)

# Defining important dependencies
secret_file = json.load(open(cwd+"/bot_config/secrets.json"))
bot = commands.Bot(command_prefix="cf!", case_insensitive=True, intents=discord.Intents.all())
bot.config_token = secret_file["token"]
logging.basicConfig(level=logging.INFO)

bot.version = "1.0"

bot.blacklisted_users = []


@bot.event
async def on_ready():
    print(f"-----\nLogged in as: {bot.user.name} : {bot.user.id}\n-----\nMy current prefix is: {get_prefix}\n-----")
    print("Let the chaos begin!\n-----")
    data = cogs._json.read_json("blacklist")
    bot.blacklisted_users = data["blacklistedUsers"]
    await bot.change_presence(activity=discord.Game(name=f"Use {get_prefix}help to induce chaos to this server!"))


@bot.event
async def on_message(message):
    # Ignore messages sent by yourself
    if message.author.id == bot.user.id:
        return

    # A way to blacklist users from the bot by not processing commands if the author is blacklisted
    if message.author.id in bot.blacklisted_users:
        return

    # Whenever the bot is tagged, respond with its prefix
    if bot.user.mention in message.content:
        data = cogs._json.read_json("prefixes")
        if str(message.guild.id) in data:
            prefix = data[str(message.guild.id)]
        else:
            prefix = 'tut!'
        prefixMsg = await message.channel.send(f"My prefix is `{prefix}`")
        await prefixMsg.add_reaction('👀')

    await bot.process_commands(message)


async def load():
    for file in os.listdir(cwd+"/cogs"):
        if file.endswith(".py") and not file.startswith("_"):
            await bot.load_extension(f"cogs.{file[:-3]}")


async def main():
    await load()
    await bot.start(bot.config_token)

# Run the bot
asyncio.run(main())
