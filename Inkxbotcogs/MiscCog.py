from discord.ext import commands
import asyncio
import discord

class Misc:
    """ Miscellaneous commands. """

    def __init__(self, bot):
        self.bot = bot

    @commands.command(hidden=True)
    async def coreyrage(self, ctx):
        """Corey's rage"""
        await ctx.trigger_typing()
        await asyncio.sleep(8)
        await ctx.send("I HATE EVERYTHING ARE YOU KIDDING ME RAAAAAAAAAAAAAAAAAAAGHHHHHHHHHHHHHHHHHHHHHHHFEIFYEDBJ")

    @commands.command(name="break")
    async def _break(self, ctx):
        """Take a break"""
        await ctx.trigger_typing()
        await asyncio.sleep(8)
        await ctx.send("It's time to take a break. Or you'll probably never stop.")


    @commands.command(hidden=True)
    async def ctkcryo(self, ctx):
        """cryo"""
        await ctx.trigger_typing()
        await asyncio.sleep(8)
        await ctx.send("PEW PEW PEW! PEW PEW PEW PEW PEW! SHUT THE FUCK UP")

    @commands.command(hidden=True)
    async def coreygasm(self, ctx):
        """coreygasm"""
        await ctx.trigger_typing()
        await asyncio.sleep(8)
        await ctx.send("OMGOMGOMGOMGOMGFDEJWDVEJFVEJKVJEJR")

    @commands.command(hidden=True)
    async def ctkmoment(self, ctx):
        """ctkmoment"""
        await ctx.trigger_typing()
        await asyncio.sleep(8)
        await ctx.send("OH THAT CTK *laugh track*")

    @commands.command(hidden=True)
    async def zhuli(self, ctx):
        await ctx.trigger_typing()
        await asyncio.sleep(8)
        await ctx.send("Zhu Li, do the thing!")

    @commands.command(hidden=True)
    async def beck(self, ctx):
        await ctx.trigger_typing()
        await asyncio.sleep(8)
        await ctx.send("That's more like it!")

    @commands.command()
    async def slap(self, ctx, args):
        """Slap someone!"""
        user = ctx.message.author.mention
        if args == "<@245648163837444097>":
            await ctx.trigger_typing()
            await asyncio.sleep(1)
            await ctx.send("Don't think about slapping me \U0001f621")
        elif args == " <@245648163837444097> ":
            await ctx.trigger_typing()
            await asyncio.sleep(1)
            await ctx.send("Don't think about slapping me \U0001f621")
        elif args == ctx.message.author.mention:
            await ctx.trigger_typing()
            await asyncio.sleep(1)
            await ctx.send("Way to go, you just slaped yourself.")
        elif args == ctx.message.author.name:
            await ctx.trigger_typing()
            await asyncio.sleep(1)
            await ctx.send("Way to go, you just slaped yourself.")
        elif args == "@everyone":
            await ctx.trigger_typing()
            await asyncio.sleep(1)
            await ctx.send("That is totaly breaking the rules...")
        elif args == "@here":
            await ctx.trigger_typing()
            await asyncio.sleep(1)
            await ctx.send("That is totaly breaking the rules...")
        elif args == "/@everyone":
            await ctx.trigger_typing()
            await asyncio.sleep(1)
            await ctx.send("That is totaly breaking the rules...")
        elif args == "/@here":
            await ctx.trigger_typing()
            await asyncio.sleep(1)
            await ctx.send("That is totaly breaking the rules...")
        elif args == "\@everyone":
            await ctx.trigger_typing()
            await asyncio.sleep(1)
            await ctx.send("That is totaly breaking the rules...")
        elif args == "\@here":
            await ctx.trigger_typing()
            await asyncio.sleep(1)
            await ctx.send("That is totaly breaking the rules...")
        else:
            await ctx.trigger_typing()
            await asyncio.sleep(1)
            await ctx.send('**SMACK!** *{0} slaps {1}*'.format(user, args))

    @commands.command()
    async def add(self, ctx):
        """I will give you a link so I can be added to a server"""
        await ctx.trigger_typing()
        await asyncio.sleep(1)
        await ctx.author.send('You want to add me to a server? Ok! Add me to a server with this link: <https://discordapp.com/oauth2/authorize?client_id=245648163837444097&scope=bot&permissions=268437512>')
        if isinstance(ctx.message.channel, discord.TextChannel):
            await ctx.send("{} check your dms".format(ctx.message.author.mention))
        else:
            None

    @commands.command(hidden=True)
    async def typing(self, ctx):
        """A little test command to test to see if I'm typing"""
        await ctx.trigger_typing()
        await asyncio.sleep(8)
        await ctx.send("There, I'm done typing for you")

    @commands.command(hidden=True, pass_context=True)
    @commands.is_owner()
    async def say(self, ctx, chanid, args):
        """well..."""
        chan = int(chanid)
        channel = self.bot.get_channel(chan)
        await channel.trigger_typing()
        await asyncio.sleep(1)
        await channel.send(args)
        await ctx.send("\U0001f44d")

    @commands.command(hidden=True, pass_context=True)
    @commands.is_owner()
    async def send(self, ctx, args):
        """..."""
        channel = self.bot.get_channel(318533496060641280)
        await channel.trigger_typing()
        await asyncio.sleep(1)
        await channel.send(args)
        await ctx.send("\U0001f44d")

    @commands.command(pass_context=True, hidden=True)
    @commands.is_owner()
    async def switchfc(self, ctx):
        """Inkx's Switch FC"""
        await ctx.trigger_typing()
        await asyncio.sleep(1)
        await ctx.send("Here's my creator's Switch FC! \nSW-0631-3294-7718")

def setup(bot):
    bot.add_cog(Misc(bot))
