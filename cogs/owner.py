import discord
from discord.ext import commands

import cogs._json


class Owner(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print("Owner Cog has been loaded\n-----")

    @commands.command(aliases=["disconnect", "close", "stopbot"])
    @commands.is_owner()
    async def logout(self, ctx):
        """
        If the user running the command owns the bot then this will disconnect the bot from discord.
        """
        await ctx.send(f"Hey {ctx.author.mention}, I am logging out :wave:")
        await self.bot.close()

    @logout.error
    async def logout_error(self, ctx, error):
        """
        Whenever the logout command has an error, this will be tripped.
        """
        if isinstance(error, commands.CheckFailure):
            await ctx.send("You lack permission to use this command as you are not the owner of this bot.")
        else:
            raise error

    @commands.command()
    @commands.is_owner()
    async def blacklist(self, ctx, user: discord.Member):
        """
        If the user running the command owns the bot, then this will prevent a user from using it.
        :param user: The user you want to blacklist. (mention)
        """
        if ctx.message.author.id == user.id:
            await ctx.send("You cannot blacklist yourself.")

        self.bot.blacklisted_users.append(user.id)
        data = cogs._json.read_json("blacklist")
        data["blacklistedUsers"].append(user.id)
        cogs._json.write_json(data, "blacklist")
        await ctx.send(f"User {user.name} has been blacklisted.")

    @commands.command()
    @commands.is_owner()
    async def whitelist(self, ctx, user: discord.Member):
        """
        If the user running the command owns the bot, then this will remove a user from the blacklist.
        :param user: The user you want to whitelist. (member)
        """
        self.bot.blacklisted_users.remove(user.id)
        data = cogs._json.read_json("blacklist")
        data["blacklistedUsers"].remove(user.id)
        cogs._json.write_json(data, "blacklist")
        await ctx.send(f"User {user.name} has been whitelisted.")


async def setup(bot):
    await bot.add_cog(Owner(bot))
