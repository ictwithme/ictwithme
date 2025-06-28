import pytz
import datetime
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from forex import get_forex_news
from gpt import generate_analysis
from telegram import Bot
import asyncio

TIMEZONE = pytz.timezone("America/New_York")
CHANNEL_ID = "@ictwithme"

async def check_forex_news(bot: Bot):
    events = get_forex_news()
    now = datetime.datetime.now(TIMEZONE)

    for event in events:
        event_time = event["time"]
        if event_time - now <= datetime.timedelta(minutes=10) and not event["sent"]:
            analysis = generate_analysis(event["title"], event["impact"], event["currency"])

            message = f"""📢 <b>خبر اقتصادی پیش رو</b>

🕒 زمان: {event_time.strftime('%Y-%m-%d %H:%M')} به وقت نیویورک  
🌍 کشور: {event["currency"]}  
🔥 اهمیت: {event["impact"]}
📰 عنوان: {event["title"]}

🧠 <b>تحلیل فاندامنتال:</b>  
{analysis}

📡 منبع: ForexFactory.com  
این ربات توسط کانال @ictwithme جهت رفاه و کمک به تریدرهای سراسر ایران ساخته شده است."""

            await bot.send_message(chat_id=CHANNEL_ID, text=message, parse_mode="HTML")
            event["sent"] = True

def create_scheduler(bot: Bot):
    scheduler = AsyncIOScheduler(timezone=TIMEZONE)
    scheduler.add_job(check_forex_news, 'interval', minutes=1, args=[bot])
    scheduler.start()
