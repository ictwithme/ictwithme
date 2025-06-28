import os
import asyncio
from telegram.ext import (
    Application,
    CommandHandler,
    CallbackQueryHandler,
    MessageHandler,
    filters,
)
from handlers import (
    start,
    handle_button_click,
    handle_text_message,
)
from scheduler import create_scheduler
from dotenv import load_dotenv

load_dotenv()  # بارگذاری متغیرهای محیطی از .env

TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")

async def main():
    # ساخت اپلیکیشن
    application = Application.builder().token(TELEGRAM_BOT_TOKEN).build()

    # اضافه کردن هندلرها
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CallbackQueryHandler(handle_button_click))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_text_message))

    # راه‌اندازی زمان‌بند
    create_scheduler(application.bot)

    # اجرای ربات با polling
    await application.run_polling()

if __name__ == "__main__":
    asyncio.run(main())
