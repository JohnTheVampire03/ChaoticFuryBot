import discord
from discord.ext import commands
import platform
import cogs._json


class General(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print("General Cog has been loaded\n-----")

    @commands.command()
    async def stats(self, ctx):
        """
        A useful command that displays bot statistics.
        """
        pythonVersion = platform.python_version()
        dpyVersion = discord.__version__
        serverCount = len(self.bot.guilds)
        memberCount = len(set(self.bot.get_all_members()))

        embed = discord.Embed(title=f"{self.bot.user.name} Stats", description="\uFEFF", colour=ctx.author.colour,
                              timestamp=ctx.message.created_at)

        embed.add_field(name="Bot Version:", value=self.bot.version)
        embed.add_field(name="Python Version:", value=pythonVersion)
        embed.add_field(name="discord.py Version:", value=dpyVersion)
        embed.add_field(name="Total Guilds:", value=serverCount)
        embed.add_field(name="Total Users:", value=memberCount)
        embed.add_field(name="Bot Developers:", value="<@326296729345589252>")

        embed.set_footer(text=f"Carpe Noctem | {self.bot.user.name}")
        embed.set_author(name=self.bot.user.name, icon_url=self.bot.user.avatar)

        await ctx.send(embed=embed)

    @commands.command()
    @commands.has_guild_permissions(administrator=True)
    @commands.cooldown(1, 5, commands.BucketType.guild)
    async def prefix(self, ctx, *, pre="cf!"):
        """
        Set a custom prefix for the bot.
        :param pre: The prefix you want to set.
        """
        data = cogs._json.read_json("prefixes")
        data[str(ctx.message.guild.id)] = pre
        cogs._json.write_json(data, "prefixes")
        await ctx.send(f"The guild prefix has been set to `{pre}`. Use `{pre}prefix <prefix>` to change it again!")


async def setup(bot):
    await bot.add_cog(General(bot))
