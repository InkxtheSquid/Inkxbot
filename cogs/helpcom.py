from discord.ext import commands
import discord

from jishaku.paginators import PaginatorEmbedInterfaceForHelpCom, PaginatorInterface

class InkxHelp(commands.DefaultHelpCommand):
    """
    A subclass of :class:`commands.MinimalHelpCommand` that uses a PaginatorEmbedInterface for pages.
    """
    def __init__(self, **options):
        self.no_category=""
        paginator = options.pop('paginator', commands.Paginator(prefix=None, suffix=None, max_size=450))
        super().__init__(paginator=paginator, help_attrs=dict(hidden=True), no_category="", show_check_failure=True, indent=5, **options)
    
    async def send_pages(self):
        destination = self.get_destination()

        interface = PaginatorEmbedInterfaceForHelpCom(self.context.bot, self.paginator, owner=self.context.author)
        try:
            await interface.send_to(destination)
        except Exception as e:
            await destination.send("I don't have permission to embed links, I need to embed links to send you help.".format(type(e)))
def setup(bot):
    bot.help_command = InkxHelp()