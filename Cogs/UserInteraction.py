import math
import os
from ftplib import FTP

import discord
import json
from discord.ext import commands

channelGeneral = 603142647728701455

path = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))

# Place for non Buddy Jam specific commands
class UserInteraction(commands.Cog, name="General"):
    def __init__(self, bot):
        self.bot = bot

        if os.path.exists(os.path.join(path, 'userdata.json')):
            with open(os.path.join(path, 'userdata.json')) as f:
                self.userdata = json.load(f)
        else:
            self.userdata = {

            }

    async def saveFiles(self):
        with open(os.path.join(path, 'userdata.json'), 'w') as f:
            json.dump(self.userdata, f)

        conn = FTP(host=os.environ.get('FTPHost'))
        conn.connect()
        conn.login(user=os.environ.get('FTPUser'), passwd=os.environ.get('FTPPass'))
        with open('Cogs/userdata.json', 'rb') as f:
            conn.storlines('STOR %s' % 'userdata.json', f)
        conn.quit()

    @commands.command(pass_context=False)
    async def hello(self, ctx, args = [], member: discord.Member = None):
        """Says hello"""
        member = member or ctx.author
        if member != self.bot:
            await ctx.send("Hey there!")

    @commands.command()
    async def buddyscore(self, ctx, param = None, member: discord.Member = None):
        """Posts the users buddy-score"""
        member = member or ctx.author
        if member != self.bot:
            if param is None:
                self.userdata.setdefault(str(member.id), {})
                self.userdata[str(member.id)].setdefault("score", 0)
                self.userdata[str(member.id)].setdefault("level", 0)
                await ctx.send(f"You're level {self.userdata[str(member.id)]['level']} and your Buddy-Score is at {self.userdata[str(member.id)]['score']}!")
            else:
                self.userdata.setdefault(param[2:-1], {})
                self.userdata[param[2:-1]].setdefault("score", 0)
                self.userdata[param[2:-1]].setdefault("level", 0)
                await ctx.send(f"{param} is level {self.userdata[param[2:-1]]['level']} with a Buddy-Score of {self.userdata[param[2:-1]]['score']}!")


    @commands.command()
    @commands.is_owner()
    async def wipechannels(self, ctx):
        """Wipes the server clean of ANY messages"""
        server = ctx.guild
        channels = server.text_channels
        for channel in channels:
            await channel.purge()

    @commands.Cog.listener()
    async def on_member_join(self, member):
        channel = self.bot.get_channel(channelGeneral)
        await channel.send(f"Welcome to the Buddy-Jam {str(member.mention)}!")

    async def give_exp(self, member, amount, channel):
        ud = self.userdata
        ud.setdefault(str(member.id), {})
        ud[str(member.id)].setdefault("score", 0)
        ud[str(member.id)].setdefault("level", 0)
        ud[str(member.id)]["score"] += amount
        if math.sqrt(ud[str(member.id)]["score"]) > ud[str(member.id)]["level"]:
            await self.level_up(member, channel)


    async def level_up(self, member, channel):
        ud = self.userdata
        ud[str(member.id)]["level"] += 1
        guild = member.guild
        r = None
        for role in member.roles:
            if "Level" in role.name:
                await member.remove_roles(role)
        for role in guild.roles:
            if f"Level {ud[str(member.id)]['level']}" == role.name:
                r = role
                break
        if r != None:
            await member.add_roles(r)
        else:
            nr = await guild.create_role(name=f"Level {ud[str(member.id)]['level']}")
            await nr.edit(hoist=True,position=int(ud[str(member.id)]['level']))
            await member.add_roles(nr)
        await channel.send("Congratulations, you leveled up!")

    @commands.Cog.listener()
    async def on_message(self, message):
        if not message.author.bot:
            if message.content.find("thank") != -1 and len(message.mentions) == 1:
                if message.mentions[0] != message.author:
                    await self.give_exp(message.mentions[0], 1, message.channel)
                    await self.saveFiles()
                    await message.channel.send(f"{message.mentions[0].display_name} earned 1 Buddy-Point and now has {self.userdata[str(message.mentions[0].id)]['score']}")


def setup(bot):
    bot.add_cog(UserInteraction(bot))
