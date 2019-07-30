from ftplib import FTP

from discord.ext import commands
import os


def writeline(data):
     file.write(data)
     file.write(os.linesep)

conn = FTP(host=os.environ.get('FTPHost'))
conn.connect()
conn.login(user=os.environ.get('FTPUser'),passwd=os.environ.get('FTPPass'))

file = open('Cogs/data.json', 'w+')
conn.retrlines('RETR data.json', writeline)
file.close()

file = open('Cogs/userdata.json', 'w+')
conn.retrlines('RETR userdata.json', writeline)
file.close()

conn.close()

# Set the prefix for the bot to listen for commands
bot = commands.Bot(command_prefix='!')
data = {}

# Writes a short statement into the log that the bot has started
@bot.event
async def on_ready():
    print('We have logged in as {0.user}'.format(bot))
    if os.environ.get('debug') == "1":
        await bot.logout()



# Load the different modules from the Cogs folder
bot.load_extension("Cogs.UserInteraction")
bot.load_extension("Cogs.BuddyJam")

# Starts the bot
bot.run(os.environ.get('token'))