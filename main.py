import asyncio
import logging
import os

import discord
from discord.ext import commands
from dotenv import load_dotenv

load_dotenv()

logging.basicConfig(level=logging.INFO)
logging.getLogger("discord").setLevel(logging.INFO)

from keep_alive import start as start_webserver
from utils.config import TOKEN, PREFIX, PORT

intents = discord.Intents.default()
intents.message_content = True
intents.members = True

bot = commands.Bot(command_prefix=PREFIX, intents=intents)


@bot.event
async def on_ready():
    print(f"Logged in as {bot.user} ({bot.user.id})")
    try:
        synced = await bot.tree.sync()
        print(f"Synced {len(synced)} slash command(s)")
    except Exception as e:
        print(f"Slash sync failed: {e}")


async def load_cogs():
    for filename in os.listdir("./cogs"):
        if filename.endswith(".py") and not filename.startswith("_"):
            try:
                await bot.load_extension(f"cogs.{filename[:-3]}")
                print(f"Loaded cog: {filename[:-3]}")
            except Exception as e:
                print(f"Failed to load cog {filename}: {e}")


def discord_status() -> dict:
    user = str(bot.user) if bot.user else None
    try:
        latency = round(bot.latency * 1000) if not bot.is_closed() else None
    except Exception:
        latency = None
    return {
        "discord_connected": bot.user is not None and not bot.is_closed(),
        "discord_user": user,
        "discord_latency_ms": latency,
    }


async def main():
    # Start dummy web server first so Render detects an open port,
    # then run the Discord bot alongside it.
    web_task = asyncio.create_task(start_webserver(PORT, discord_status))
    async with bot:
        await load_cogs()
        try:
            await bot.start(TOKEN)
        finally:
            web_task.cancel()


if __name__ == "__main__":
    asyncio.run(main())
