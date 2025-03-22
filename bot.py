import discord
from discord.ext import commands
from os import getenv
from dotenv import load_dotenv

load_dotenv()

# Set up the bot with a command prefix
bot = commands.Bot(command_prefix='!', intents=discord.Intents.default())

channel_id = getenv('CHANNEL_ID')

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user.name}')
    
    # Example: Send a message to a specific channel when the bot starts
    channel = bot.get_channel(channel_id)  # Replace CHANNEL_ID with your actual channel ID
    await channel.send('Bot is now online!')

# Example command
@bot.command()
async def hello(ctx):
    await ctx.send('Hello there!')

# To send files (like your PDF)
@bot.command()
async def report(ctx):
    await ctx.send('Here is your stock report!', file=discord.File('stock_analysis.pdf'))

token = getenv('DISCORD_BOT_TOKEN')
# Run the bot with your token
bot.run(token)