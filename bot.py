# bot.py
import asyncio
import logging
import os
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes
from dotenv import load_dotenv
from scheduler import create_scheduler
from news import check_forexfactory, check_bloomberg, check_investing
from db import init_db, add_user, set_user_status, get_user_status, get_active_users

load_dotenv()

TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
CHANNEL_ID = os.getenv("CHANNEL_ID")  # مثال: "@ictwithme"

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# دکمه‌های اصلی ربات
def get_main_keyboard():
    keyboard = [
        [InlineKeyboardButton("📡 دریافت اخبار اقتصادی", callback_data='toggle_news')],
        [InlineKeyboardButton("🧪 تست", callback_data='test')]
    ]
    return InlineKeyboardMarkup(keyboard)

# هندلر start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    add_user(user_id)
    await update.message.reply_text(
        "👋 به ربات تحلیل اقتصادی خوش آمدید!\nاز دکمه‌های زیر استفاده کنید:",
        reply_markup=get_main_keyboard()
    )

# دکمه‌ها
async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    user_id = query.from_user.id

    if query.data == 'toggle_news':
        status = get_user_status(user_id)
        new_status = not status
        set_user_status(user_id, new_status)
        msg = "✅ دریافت اخبار فعال شد." if new_status else "❌ دریافت اخبار غیرفعال شد."
        await query.edit_message_text(text=msg, reply_markup=get_main_keyboard())

    elif query.data == 'test':
        test_text = (
            "🧪 این یک پیام تستی است برای بررسی دریافت تحلیل اقتصادی.\n"
            "این ربات توسط کانال @ictwithme جهت رفاه و کمک به تریدرهای سراسر ایران ساخته شده است."
        )
        await context.bot.send_message(chat_id=user_id, text=test_text)
        await context.bot.send_message(chat_id=CHANNEL_ID, text=f"[تست کاربر {user_id}]\n{test_text}")

# زمان‌بندی خودکار
async def scheduled_tasks(application):
    await check_forexfactory(application)
    users = get_active_users()
    for user_id in users:
        await check_bloomberg(application, user_id)
        await check_investing(application, user_id)

# اجرای اصلی
async def main():
    init_db()
    application = Application.builder().token(TELEGRAM_BOT_TOKEN).build()

    application.add_handler(CommandHandler("start", start))
    application.add_handler(CallbackQueryHandler(button_handler))

    scheduler = create_scheduler(application.bot)  # 🟢 اصلاح این خط
    scheduler.add_job(lambda: asyncio.create_task(scheduled_tasks(application)), 'interval', minutes=5)

    await application.run_polling()

if __name__ == '__main__':
    asyncio.run(main())
