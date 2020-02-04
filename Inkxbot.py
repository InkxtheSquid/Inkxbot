from collections import Counter
import traceback
import datetime
import logging
import asyncio
import copy
import json
import sys
import os
import aiohttp
import jishaku
from jishaku.paginators import PaginatorEmbedInterface, PaginatorInterface
from discord.ext import commands
import discord

#ssh -i "InkxtheSquid.pem" ubuntu@ec2-54-153-19-35.us-west-1.compute.amazonaws.com


description = 'My command list is right here, each is used with a comma' # or a period' (in the future)


# this specifies what extensions to load when the bot starts up
startup_extensions = ["cogs.JustdanceCog",
                      "cogs.splatoon",
                      "cogs.HearthstoneCog",
                      "cogs.destiny",
                      "cogs.BackgroundtaskCog",
                      "cogs.modcog",
                      "cogs.misc",
                      "cogs.dbots",
                      "cogs.ScoresForBattles",
                      "cogs.meta",
                      "cogs.EasterEggs",
                      "cogs.stats",
                      "cogs.admin",
                      "cogs.helpcom"
                      ]


discord_logger = logging.getLogger('discord')
discord_logger.setLevel(logging.CRITICAL)
log = logging.getLogger()
log.setLevel(logging.INFO)
handler = logging.FileHandler(filename='inkxbot.log', encoding='utf-8', mode='w')
log.addHandler(handler)

botfmt = commands.DefaultHelpCommand(show_check_failure=True)

bot = commands.Bot(command_prefix=',', formatter=botfmt)


def load_messages():
    with open('servermessage.json') as m:
        return json.load(m)

@bot.event
async def on_member_join(member):
    guild = member.guild
    messages = load_messages()
    guildstr = str(guild.id)
    if guildstr not in messages: return
    if 'welcome' not in messages[guildstr]: return
    srv = messages[guildstr]
    chanid = srv['channel']
    channel = bot.get_channel(chanid)
    wlc = messages[guildstr]['welcome'].format(member)
    await channel.send(wlc)

@bot.event
async def on_ready():
    print('Inkxbot is logged in and online!')
    print("discord.py version is " + discord.__version__)
    print('--------------------------------')
    if not hasattr(bot, 'uptime'):
        bot.uptime = datetime.datetime.utcnow()


#@bot.event
#async def on_member_ban(guild, user):
    #await asyncio.sleep(5)
    #async for entry in guild.audit_logs(action=discord.AuditLogAction.ban):
        #channel = discord.utils.get(guild.channels, name='banlogs')
        #try:
            #if entry.reason == None:
                #return await channel.send(f"**BAN** \n**User**: {user} \n**Reponsible Mod**: {entry.user}")
            #else:
                #return await channel.send(f"**BAN** \n**User**: {user} \n**Reason**: {entry.reason} \n**Reponsible Mod**: {entry.user}")
        #except:
            #pass

@bot.event
async def on_message(message):
    if message.author.bot:
        return

    await bot.process_commands(message)

help_ = bot.command('help')

@bot.event
async def on_command_error(ctx, error):
    channel = ctx.message.channel
    author  = ctx.message.author
    if isinstance(error, commands.NoPrivateMessage):
        await discord.User.trigger_typing(author)
        await asyncio.sleep(1)
        await author.send("Hey! This command can't be used in DMs.")
    elif isinstance(error, commands.DisabledCommand):
        channel = ctx.message.channel
        await channel.trigger_typing()
        await asyncio.sleep(1)
        await channel.send("I'm Sorry. This command is disabled and it can't be used.")
    elif isinstance(error, commands.CommandInvokeError):
        channel = ctx.message.channel
        print('In {0.command.qualified_name}:'.format(ctx), file=sys.stderr)
        traceback.print_tb(error.original.__traceback__)
        print('{0.__class__.__name__}: {0}'.format(error.original), file=sys.stderr)
        e = discord.Embed(title='Inkx! I have encountered an Error!', color=0xcc6600)
        e.add_field(name='Invoke', value=error)
        e.description = '```py\nIn {0.command.qualified_name}:\n```'.format(ctx) + '{0.__class__.__name__}: {0}'.format(error.original)
        e.timestamp = datetime.datetime.utcnow()
        ch = bot.get_channel(348268312427364374)
        try:
            await ch.send(embed=e)
        except:
            pass

    elif isinstance(error, commands.CommandNotFound):
        log.info(f"\"{ctx.message.guild}\": \"{ctx.message.author}\" used a command thats not in Inkxbot, content is resent here: '{ctx.message.content}'")
    elif isinstance(error, commands.MissingRequiredArgument):
        channel = ctx.message.channel
        await channel.trigger_typing()
        await asyncio.sleep(1)
        await channel.send(f"You've asked me about my `{ctx.command}` command without arguments, use `,help {ctx.command}`")

@bot.event
async def on_error(event, *args, **kwargs):
    e = discord.Embed(title='Inkx! I have encountered an Error!', color=0xcc6600)
    e.add_field(name='Event', value=event)
    e.description = f'```py\n{traceback.format_exc()}\n```'
    e.timestamp = datetime.datetime.utcnow()
    ch = bot.get_channel(348268312427364374)
    try:
        log.info(event)
        await ch.send(embed=e)
    except:
        pass

@bot.event
async def on_resumed():
    print('resumed...')

@bot.command(hidden=True)
@commands.is_owner()
async def do(ctx, times : int, *, command):
    """Repeats a command a specified number of times."""
    msg = copy.copy(ctx.message)
    msg.content = command
    for i in range(times):
        await bot.process_commands(msg)


def load_credentials():
    with open('credentials.json') as f:
        return json.load(f)


if __name__ == '__main__':
    credentials = load_credentials()
    token = credentials['token']
    bot.aio_session = aiohttp.ClientSession(headers={'User-Agent': 'Inkxbot/2.0'},loop=bot.loop)
    bot.client_id = credentials['client_id']
    bot.carbon_key = credentials['carbon_key']
    bot.discordlist_token = credentials['discordlist_token']
    bot.dbots_key = credentials['dbots_key']
    bot.challongekey = credentials['challongekey']
    bot.consumer_key = credentials['consumer_key']
    bot.consumer_secret = credentials['consumer_secret']
    bot.access_token = credentials['access_token']
    bot.access_token_secret = credentials['access_token_secret']
    bot.commands_used = Counter()
    bot.load_extension('jishaku')
    for extension in startup_extensions:
        try:
            bot.load_extension(extension)
        except Exception as e:
            print('Failed to load extension {}\n{}: {}'.format(extension, type(e).__name__, e))
    bot.run(token)
    handlers = log.handlers[:]
    for hdlr in handlers:
        hdlr.close()
        log.removeHandler(hdlr)
