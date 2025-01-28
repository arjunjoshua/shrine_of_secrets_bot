import discord
import datetime
from main import get_shrine_from_nightlight
from dotenv import load_dotenv
import os

load_dotenv()
token = os.getenv("DISCORD_TOKEN")

shrine_channel_id = os.getenv("SHRINE_CHANNEL_ID")

# Create a discord client
intents = discord.Intents.default()
intents.messages = True
client = discord.Client(intents=intents)


@client.event
async def on_ready():
    print(f'We have logged in as {client.user}')

    # get the shrine of secrets
    shrine_perks = get_shrine_from_nightlight()

    # send the shrine of secrets to the channel
    await send_to_channel(shrine_perks)


# send data to a channel
async def send_to_channel(shrine_of_secrets):
    channel = client.get_channel(int(shrine_channel_id))
    current_date = datetime.datetime.now().strftime("%m/%d/%Y")
    date_in_one_week = (datetime.datetime.now() + datetime.timedelta(days=7)).strftime("%m/%d/%Y")

    formatted_shrine = f"Shrine of Secrets for {current_date} - {date_in_one_week}\n" + "\n".join(shrine_of_secrets)

    if channel:
        await channel.send(formatted_shrine)

    # close the connection
    await client.close()

# start the bot
client.run(token)

