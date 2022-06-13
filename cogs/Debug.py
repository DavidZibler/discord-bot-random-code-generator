# ----------{ Imports requirements }----------
import discord
from discord.ext import commands
from discord.commands import slash_command


# ----------{ Debug class }----------
class Debug(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    # ----------{ Methods }----------
    '''< Ping call >
    Check if bot responds to your first call.
    '''
    @slash_command(name="ping", description="pong")
    @commands.has_permissions(administrator=True)
    async def ping(self, ctx):
        print("pong")
        await ctx.respond("pong", delete_after=3)

    ''' < Get last messages >
    Send last 100 messages to console.
    '''
    @slash_command(name="get_last_messages", description="Get last 100 messages in active channel!")
    @commands.has_permissions(administrator=True)
    async def get_last_messages(self, ctx):
        print("---------------------------------------------------")
        print("Getting last 100 messages")
        _channel = ctx.channel
        message_list = await _channel.history(limit=100).flatten()

        await ctx.respond('Response', delete_after=0)

        print("---------------------------------------------------")
        print("Messages->")
        for i in message_list:
            print(i.content)
        print("Finished!")
        print("---------------------------------------------------")

    ''' < Clear channel >
    Clear last 15 messages in a channel.
    Be careful with using this command (Just for testing)!!!
    '''
    @commands.command()
    @commands.has_permissions(administrator=True)
    async def clear_channel(self, ctx):
        print("clearing ...")
        _channel = ctx.channel
        message_list = await _channel.history(limit=15).flatten()

        for i in message_list:
            await i.delete()

        print("All messages cleared!")

    # ----------{ Error handling }----------
    @ping.error
    async def ping_error(self, ctx, error):
        if isinstance(error, commands.MissingPermissions):
            await ctx.send('Missing administrator permissions.', delete_after=2)

    @get_last_messages.error
    async def get_last_messages_error(self, ctx, error):
        if isinstance(error, commands.MissingPermissions):
            await ctx.send('Missing administrator permissions.', delete_after=2)

    @clear_channel.error
    async def clear_channel_error(self, ctx, error):
        if isinstance(error, commands.MissingPermissions):
            await ctx.send('Missing administrator permissions.', delete_after=2)


# ----------{ Cog export }----------
def setup(bot):
    bot.add_cog(Debug(bot))
