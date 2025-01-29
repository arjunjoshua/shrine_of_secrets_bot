#!/usr/bin/env python3

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
    date = datetime.datetime.now()

    # Get the next Tuesday's date
    while date.weekday() != 3:
        date += datetime.timedelta(days=1)

    shrine_refresh_date = date.strftime("%b %d, %Y") + " 16:00 UTC"

    formatted_shrine = (f"Shrine of Secrets currently contains the following perks:\n\n" + "\n".join(shrine_of_secrets)
                        + f"\n\nAvailable until {shrine_refresh_date}")

    if channel:
        await channel.send(formatted_shrine)

    # close the connection
    await client.close()

# start the bot
client.run(token)

