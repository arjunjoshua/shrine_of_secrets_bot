A Discord bot that checks in on Dead By Daylight's Shrine of Secrets every week and posts the new perks to a channel.
Currently available as a custom bot that you can host yourself, but I plan to make it public soon.

## Setting up 
1) Go to the Discord Developer Portal - https://discord.com/developers/applications
2) Create a new application and create a bot within the application. Make sure you copy the token
3) Go to the OAuth2 section and generate an invite link. Use this invite link to add the bot to your server.


## Using the bot
1) Add your desired channel ID and token from Step 2 of setting up as environment variables
2) Host the bot on a computer/server of your choice
3) Schedule the discord.py file to run every Tuesday at 17:00GMT (The shrine resets at 15:00GMT, but the bot pulls data from https://nightlight.gg/shrine) 
