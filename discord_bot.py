#!/usr/bin/env python3
import discord
import datetime
from main import get_shrine_from_nightlight
from dotenv import load_dotenv
import os
from discord.ext import commands
import asyncio

load_dotenv()
token = os.getenv("DISCORD_TOKEN")
shrine_channel_id = os.getenv("SHRINE_CHANNEL_ID")

# Create a discord client
intents = discord.Intents.default()
intents.messages = True
intents.message_content = True
bot = commands.Bot(command_prefix='!', intents=intents)


@bot.event
async def on_ready():
    print(f'We have logged in as {bot.user}')

    # # get the shrine of secrets
    # shrine_perks = get_shrine_from_nightlight()
    #
    # # send the shrine of secrets to the channel
    # await send_to_channel(shrine_perks)


@bot.command()
async def shrine(ctx: commands.Context):
    # get the shrine of secrets
    shrine_perks = get_shrine_from_nightlight()

    # send the shrine of secrets to the channel
    await send_to_channel(shrine_perks)


# send data to a channel
async def send_to_channel(shrine_of_secrets):
    channel = bot.get_channel(int(shrine_channel_id))
    date = datetime.datetime.now()

    # Get the next Tuesday's date
    while date.weekday() != 3:
        date += datetime.timedelta(days=1)

    shrine_refresh_date = date.strftime("%b %d, %Y") + " 16:00 UTC"

    formatted_shrine = (f"The Shrine of Secrets currently contains the following perks:\n\n" + "\n".join(shrine_of_secrets)
                        + f"\n\nAvailable until {shrine_refresh_date}")

    if channel:
        await channel.send(formatted_shrine)


async def schedule_weekly_shrine():
    await bot.wait_until_ready()  # Wait until bot is ready

    while not bot.is_closed():
        now = datetime.datetime.utcnow()
        target_time = now.replace(hour=16, minute=0, second=0, microsecond=0)

        # Find the next Tuesday
        days_until_tuesday = (1 - now.weekday()) % 7  # 0 = Monday, 1 = Tuesday, etc.
        target_time += datetime.timedelta(days=days_until_tuesday)

        # If it's already past 16:00 UTC today, schedule for next week
        if now >= target_time:
            target_time += datetime.timedelta(weeks=1)

        # Calculate the wait time until the next scheduled run
        wait_time = (target_time - now).total_seconds()
        print(f"Next shrine update scheduled for: {target_time} UTC")

        await asyncio.sleep(wait_time)  # Sleep until the target time

        # Fetch and send shrine details
        shrine_perks = await get_shrine_from_nightlight()
        await send_to_channel(shrine_perks)


# start the bot
bot.run(token)

