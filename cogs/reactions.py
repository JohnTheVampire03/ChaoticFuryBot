import discord
from discord.ext import commands
from cogs._json import read_json, write_json


class ReactionRoles(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.roles_file = "reaction_roles"
        self.roles_data = read_json(self.roles_file)
        self.reaction_roles_messages_file = "reaction_role_messages"
        self.reaction_roles_messages = read_json(self.reaction_roles_messages_file)

    def save_roles(self):
        write_json(self.roles_data, self.roles_file)

    def save_messages(self):
        write_json(self.reaction_roles_messages, self.reaction_roles_messages_file)

    @commands.Cog.listener()
    async def on_ready(self, ctx):
        print("Reactions Cog has been loaded\n-----")

    @commands.Cog.listener()
    async def on_reaction_add(self, reaction, user):
        if user.bot:
            return  # Ignore reactions from bots

        emoji_str = str(reaction.emoji)
        message_id = reaction.message.id

        if message_id in self.reaction_roles_messages and emoji_str in self.roles_data:
            role_id = self.roles_data[emoji_str]
            guild = self.bot.get_guild(reaction.message.guild.id)
            role = guild.get_role(role_id)

            if role:
                await user.add_roles(role)
                print(f"Added role {role.name} to {user.display_name}")

    @commands.Cog.listener()
    @commands.guild_only()
    @commands.has_guild_permissions(administrator=True)
    async def on_reaction_remove(self, reaction, user):
        if user.bot:
            return  # Ignore reactions from bots

        emoji_str = str(reaction.emoji)
        message_id = reaction.message.id

        if message_id in self.reaction_roles_messages and emoji_str in self.roles_data:
            role_id = self.roles_data[emoji_str]
            guild = self.bot.get_guild(reaction.message.guild.id)
            role = guild.get_role(role_id)

            if role and role in user.roles:
                await user.remove_roles(role)
                print(f"Removed role {role.name} from {user.display_name}")

    @commands.command(name="addrole")
    @commands.guild_only()
    @commands.has_guild_permissions(administrator=True)
    async def add_role(self, ctx, role: discord.Role, emoji):
        self.roles_data[str(emoji)] = role.id
        self.save_roles()
        await ctx.send(f"Role {role.name} added with emoji {emoji}.")

    @commands.command(name="removerole")
    async def remove_role(self, ctx, emoji):
        if str(emoji) in self.roles_data:
            del self.roles_data[str(emoji)]
            self.save_roles()
            await ctx.send(f"Role removed for emoji {emoji}.")
        else:
            await ctx.send("No role found for the provided emoji.")

    @commands.command(name="viewroles")
    async def view_roles(self, ctx):
        roles_info = "\n".join(
            [f"{emoji}: {self.get_role_name(ctx, role_id)}" for emoji, role_id in self.roles_data.items()])
        await ctx.send(f"Saved roles:\n{roles_info}")

    def get_role_name(self, ctx, role_id):
        role = ctx.guild.get_role(role_id)
        return role.name if role else "Role not found"

    @commands.command(name="reactionroles")
    @commands.guild_only()
    @commands.has_guild_permissions(administrator=True)
    async def reaction_roles(self, ctx):
        embed = discord.Embed(title="Reaction Roles", description="React to get the corresponding roles:")
        for emoji, role_id in self.roles_data.items():
            role = ctx.guild.get_role(role_id)
            if role:
                embed.add_field(name=str(emoji), value=role.mention, inline=True)
            else:
                embed.add_field(name=str(emoji), value="Role not found", inline=True)
        message = await ctx.send(embed=embed)

        for emoji in self.roles_data.keys():
            await message.add_reaction(emoji)

        # Save the message ID for future reference
        self.reaction_roles_messages[message.id] = True
        self.save_messages()


async def setup(bot):
    await bot.add_cog(ReactionRoles(bot))
