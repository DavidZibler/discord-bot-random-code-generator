# -----{ Imports requirements }-----
import discord
from discord.ext import commands
import os   # default module
from dotenv import load_dotenv


load_dotenv()   # load all the variables from the env file
bot = commands.Bot(command_prefix="/", intents=discord.Intents.all())


@bot.event
async def on_ready():
    print("---------------------------------------------------")
    print("RRC - Code Generator, bot is loaded & ready to use!")
    print("---------------------------------------------------")


bot.run(process.env.TOKEN)
