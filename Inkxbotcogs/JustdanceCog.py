from discord.ext import commands
from .utils import config, checks
import asyncio, aiohttp
from urllib.parse import quote as urlquote
from collections import namedtuple


class Just_Dance:
    def __init__(self, bot):
        self.bot = bot     
         
    @commands.command()
    async def justdancewiki(self, title):
        """Returns a justdancewikia page. For spaces use underscores."""
        url = 'http://justdance.wikia.com/wiki/' + urlquote(title)

        async with aiohttp.get(url) as resp:
            if resp.status == 404:
                await self.bot.say('Could not find your page. Try a search:\n{0.url}'.format(resp))
            elif resp.status == 200:
                await self.bot.say(resp.url)
            elif resp.status == 502:
                await self.bot.say('Seems like the Just Dance Wiki is taking too long to respond. Try again later.')
            else:
                await self.bot.say('An error has occurred of status code {0.status} happened. Tell Inkx.'.format(resp))
     
    @commands.command()
    async def sgmd(self):
        """I will post a photo of She's Got Me Dancing"""
        await self.bot.say('http://vignette1.wikia.nocookie.net/justdance/images/d/de/Gotmedancing_coach_1_big.png/revision/latest?cb=20150123085617')

def setup(bot):
    bot.add_cog(Just_Dance(bot))
