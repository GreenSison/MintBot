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

    @app_commands.command(name="gay", description="Check how gay someone is")
    @app_commands.describe(user="Person to check (defaults to you)")
    async def gay(
        self, interaction: discord.Interaction, user: discord.Member | None = None
    ):
        target = user or interaction.user
        pct = random.randint(0, 100)
        if pct < 10:
            blurb = random.choice(
                [
                    "certified straight, painfully heterosexual",
                    "straight as an arrow, boringly so",
                    "hetero levels off the charts",
                ]
            )
        elif pct < 30:
            blurb = random.choice(
                [
                    "mostly straight, but sussy vibes detected",
                    "a little fruity around the edges",
                    "straight with questionable playlist choices",
                ]
            )
        elif pct < 50:
            blurb = random.choice(
                [
                    "half-half, bi-curious energy",
                    "suspiciously fond of brunch",
                    "straight on paper, rainbow in spirit",
                ]
            )
        elif pct < 70:
            blurb = random.choice(
                [
                    "pretty gay, owns at least one rainbow item",
                    "slay energy radiating strongly",
                    "definitely claps when the plane lands in Mykonos",
                ]
            )
        elif pct < 90:
            blurb = random.choice(
                [
                    "super gay, villages are missing their idol",
                    "walks like the runway follows them",
                    "knows every drag queen by first name",
                ]
            )
        else:
            blurb = random.choice(
                [
                    "ULTRA MEGA GAY, final boss of fabulous",
                    "off the charts, rainbows fear YOU",
                    "1000% iconic, no further questions",
                ]
            )
        await interaction.response.send_message(
            f"\U0001f308 {target.mention} is **{pct}% gay** — {blurb}."
        )

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
