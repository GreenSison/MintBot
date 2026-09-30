import os

from dotenv import load_dotenv

load_dotenv()

TOKEN = os.getenv("DISCORD_TOKEN", "")
PREFIX = os.getenv("COMMAND_PREFIX", "!")
GUILD_ID = os.getenv("GUILD_ID")  # optional: for instant guild slash sync in dev
PORT = int(os.getenv("PORT", "10000"))  # Render injects PORT, defaults to 10000 locally

if not TOKEN:
    raise RuntimeError("DISCORD_TOKEN not set. Copy .env.example to .env and fill it in.")
