import random

import discord
from discord import app_commands
from discord.ext import commands


class General(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.hybrid_command(name="ping", description="Check bot latency")
    async def ping(self, ctx: commands.Context):
        await ctx.send(f"Pong! {round(self.bot.latency * 1000)}ms")

    @app_commands.command(name="hello", description="Say hello")
    async def hello(self, interaction: discord.Interaction):
        await interaction.response.send_message(f"Hello {interaction.user.mention}!")

    @app_commands.command(name="flip", description="Flip a coin")
    async def flip(self, interaction: discord.Interaction):
        await interaction.response.send_message(random.choice(["Heads", "Tails"]))

    @app_commands.command(name="anolaro", description="Randomly pick one from your list")
    @app_commands.describe(
        option1="First choice",
        option2="Second choice",
        option3="Third choice (optional)",
        option4="Fourth choice (optional)",
        option5="Fifth choice (optional)",
    )
    async def anolaro(
        self,
        interaction: discord.Interaction,
        option1: str,
        option2: str,
        option3: str | None = None,
        option4: str | None = None,
        option5: str | None = None,
    ):
        choices = [o for o in (option1, option2, option3, option4, option5) if o]
        await interaction.response.send_message(f"\U0001f3b2 {random.choice(choices)}")


async def setup(bot: commands.Bot):
    await bot.add_cog(General(bot))
