import asyncio
import logging
import os
import sys

import discord
from discord.ext import commands
from dotenv import load_dotenv

load_dotenv()


def setup_logging(level: str = "INFO") -> None:
    numeric = getattr(logging, level.upper(), logging.INFO)
    logging.basicConfig(
        level=numeric,
        format="%(asctime)s | %(levelname)-8s | %(name)s | %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
        stream=sys.stdout,
        force=True,
    )
    # Quiet noisy libs unless DEBUG.
    if numeric > logging.DEBUG:
        for noisy in ("discord.http", "discord.gateway", "aiohttp.access"):
            logging.getLogger(noisy).setLevel(logging.WARNING)


setup_logging(os.getenv("LOG_LEVEL", "INFO"))

from keep_alive import start as start_webserver
from utils.config import TOKEN, PREFIX, PORT, GUILD_ID

intents = discord.Intents.default()
intents.message_content = True
intents.members = True

bot = commands.Bot(command_prefix=PREFIX, intents=intents)


@bot.event
async def on_ready():
    print(f"Logged in as {bot.user} ({bot.user.id})")


async def load_cogs():
    for filename in os.listdir("./cogs"):
        if filename.endswith(".py") and not filename.startswith("_"):
            try:
                await bot.load_extension(f"cogs.{filename[:-3]}")
                print(f"Loaded cog: {filename[:-3]}")
            except Exception as e:
                print(f"Failed to load cog {filename}: {e}")


async def setup_hook():
    # Runs once per process start (unlike on_ready, which fires on every
    # gateway reconnect). Syncing here avoids re-registering commands on
    # each reconnect — that storm is what trips Discord's global 429s.
    await load_cogs()
    try:
        # GUILD_ID set: guild-scoped sync for instant iteration (no 1h global wait).
        # Otherwise: global sync.
        if GUILD_ID:
            guild = discord.Object(id=int(GUILD_ID))
            bot.tree.copy_global_to(guild=guild)
            synced = await bot.tree.sync(guild=guild)
            print(f"Synced {len(synced)} command(s) to guild {GUILD_ID}")
            synced = await bot.tree.sync()
        else:
            synced = await bot.tree.sync()
        print(f"Synced {len(synced)} slash command(s)")
    except Exception as e:
        print(f"Slash sync failed: {e}")


bot.setup_hook = setup_hook


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
        try:
            await bot.start(TOKEN)
        finally:
            web_task.cancel()


if __name__ == "__main__":
    asyncio.run(main())
