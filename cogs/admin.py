from contextlib import redirect_stdout
import traceback
import textwrap
import asyncio
import io
import sys

from discord.ext import commands
import discord
import jishaku
# to expose to the eval command
import datetime
from collections import Counter


class Admin(commands.Cog):
    """Admin-only commands that make the bot dynamic."""

    def __init__(self, bot):
        self.bot = bot
        self._last_result = None
        self.sessions = set()

    def cleanup_code(self, content):
        """Automatically removes code blocks from the code."""
        # remove ```py\n```
        if content.startswith('```') and content.endswith('```'):
            return '\n'.join(content.split('\n')[1:-1])

        # remove `foo`
        return content.strip('` \n')

    async def __local_check(self, ctx):
        return await self.bot.is_owner(ctx.author)

    def get_syntax_error(self, e):
        if e.text is None:
            return f'```py\n{e.__class__.__name__}: {e}\n```'
        return f'```py\n{e.text}{"^":>{e.offset}}\n{e.__class__.__name__}: {e}```'


    @commands.command(hidden=True, pass_context=True)
    @commands.is_owner()
    async def load(self, ctx, *, module : str):
        """Loads a module."""
        extension = "cogs." + module
        try:
            self.bot.load_extension(extension)
        except Exception as e:
            await ctx.message.add_reaction('\U0001f6ab')
            await ctx.send('{}: {}'.format(type(e).__name__, e))
        else:
            await ctx.send('<:radithumbsup:544036454867927080>')

    @commands.command(hidden=True, pass_context=True)
    @commands.is_owner()
    async def unload(self, ctx, *, module : str):
        """Unloads a module."""
        extension = "cogs." + module
        try:
            self.bot.unload_extension(extension)
        except Exception as e:
            await ctx.message.add_reaction('\U0001f6ab')
            await ctx.send('{}: {}'.format(type(e).__name__, e))
        else:
            await ctx.send('<:radithumbsup:544036454867927080>')

    @commands.command(name='reload', hidden=True, pass_context=True)
    @commands.is_owner()
    async def _reload(self, ctx, *, module : str):
        """Reloads a module."""
        extension = "cogs." + module
        try:
            self.bot.unload_extension(extension)
            self.bot.load_extension(extension)
        except Exception as e:
            await ctx.message.add_reaction('\U0001f6ab')
            await ctx.send('{}: {}'.format(type(e).__name__, e))
        else:
            await ctx.send('<:radithumbsup:544036454867927080>')



    @commands.command(pass_context=True, hidden=True, name='eval')
    @commands.is_owner()
    async def _eval(self, ctx, *, body: str):
        """Evaluates a code"""

        env = {
            'bot': self.bot,
            'ctx': ctx,
            'channel': ctx.channel,
            'author': ctx.author,
            'guild': ctx.guild,
            'message': ctx.message,
            '_': self._last_result
        }

        env.update(globals())

        body = self.cleanup_code(body)
        stdout = io.StringIO()

        to_compile = f'async def func():\n{textwrap.indent(body, "  ")}'

        try:
            exec(to_compile, env)
        except Exception as e:
            return await ctx.send(f'```py\n{e.__class__.__name__}: {e}\n```')

        func = env['func']
        try:
            with redirect_stdout(stdout):
                ret = await func()
        except Exception as e:
            value = stdout.getvalue()
            emoji = '\N{THUMBS UP SIGN}'
            await ctx.message.add_reaction(emoji)
            await ctx.send(f'```py\n{value}{traceback.format_exc()}\n```')
        else:
            value = stdout.getvalue()
            try:
                emoji = '\N{THUMBS UP SIGN}'
                await ctx.message.add_reaction(emoji)
            except:
                pass

            if ret is None:
                if value:
                    await ctx.send(f'```py\n{value}\n```')
            else:
                self._last_result = ret
                await ctx.send(f'```py\n{value}{ret}\n```')


def setup(bot):
    bot.add_cog(Admin(bot))
