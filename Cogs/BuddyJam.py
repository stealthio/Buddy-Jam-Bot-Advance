import os
from ftplib import FTP

from discord.ext import commands
import json

channelAnnouncements = 603164467253215232
channelVoting = 603171016918827008
channelInformation = 603149920345653258
path = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))

# Controls BuddyJam specific commands and behaviours
class BuddyJam(commands.Cog, name="Buddy-Jam"):
    def __init__(self, bot):
        print("Initializing BuddyJam Cog")
        self.bot = bot
        if os.path.exists(os.path.join(path, 'data.json')):
            with open(os.path.join(path, 'data.json')) as f:
                self.data = json.load(f)
        else:
            self.data = {
                "suggestions": [],
                "jam": -1,
                "theme": "",
                "nextTheme": ""
            }

    # Command to suggest a new theme to be added to the theme pool
    @commands.command()
    async def suggest(self, ctx, theme=""):
        """Puts a theme into the voting pool"""
        if theme == "":
            await ctx.send('Usage: ```!suggest "Example Theme"```')
            return
        self.data["suggestions"].append(theme)
        self.data["suggestions"].sort()
        await ctx.message.delete()
        await ctx.send(f"Added {theme} to the theme pool!")

    # Command to check which of the messages in the Voting area has the most Thumbsups
    async def declareWinningTheme(self):
        """Posts the theme with most upvotes into the voting channel"""
        channel = self.bot.get_channel(channelVoting)
        winningMessage = channel.last_message
        winningCount = 0
        async for message in channel.history(limit=200):
            for reaction in message.reactions:
                if reaction.emoji == "👍":
                    if (winningMessage is None) or (winningCount < reaction.count):
                        winningMessage = message
                        winningCount = reaction.count
        if winningMessage == None:
            await channel.send("Winning theme could not be picked")
            return False
        self.data["nextTheme"] = winningMessage.content
        return True

    async def saveFiles(self):
        with open(os.path.join(path, 'data.json'), 'w') as f:
            json.dump(self.data, f)
        conn = FTP(host=os.environ.get('FTPHost'))
        conn.connect()
        conn.login(user=os.environ.get('FTPUser'), passwd=os.environ.get('FTPPass'))
        with open('Cogs/data.json', 'rb') as f:
            conn.storlines('STOR %s' % 'data.json', f)
        conn.quit()

    async def refreshInformation(self):
        await self.saveFiles()
        channel = self.bot.get_channel(channelInformation)
        newText = f"""Buddy-Jam {self.data['jam']}
Current Theme: {self.data['theme']}

The jams start and end with each month. Themes for the monthly voting can be submitted by typing
```
!suggest "My Theme"
```
over in the #bot-stuff area.

Looking for a Buddy? Head over to #find-a-buddy or look at our Crowdforge page for an open team.
Have your project ready for submission? Great! Submit it on the buddy-jam itch.io page, also don't forget
to post it on the #submissions tab!

Relevant links:
Itch.io: https://itch.io/jam/buddy-jam-{self.data['jam']}
Crowdforge: https://crowdforge.io/jams/Buddy-Jam-{self.data['jam']}
"""
        message = None
        async for m in channel.history(limit=200):
            if m.author.bot:
                message = m
                break
        if message is None:
            await channel.send(newText)
        else:
            await message.edit(content=newText)



    async def clearVoting(self):
        channel = self.bot.get_channel(channelVoting)
        async for message in channel.history(limit=200):
            await message.delete()

    # Command to set the current Buddy Jam number
    @commands.command()
    @commands.has_permissions(administrator=True)
    async def setjamno(self, ctx, jam):
        """Set the current Buddy Jam number"""
        if jam == "":
            await ctx.send('Usage: ```!setJamNo 3```')
            return
        self.data['jam'] = int(jam)
        await ctx.send(f"Set current Jam to {jam}")
        await self.refreshInformation()

    # Command to announce that the current jam is almost over, and that the voting for the next one starts
    @commands.command()
    @commands.has_permissions(administrator=True)
    async def announcejam(self, ctx):
        """Writes an announcement regarding voting into the announcement channel"""
        member = ctx.author
        if member != self.bot:
            channel = self.bot.get_channel(channelAnnouncements)
            nextJam = int(self.data['jam'])+1
            await channel.send(f"""@everyone
Buddy Jam {self.data['jam']} is almost over! And we are preparing for our next jam.
It's time to vote for the theme of the Buddy Jam {nextJam}!

Thanks to everyone who entered his/her suggestion to the pool of themes to pick from. I will post each suggestion individually - your vote will be a :thumbsup: (and only :thumbsup:  will be counted)
Feel free to vote :thumbsup: for multiple themes if you like more than one ~
Votings will be closed a few hours before the jam begins and the winner will be announced here and on https://itch.io/jam/buddy-jam-{nextJam}
""")
            await self.clearVoting()
            channel = self.bot.get_channel(channelVoting)
            for theme in self.data["suggestions"]:
                await channel.send(theme)

    # Command to start the next jam
    @commands.command()
    @commands.has_permissions(administrator=True)
    async def startjam(self, ctx):
        """Announces that the next jam has started"""
        member = ctx.author
        if member != self.bot:
            if not await self.declareWinningTheme():
                await ctx.send("Failed to declare winning theme")
                return
            await self.bot.get_channel(channelVoting).purge()
            self.data['jam'] += 1
            channel = self.bot.get_channel(channelAnnouncements)
            await channel.send(f"""@everyone the theme for Buddy Jam {self.data['jam']} is:
{self.data["nextTheme"]}!

Get coding! :buddies:

Also don't forget to suggest themes for our next jam using the !suggest command!
https://itch.io/jam/buddy-jam-{self.data['jam']}
""")
            # Wipe the suggestions list
            self.data["suggestions"] = []
            self.data["theme"] = self.data["nextTheme"]
            self.data["nextTheme"] = ""
            await self.refreshInformation()


def setup(bot):
    bot.add_cog(BuddyJam(bot))
