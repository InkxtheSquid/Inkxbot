import asyncio
import subprocess
from discord.ext import commands
import discord


class Backgndtsk(commands.Cog):
    """ a cog that loops certain tasks for the bot, this is also a sister cog for splatoon.py """

    def __init__(self, bot):
        self.bot = bot
        self.taskupdater = bot.loop.create_task(self.background_task())

    def __unload(self):
        self.taskupdater.cancel()

    async def background_task(self):
        # this background task is for changing the playing status
        await self.bot.wait_until_ready()
        await asyncio.sleep(10)
        while not self.bot.is_closed():
            subprocess.Popen('python3.6 splatnet2_cookiepull.py', shell=True)
            await self.bot.change_presence(activity=discord.Game(name='https://inkxbot.github.io'))
            await asyncio.sleep(60)
            await self.bot.change_presence(activity=discord.Activity(type=discord.ActivityType.listening, name='{} servers | ,help'.format(len(self.bot.guilds))))
            await asyncio.sleep(60)
            await self.bot.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name=',help for info'))
            await asyncio.sleep(60)
            await self.bot.change_presence(activity=discord.Game(name='give bots custom status'))
            await asyncio.sleep(60)

def setup(bot):
    bot.add_cog(Backgndtsk(bot))
