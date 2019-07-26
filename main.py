from discord.ext import commands
import os

# Set the prefix for the bot to listen for commands
bot = commands.Bot(command_prefix='!')
data = {}

# Writes a short statement into the log that the bot has started
@bot.event
async def on_ready():
    print('We have logged in as {0.user}'.format(bot))
    if os.environ.get('debug') == 1:
        await bot.logout()



# Load the different modules from the Cogs folder
bot.load_extension("Cogs.UserInteraction")
bot.load_extension("Cogs.BuddyJam")

# Starts the bot
bot.run(os.environ.get('token'))