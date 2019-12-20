from collections import Counter
import datetime
import asyncio
import logging

from discord.ext import commands
import discord
import psutil

log = logging.getLogger()

class Stats(commands.Cog):
    """Bot usage statistics."""

    def __init__(self, bot):
        self.bot = bot

    async def on_command(self, ctx):
        self.bot.commands_used =+ 1
        message = ctx.message
        destination = None
        if isinstance(message.channel, discord.abc.PrivateChannel):
            destination = 'DM'
        else:
            destination = '#{0.channel.name} ({0.guild.name})'.format(message)

        log.info('{0.created_at}: {0.author.name} in {1}: {0.content}'.format(message, destination))

    async def on_socket_response(self, msg):
        self.bot.socket_stats[msg.get('t')] += 1

    @commands.command(hidden=True)
    @commands.is_owner()
    async def commandstats(self, ctx):
        p = commands.Paginator()
        counter = self.bot.commands_used
        width = len(max(counter, key=len))
        total = sum(counter.values())

        fmt = '{0:<{width}}: {1}'
        p.add_line(fmt.format('Total', total, width=width))
        for key, count in counter.most_common():
            p.add_line(fmt.format(key, count, width=width))

        for page in p.pages:
            await self.bot.say(page)

    def get_bot_uptime(self, *, brief=False):
        now = datetime.datetime.utcnow()
        delta = now - self.bot.uptime
        hours, remainder = divmod(int(delta.total_seconds()), 3600)
        minutes, seconds = divmod(remainder, 60)
        days, hours = divmod(hours, 24)

        if not brief:
            if days:
                fmt = '{d} days, {h} hours, {m} minutes, and {s} seconds'
            else:
                fmt = '{h} hours, {m} minutes, and {s} seconds'
        else:
            fmt = '{h}h {m}m {s}s'
            if days:
                fmt = '{d}d ' + fmt

        return fmt.format(d=days, h=hours, m=minutes, s=seconds)


    @commands.command(hidden=True)
    @commands.is_owner()
    async def uptime(self, ctx):
        """Tells you how long I have been up for."""
        await ctx.send('Uptime: **{}**'.format(self.get_bot_uptime()))


    @commands.command(aliases=['inkxbot', 'Inkxbot'])
    async def about(self, ctx):
        """Tells you information about myself."""

        embed = discord.Embed(description='Check https://inkxbot.github.io/ for a little documentation!')
        embed.colour = 0xff4500 # OrangeRed

        try:
            owner = self._owner
        except AttributeError:
            owner = self._owner = await self.bot.fetch_user('122043518544904192')

        embed.set_author(name=str(owner), icon_url=owner.avatar_url)

        # statistics
        total_members = sum(len(s.members) for s in self.bot.guilds)
        total_online  = sum(1 for m in self.bot.get_all_members() if m.status != discord.Status.offline)
        unique_members = set(self.bot.get_all_members())
        unique_online = sum(1 for m in unique_members if m.status != discord.Status.offline)

        members = '%s total\n%s online\n%s unique\n%s unique online' % (total_members, total_online, len(unique_members), unique_online)
        embed.add_field(name='Members', value=members)
        embed.add_field(name='Uptime', value=self.get_bot_uptime(brief=True))
        embed.set_footer(text='Made via discord.py, pfp: jenthenightmariontte', icon_url='http://i.imgur.com/5BFecvA.png')
        embed.timestamp = self.bot.uptime

        embed.add_field(name='Servers', value=len(self.bot.guilds))
        embed.add_field(name='Commands Run', value=sum(self.bot.commands_used.values()))

        memory_usage = psutil.Process().memory_full_info().uss / 1024**2
        embed.add_field(name='Memory Usage', value='{:.2f} MiB'.format(memory_usage))

        await ctx.trigger_typing()
        await asyncio.sleep(1)
        await ctx.send(embed=embed)



def setup(bot):
    bot.commands_used = Counter()
    bot.socket_stats = Counter()
    bot.add_cog(Stats(bot))