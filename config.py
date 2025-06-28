import os
from dotenv import load_dotenv

load_dotenv()

TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
CHANNEL_ID = os.getenv("CHANNEL_ID")
DB_PATH = os.getenv("DB_PATH", "users.db")

NEW_YORK_TIMEZONE = "America/New_York"
