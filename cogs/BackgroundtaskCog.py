import asyncio
import subprocess
import random
import discord
import json

from discord.ext import tasks, commands
from disputils import BotEmbedPaginator
from time import gmtime, strftime


class Backgndtsk(commands.Cog):
    """ a cog that loops certain tasks for the bot, this is also a sister cog for splatoon.py """

    def __init__(self, bot):
        self.bot = bot
        self.splatoon = bot.get_cog("Splatoon")
        self.bgtask.start()

    def cog_unload(self):
        self.bgtask.cancel()


    @tasks.loop(minutes=600)
    async def bgtask(self):
        #statuskeys = load_statuskeys()
        #key = statuskeys[str(random.randrange(4))]
        #satuslist=[discord.ActivityType.playing, discord.ActivityType.listening, discord.ActivityType.watching]
        #await self.bot.change_presence(activity=discord.Activity(type=discord.ActivityType.playing, name=key['status'].format(len(self.bot.guilds))))
        subprocess.Popen('python3 splatnet2statink.py', shell=True)
        #await self.splatoon.splatgear_clock()

    @bgtask.before_loop
    async def before_bgtask(self):
        print('waiting...')
        await self.bot.wait_until_ready()

def setup(bot):
    bot.add_cog(Backgndtsk(bot))
