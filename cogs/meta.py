import unicodedata
import discord
from discord.ext import commands
from io import BytesIO
from PIL import Image

from jishaku.functools import executor_function

@executor_function
def color_processing(color: discord.Color):
    with Image.new('RGB', (64, 64), color.to_rgb()) as im:
        buff = BytesIO()
        im.save(buff, 'png')

    buff.seek(0)
    return buff



    

class Meta(commands.Cog):
    """Commands for utilities related to Discord or about myself."""

    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def color(self, ctx, color: discord.Color=None):
        """sends an image of the color of your highest role.
        """
        color = color or ctx.author.color
        buff = await color_processing(color=color)
        await ctx.send(file=discord.File(fp=buff, filename='color.png'))

    @commands.command()
    async def charinfo(self, ctx, *, characters: str):
        """Shows you information about a number of characters in emojis.
        Only up to 15 characters at a time.
        """

        if len(characters) > 15:
            await ctx.send('Too many characters ({}/15)'.format(len(characters)))
            return

        fmt = '`\\U{0:>08}`: {1} - {2} \N{EM DASH} <http://www.fileformat.info/info/unicode/char/{0}>'

        def to_string(c):
            digit = format(ord(c), 'x')
            name = unicodedata.name(c, 'Name not found.')
            return fmt.format(digit, name, c)

        await ctx.send('\n'.join(map(to_string, characters)))

        #I'll work on this later
    #@commands.command()
    #async def source(self, command : str = None):
        #"""Displays my full source code or for a specific command."""
        #source_url = 'https://github.com/InkxtheSquid/Inkxbot'
        #if command is None:
            #await self.bot.say(source_url)
            #return

        #code_path = command.split('.')
        #obj = self.bot
        #for cmd in code_path:
            #try:
                #obj = obj.get_command(cmd)
                #if obj is None:
                    #await self.bot.say('Could not find the command ' + cmd)
                    #return
            #except AttributeError:
                #await self.bot.say('{0.name} command has no subcommands'.format(obj))
                #return
        ## since we found the command we're looking for, presumably anyway, let's
        ## try to access the code itself
        #src = obj.callback.__code__
        #lines, firstlineno = inspect.getsourcelines(src)
        #if not obj.callback.__module__.startswith('discord'):
            ## not a built-in command
            #location = os.path.relpath(src.co_filename).replace('\\', '/')
        #else:
            #location = obj.callback.__module__.replace('.', '/') + '.py'
            #source_url = 'https://github.com/Rapptz/discord.py'

        #final_url = '<{}/blob/master/{}#L{}-L{}>'.format(source_url, location, firstlineno, firstlineno + len(lines) - 1)
        #await self.bot.say(final_url)

    @commands.command(rest_is_raw=True, hidden=True)
    @commands.is_owner()
    async def echo(self, ctx, *, content):
        await ctx.send(content)

def setup(bot):
    bot.add_cog(Meta(bot))