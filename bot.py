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

load_dotenv()

TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")

async def main():
    application = Application.builder().token(TELEGRAM_BOT_TOKEN).build()

    application.add_handler(CommandHandler("start", start))
    application.add_handler(CallbackQueryHandler(handle_button_click))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_text_message))

    create_scheduler(application.bot)

    # اجرای ربات با polling
    await application.run_polling(close_loop=False)

if __name__ == "__main__":
    try:
        # بررسی اینکه آیا event loop در حال اجراست
        loop = asyncio.get_event_loop()
        if loop.is_running():
            # اگر در محیطی مثل Jupyter یا Render هستیم
            loop.create_task(main())
        else:
            loop.run_until_complete(main())
    except RuntimeError:
        # حالت fallback برای محیط‌هایی که بالا نمی‌آیند
        asyncio.run(main())
