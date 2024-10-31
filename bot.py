import discord
import aiohttp
from apscheduler.schedulers.asyncio import AsyncIOScheduler

# Discord bot token
TOKEN = 'tokenbotdiscord'  # Replace with your Discord bot token

# API URL for ORE token price
PRICE_API_URL = 'https://api.coingecko.com/api/v3/simple/price?ids=ore&vs_currencies=usd'

# Create an instance of Intents
intents = discord.Intents.default()
intents.message_content = True  # Required to read message content

# Initialize Discord client with intents
client = discord.Client(intents=intents)
scheduler = AsyncIOScheduler()

async def update_status():
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(PRICE_API_URL) as response:
                data = await response.json()
                price = data['ore']['usd']  # Adjust based on the ORE token's API response
                status_message = f'ORE price: ${price}'
                await client.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name=status_message))
                print(f'Updated status: {status_message}')
    except Exception as e:
        print(f'Error fetching price: {e}')

@client.event
async def on_ready():
    print(f'Logged in as {client.user}')
    # Update status immediately on startup
    await update_status()
    # Schedule the status update every 10 seconds
    scheduler.add_job(update_status, 'interval', seconds=10)
    scheduler.start()

# Run the bot
client.run(TOKEN)`
