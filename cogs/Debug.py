# ----------{ Imports requirements }----------
import discord
from discord.ext import commands


# ----------{ Debug class }----------
class Debug(commands.Cog):

    def __init__(self, client):
        self.client = client

    # ----------{ Methods }----------
    '''< Ping call >
    Check if bot responds to your first call.
    '''
    @commands.command(name="ping", description="pong")
    @commands.has_permissions(administrator=True)
    async def ping(self, ctx):
        print("pong")
        await ctx.send("pong")

    ''' < Get last messages >
    Send last 100 messages to console.
    '''
    @commands.command()
    @commands.has_permissions(administrator=True)
    async def get_last_messages(self, ctx):
        print("---------------------------------------------------")
        print("Getting last 100 messages")
        _channel = ctx.channel
        message_list = await _channel.history(limit=100).flatten()

        await ctx.message.delete()

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
def setup(client):
    client.add_cog(Debug(client))
