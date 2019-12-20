import asyncio
import logging
import json

from discord.ext import commands
import discord

log = logging.getLogger()


def load_teams():
    with open('teams.json') as l:
        return json.load(l)


def load_trnynames():
    with open('tournamentnames.json') as t:
        return json.load(t)

def stream_key(argument):
    return argument

class Scoring(commands.Cog):
    """Commands that display scores from e-sport battles against teams."""

    def __init__(self, bot):
        self.bot = bot



    @commands.command(aliases=['p'], pass_context=True, hidden=False)
    @commands.guild_only()
    @commands.has_permissions(manage_channels=True)
    async def post(self, ctx, battle, homescr, args, awayscr, type: stream_key = None):
        """posts a battle result.
         EXAMPLE: ,post 'scrim or result' 2 'name of clan you scrimed against' 1 'vod(optional for vod reviewing)'"""
        teams = load_teams()
        trnys = load_trnynames()
        guild = ctx.message.guild
        guildidstr = str(guild.id)
        teamguild = teams[guildidstr]
        teamname = teamguild['team']
        trnyname = trnys[battle]['tourny']
        try:
            if type is None:
                if battle == 'scrim':
                    channel = discord.utils.get(guild.channels, name='results') 
                    await channel.send("**Scrim** \n{0} {1}  -  {3} {2}".format(teamname, homescr, args, awayscr))
                    await ctx.trigger_typing()
                    await asyncio.sleep(1)
                    await ctx.send("done")
                    return

                elif battle == 'result':
                    channel = discord.utils.get(guild.channels, name='scrim-scores')
                    await channel.send("**Scrim** \n{0} {1}  -  {3} {2}".format(teamname, homescr, args, awayscr))
                    await ctx.trigger_typing()
                    await asyncio.sleep(1)
                    await ctx.send("done")
                    return

                elif battle == battle:
                    channel = discord.utils.get(guild.channels, name='results')
                    await channel.send("**Tournament**: {4} \n{0} {1}  -  {3} {2}".format(teamname, homescr, args, awayscr, trnyname))
                    await ctx.trigger_typing()
                    await asyncio.sleep(1)
                    await ctx.send("done")
                    return

                elif guildidstr not in teams:
                    await ctx.trigger_typing()
                    await asyncio.sleep(1)
                    await ctx.send("You haven't given me your team's name, type `,writeteam \"YOUR TEAM'S NAME HERE\"` to store it into my database")
                    return

                else:
                    await ctx.trigger_typing()
                    await asyncio.sleep(1)
                    await ctx.send("It seems there's a problem, try again")
                    return


            elif battle == 'scrim':
                channel = discord.utils.get(guild.channels, name='vod-review')
                await channel.send(f"**Scrim** \n{teamname} {homescr}  -  {awayscr} {args} \n{type}")
                await ctx.trigger_typing()
                await asyncio.sleep(1)
                await ctx.send("done")
                return

            elif battle == 'result':
                channel = discord.utils.get(guild.channels, name='vod-review')
                await channel.send(f"**Scrim** \n{teamname} {homescr}  -  {awayscr} {args} \n{type}")
                await ctx.trigger_typing()
                await asyncio.sleep(1)
                await ctx.send("done")
                return

            elif battle == battle:
                channel = discord.utils.get(guild.channels, name='vod-review')
                await channel.send(f"**Tournament**: {trnyname}  \n{teamname} {homescr}  -  {awayscr} {args} \n{type}")
                await ctx.trigger_typing()
                await asyncio.sleep(1)
                await ctx.send("done")
                return
                    
            else:
                await ctx.trigger_typing()
                await asyncio.sleep(1)
                await ctx.send("It seems there's a problem, try again")
                return

            

        except Exception as e:
            await ctx.send("A {0} has occurred, did you make the correct type of channel".format(type(e)))
            log.info(e)

    @commands.command(aliases=['wt'], pass_context=True, hidden=False)
    @commands.guild_only()
    @commands.has_permissions(manage_channels=True)
    async def writeteam(self, ctx, args):
        """I will write the name of your clan to my database
        you must have the permissions to manage channels in order to use this"""
        guild = ctx.message.guild
        teams = load_teams()
        d = teams
        d[guild.id] = {}
        d[guild.id]["team"] = args
        await ctx.trigger_typing()
        with open('teams.json', 'w') as fp:
            json.dump(d, fp, indent=2)
        await asyncio.sleep(1)
        await ctx.send("I have successfully written your team's name into my database")

    @commands.command(pass_context=True, hidden=True)
    @commands.is_owner()
    async def newtrny(self, ctx, tn, args):
        trnys = load_trnynames()
        d = trnys
        d[tn] = {}
        d[tn]['tourny'] = args
        with open('tournamentnames.json', 'w') as fp:
            json.dump(d, fp, indent=2)
        await asyncio.sleep(1)
        await ctx.send("<:radithumbsup:317056486297829386>")

def setup(bot):
    bot.add_cog(Scoring(bot))
