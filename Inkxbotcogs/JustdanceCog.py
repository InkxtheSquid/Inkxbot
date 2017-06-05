from discord.ext import commands
from .utils import config, checks
import asyncio, aiohttp
from urllib.parse import quote as urlquote
from collections import namedtuple


class Just_Dance:
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def justdancewiki(self, ctx, args):
        """Returns a justdancewiki page: ,justdancewiki "I Love It" """
        url = 'http://justdance.wikia.com/wiki/' + urlquote(args)
        async with aiohttp.get(url) as resp:
            if resp.status == 404:
                await ctx.send('Could not find your page. Try a search:\n<{0.url}>'.format(resp))
            elif resp.status == 200:
                await ctx.send(resp.url)
            elif resp.status == 502:
                await ctx.send('Seems like the Just Dance Wiki is taking too long to respond. Try again later.')
            else:
                await ctx.send('An error has occurred of a status code {0.status} happened. Tell Inkx.'.format(resp))

    @commands.command()
    async def sgmd(self, ctx):
        """I will post a photo of She's Got Me Dancing"""
        await ctx.trigger_typing()
        await asyncio.sleep(1)
        await ctx.send('http://vignette1.wikia.nocookie.net/justdance/images/d/de/Gotmedancing_coach_1_big.png/revision/latest?cb=20150123085617')

def setup(bot):
    bot.add_cog(Just_Dance(bot))
