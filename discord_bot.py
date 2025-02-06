#!/usr/bin/env python3
import discord
import datetime
from dotenv import load_dotenv
import os
from discord.ext import commands
import asyncio

load_dotenv()
token = os.getenv("DISCORD_TOKEN")
update_frequency = os.getenv("SHRINE_UPDATE_FREQUENCY")

# read channel ids from the channel_ids.txt file
with open("channel_ids.txt", "r") as f:
    shrine_channel_ids = [int(line.strip()) for line in f]

# Create a discord client
intents = discord.Intents.default()
intents.messages = True
intents.message_content = True
bot = commands.Bot(command_prefix='!', intents=intents)


@bot.event
async def on_ready():
    print(f'We have logged in as {bot.user}')

    # schedule the weekly shrine update
    if not hasattr(bot, 'shrine_update_task'):
        bot.shrine_update_task = bot.loop.create_task(schedule_weekly_shrine())

    # # get the shrine of secrets
    # shrine_perks = get_shrine_from_nightlight()
    #
    # # send the shrine of secrets to the channel
    # await send_to_channel(shrine_perks)


@bot.command()
async def shrine(ctx: commands.Context):
    shrine_perks = []
    # get the shrine of secrets from shrine.txt
    with open("shrine.txt", "r") as f:
        shrine_perks = [line.strip() for line in f]

    if len(shrine_perks) == 0:
        return

    # send the shrine of secrets to the channel
    await send_shrine_to_channel(shrine_perks, [ctx.channel.id])


@bot.command()
async def subscribe_to_shrine(ctx: commands.Context):
    # save the channel id to the .txt file
    shrine_channel_ids.append(ctx.channel.id)

    with open("channel_ids.txt", "w") as f:
        for channel_id in shrine_channel_ids:
            f.write(f"{channel_id}\n")

    await ctx.send("You have been subscribed to shrine updates.")


@bot.command()
async def unsubscribe_from_shrine(ctx: commands.Context):
    try:
        # Remove the current channel ID if it exists
        if ctx.channel.id in shrine_channel_ids:
            shrine_channel_ids.remove(ctx.channel.id)

            # Write updated IDs back to the file
            with open("channel_ids.txt", "w") as f:
                for channel_id in shrine_channel_ids:
                    f.write(f"{channel_id}\n")

            await ctx.send("You have been unsubscribed from shrine updates.")
        else:
            await ctx.send("You are not subscribed to shrine updates.")

    except Exception as e:
        print(e)
        await ctx.send("An error occurred while trying to unsubscribe from shrine updates. Please contact the "
                       "developer.")


# send data to a channel
async def send_shrine_to_channel(shrine_of_secrets, channel_ids=None):
    if channel_ids is None:
        channel_ids = shrine_channel_ids
    date = datetime.datetime.now()

    if update_frequency == "daily":
        # if the time is past 15:00 UTC, update the shrine for the next day
        if date.hour >= 15:
            date += datetime.timedelta(days=1)
    else:
        # Get the next Tuesday's date
        while date.weekday() != 1:
            date += datetime.timedelta(days=1)

    shrine_refresh_date = date.strftime("%b %d, %Y") + " 15:00 UTC"

    formatted_shrine = (f"The Shrine of Secrets currently contains the following perks:\n\n" + "\n".join(shrine_of_secrets)
                        + f"\n\nAvailable until {shrine_refresh_date}")

    for channel_id in channel_ids:
        channel = bot.get_channel(channel_id)
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

        # read the shrine from the file
        shrine_perks = []
        with open("shrine.txt", "r") as f:
            shrine_perks = [line.strip() for line in f]

        # send the shrine to the channel
        if len(shrine_perks) > 0:
            await send_shrine_to_channel(shrine_perks)


# start the bot
bot.run(token)


