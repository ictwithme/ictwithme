import asyncio
import logging
import os

from telegram.ext import (
    Application,
    CommandHandler,
    CallbackQueryHandler,
    MessageHandler,
    filters,
)
from telegram import Update
from telegram.constants import ParseMode
from telegram.ext import ContextTypes

from scheduler import create_scheduler
from handlers import (
    start,
    handle_button_click,
    handle_text_message,
)

# بارگذاری توکن از متغیر محیطی
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")

# فعال‌سازی لاگ‌ها
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
logger = logging.getLogger(__name__)


async def main():
    # ساخت اپلیکیشن تلگرام
    application = Application.builder().token(TELEGRAM_BOT_TOKEN).build()

    # گرفتن شیء bot برای ارسال پیام از طریق زمان‌بند
    bot = application.bot

    # راه‌اندازی زمان‌بند برای بررسی اخبار فارکس
    create_scheduler(bot)

    # افزودن هندلرها
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CallbackQueryHandler(handle_button_click))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_text_message))

    # اجرای ربات
    await application.initialize()
    await application.start()
    await application.updater.start_polling()
    await application.idle()


if __name__ == "__main__":
    asyncio.run(main())
