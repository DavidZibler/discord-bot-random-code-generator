# ----------{ Imports requirements }----------
import discord
from discord.ext import commands
from discord.ui import Button, View
from discord.utils import get
import random
import string

# ----------{ Global variables }----------
codeLength = 8
minRequiredRole = "Verified"
generatorRole = "code-generated"
# adminCodeChannel = 984938847207034941

adminCodeChannel = 983717228098760794


# ----------{ Global methods }----------
def generate_random_string(chars=string.ascii_uppercase + string.ascii_lowercase + string.digits, length=codeLength):
    return ''.join(random.choice(chars) for _ in range(length))


# ----------{ Admin class }----------
class Admin(commands.Cog):

    def __init__(self, client):
        self.client = client

    # ----------{ Methods }----------
    ''' < Setup >
    Setup embed message with buttons.
    '''
    @commands.command()
    @commands.has_permissions(administrator=True)
    async def setup(self, ctx):
        # Delete used /command
        await ctx.message.delete()

        # Create embed message
        embed = discord.Embed(
            title="📨 Private code generator",
            description="Generate your private code. You will receive a message! \n"
                        "Resend your code, if you lost your code.",
            color=discord.Color.blue()
        )

        # Generate button & view
        generate_button = GenerateCodeButton(label="Generate code")
        resend_button = ResendCodeButton(label="Resend code")

        view = View()
        view.add_item(generate_button)
        view.add_item(resend_button)

        # Send message
        await ctx.message.channel.send(embed=embed, view=view)

    # ----------{ Error handling }----------
    @setup.error
    async def setup_error(self, ctx, error):
        if isinstance(error, commands.MissingPermissions):
            await ctx.send('Missing administrator permissions.', delete_after=2)


# ----------{ Button classes }----------
class GenerateCodeButton(Button):
    def __init__(self, label):
        super().__init__(label=label, style=discord.ButtonStyle.green, emoji="✅")

    async def callback(self, interaction):
        # Variables
        member = interaction.user
        role = get(interaction.message.guild.roles, name=generatorRole)
        min_role = get(interaction.message.guild.roles, name=minRequiredRole)

        # Check if a user already has a role
        if min_role in member.roles:
            if role in member.roles:
                await interaction.response.send_message("**You already generated your code!**", delete_after=3)
            else:
                # Create code
                random_code = generate_random_string()
                _privateChannel = interaction.client.get_channel(adminCodeChannel)

                await _privateChannel.send(str(member.mention) + " " + "@" + str(member) + " " + random_code)

                # Create private embed message
                embed = discord.Embed(
                    title="🚨 **Your private code** 🚨",
                    description="**Rules:**\n"
                                "❗ Keep this code private and dont share it with anyone.\n"
                                "\n"
                                "**When/where to use this code:**\n"
                                "1️⃣ Add this code into your twitter retweet message.\n"
                                "2️⃣ Add this code into instagram image share.\n"
                                "\n"
                                "**Your code:**\n"
                                "⏩ " + random_code,
                    color=discord.Color.blue()
                )

                # Send embed
                await member.send(embed=embed)

                # Add role
                await member.add_roles(role)

                await interaction.response.send_message("**Code generated!**", delete_after=3)
        else:
            warning_message = "**You are not verified or miss minimum required role! -> **" + str(minRequiredRole)

            await interaction.response.send_message(warning_message, delete_after=3)


class ResendCodeButton(Button):
    def __init__(self, label):
        super().__init__(label=label, style=discord.ButtonStyle.primary, emoji="🔁")

    async def callback(self, interaction):
        # Variables
        member = interaction.user
        role = get(interaction.message.guild.roles, name=generatorRole)
        minimum_role = get(interaction.message.guild.roles, name=minRequiredRole)

        # Check if member has roles
        if minimum_role in member.roles:
            if role in member.roles:
                # Get channel & messages
                _privateChannel = interaction.client.get_channel(adminCodeChannel)
                message_list = await _privateChannel.history().flatten()

                member_id = int(member.id)

                member_found = False

                for i in message_list:
                    # Get all ids
                    name_id = int(str(str(i.content).split()[0]).replace("<", "").replace(">", "").replace("@", ""))
                    random_code_string = str(str(i.content).split()[2])

                    if name_id == member_id:
                        # Create private embed message
                        embed = discord.Embed(
                            title="🚨 **This is your code** 🚨",
                            description="**Rules:**\n"
                                        "❗ Keep this code private and dont share it with anyone.\n"
                                        "\n"
                                        "**When/where to use this code:**\n"
                                        "1️⃣ Add this code into your twitter retweet message.\n"
                                        "2️⃣ Add this code into instagram image share.\n"
                                        "\n"
                                        "**Your code:**\n"
                                        "⏩ " + random_code_string,
                            color=discord.Color.blue()
                        )

                        member_found = True

                        # Send embed
                        await member.send(embed=embed)

                # Check if member was found
                if member_found:
                    await interaction.response.send_message("**Check your private message for your code.**",
                                                            delete_after=3)
                else:
                    await interaction.response.send_message("**Code not found, write an admin or moderator.**",
                                                            delete_after=3)
            else:
                await interaction.response.send_message("**You have not generated your code yet!**",
                                                        delete_after=3)
        else:
            warning_message = "**You are not verified or miss minimum required role! -> **" + str(minimum_role)
            await interaction.response.send_message(warning_message,
                                                    delete_after=3)


# ----------{ Cog export }----------
def setup(client):
    client.add_cog(Admin(client))
