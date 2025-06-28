import os
from dotenv import load_dotenv
import pytz

load_dotenv()

TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
CHANNEL_USERNAME = os.getenv("CHANNEL_USERNAME", "@ictwithme")

DB_PATH = "db.sqlite3"

# منطقه زمانی نیویورک
NEW_YORK_TIMEZONE = pytz.timezone("America/New_York")
