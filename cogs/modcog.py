import asyncio
import json

from discord.ext import commands
import discord


def load_messages():
    with open('servermessage.json') as m:
        return json.load(m)


class Moderation(commands.Cog):
    """ Moderative Commands to keep the server clean """

    def __init__(self, bot):
        self.bot = bot

    def _role_from_string(self, server, rolename, roles=None):
        if roles is None:
            roles = server.roles
        role = discord.utils.find(lambda r: r.name.lower() == rolename.lower(),roles)

        return role

    @commands.command(name = 'clear', invoke_without_command=True)
    @commands.guild_only()
    @commands.has_permissions(manage_messages=True)
    async def _clear(self, ctx, amount : int = 100):
        """Deletes my messages.
        You must have permissions to manage messages in order to use this"""

        channel = ctx.message.channel
        calls = 0;
        async for msg in channel.history(limit=amount, before=ctx.message):
            if calls and calls % 5 == 0:
                await asyncio.sleep(1.5)

            if msg.author == self.bot.user:
                await msg.delete()
                calls += 1
        await ctx.send('Deleted {0}'.format(calls), delete_after=3.0)

    @commands.command(name = 'clean', invoke_without_command=True, hidden=True)
    @commands.guild_only()
    @commands.is_owner()
    async def clean(self, ctx, amount : int = 100):
        channel = ctx.message.channel
        calls = 0;
        async for msg in channel.history(limit=amount, before=ctx.message):
            if calls and calls % 5 == 0:
                await asyncio.sleep(1.5)

            if msg.author == self.bot.user:
                await msg.delete()
                calls += 1
        await ctx.send('Deleted {0}'.format(calls), delete_after=3.0)


    @commands.command(invoke_without_command=True)
    @commands.guild_only()
    @commands.has_permissions(manage_messages=True)
    async def purge(self, ctx, amount : int = 5):
        """Deletes specified number of messages.
        You must have permissions to manage messages in order to use this"""
        channel = ctx.message.channel
        message = ctx.message
        deleted = await channel.purge(limit=amount, before=message)
        await ctx.send('Deleted {}'.format(len(deleted)), delete_after=3.0)

    @commands.command(pass_context=True)
    @commands.guild_only()
    @commands.has_permissions(manage_roles=True)
    async def give(self, ctx, rolename, user: discord.Member=None):
        """Gives a role to a user, defaults to author
        Role name must be in quotes if there are spaces.
        You must have permissions to manage roles in order to use this"""
        if user is None:
            user = ctx.message.author

        role = self._role_from_string(ctx.guild, rolename)

        if role is None:
            await ctx.trigger_typing()
            await asyncio.sleep(1)
            await ctx.send('That role cannot be found.')
            return

        if not ctx.channel.permissions_for(ctx.guild.me).manage_roles:
            await ctx.trigger_typing()
            await asyncio.sleep(1)
            await ctx.send("I don't have permissions to manage roles!")
            return

        await ctx.trigger_typing()
        await self.bot.add_roles(user, role)
        await asyncio.sleep(1)
        await ctx.send('I have given the {} role to {}'.format(role.name, user.name))

    @commands.command(pass_context=True, name = 'remove')
    @commands.guild_only()
    @commands.has_permissions(manage_roles=True)
    async def _remove(self, ctx, rolename, user: discord.Member=None):
        """Removes a role from user, defaults to author
        Role name must be in quotes if there are spaces.
        You must have permissions to manage roles in order to use this"""
        role = self._role_from_string(ctx.guild, rolename)
        if role is None:
            await ctx.trigger_typing()
            await asyncio.sleep(1)
            await ctx.send("Role not found.")
            return

        if user is None:
            user = ctx.author

        if role in user.roles:
            try:
                await ctx.trigger_typing()
                await self.bot.remove_roles(user, role)
                await asyncio.sleep(1)
                await ctx.send("Role successfully removed.")
            except discord.Forbidden:
                await ctx.trigger_typing()
                await asyncio.sleep(1)
                await ctx.send("I don't have permissions to manage roles!")
        else:
            await ctx.trigger_typing()
            await asyncio.sleep(1)
            await ctx.send("User does not have that role.")


    async def on_member_remove(self, member):
        guild = member.guild
        messages = load_messages()
        guildstr = str(guild.id)
        if guildstr not in messages: return
        if 'leave' not in messages[guildstr]: return
        srv = messages[guildstr]
        chanid = srv['channel']
        channel = self.bot.get_channel(chanid)
        wlc = messages[guildstr]['leave'].format(member)
        await channel.send(wlc)

    async def on_member_ban(guild, user):
        await asyncio.sleep(5)
        try:
            async for entry in guild.audit_logs(action=discord.AuditLogAction.ban):
                channel = guild.channels.get(name='banlogs')
                if entry.reason == None:
                    return await channel.send(f"**BAN** \n**User**: {user} \n**Responsible Mod**: {entry.user}")
                else:
                    return await channel.send(f"**BAN** \n**User**: {user} \n**Reason**: {entry.reason} \n**Responsible Mod**: {entry.user}")
        except (discord.errors.Forbidden, AttributeError):
            pass

def setup(bot):
    bot.add_cog(Moderation(bot))
