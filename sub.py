import discord
from discord.ext import commands
import asyncio
import nats
from os import getenv
from dotenv import load_dotenv

load_dotenv()

DISCORD_BOT_TOKEN = getenv('DISCORD_BOT_TOKEN')  
CHANNEL_ID = getenv('CHANNEL_ID')  
NATS_SERVER = "nats://localhost:4222"  

intents = discord.Intents.default()
intents.message_content = True  
bot = commands.Bot(command_prefix='!', intents=intents)

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user.name}')
    channel = bot.get_channel(CHANNEL_ID)
    if channel:
        await channel.send('Bot is now online!')
    # Set up NATS connection
    bot.loop.create_task(setup_nats())

@bot.command()
async def hello(ctx):
    await ctx.send('Hello there!')

@bot.command()
async def report(ctx):
    await ctx.send('Here is your stock report!', file=discord.File('stock_analysis.pdf'))

async def setup_nats():
    try:
        nc = await nats.connect(NATS_SERVER)
        
        async def handle_report_command(msg):
            channel = bot.get_channel(CHANNEL_ID)
            if channel:
                await channel.send('Here is your stock report!', file=discord.File('stock_analysis.pdf'))
                print("Report command executed via NATS")
        
        async def handle_hello_command(msg):
            channel = bot.get_channel(CHANNEL_ID)
            if channel:
                await channel.send('Hello from automation!')
                print("Hello command executed via NATS")
        
        await nc.subscribe("discord.command.report", cb=handle_report_command)
        await nc.subscribe("discord.command.hello", cb=handle_hello_command)
        
        print("Connected to NATS and subscribed to command topics")
    except Exception as e:
        print(f"Error setting up NATS: {e}")

if __name__ == "__main__":
    token = DISCORD_BOT_TOKEN
    bot.run(token)