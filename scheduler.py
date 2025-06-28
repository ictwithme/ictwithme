import logging
import os
from dotenv import load_dotenv
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    Application, CommandHandler, CallbackQueryHandler, ContextTypes
)
from scheduler import create_scheduler
from database import init_db, set_user_subscription, get_user_subscription

load_dotenv()
TOKEN = os.getenv("7637175756:AAHU2LxBRVmOo7CbrIgl1j7ZovG3ex_En30")
CHANNEL_ID = os.getenv("@ictwithme")

logging.basicConfig(level=logging.INFO)

# شروع ربات
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton("فعال‌سازی اخبار اقتصادی 📈", callback_data="subscribe")],
        [InlineKeyboardButton("غیرفعال‌سازی اخبار اقتصادی 🚫", callback_data="unsubscribe")],
        [InlineKeyboardButton("دکمه تست 🧪", callback_data="test")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text("به ربات اخبار اقتصادی خوش آمدید!", reply_markup=reply_markup)

# مدیریت دکمه‌ها
async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    user_id = query.from_user.id
    
    if query.data == "subscribe":
        set_user_subscription(user_id, True)
        await query.message.reply_text("✅ دریافت اخبار اقتصادی فعال شد.")
    elif query.data == "unsubscribe":
        set_user_subscription(user_id, False)
        await query.message.reply_text("❌ دریافت اخبار اقتصادی غیرفعال شد.")
    elif query.data == "test":
        test_msg = "پیام تستی ربات \n\nاین ربات توسط کانال @ictwithme جهت رفاه و کمک به تریدرهای سراسر ایران ساخته شده است."
        await context.bot.send_message(chat_id=user_id, text=test_msg)
        await context.bot.send_message(chat_id=CHANNEL_ID, text=f"[پیام تست برای کاربر](tg://user?id={user_id})", parse_mode="Markdown")

# راه‌اندازی اصلی
def main():
    application = Application.builder().token(TOKEN).build()

    init_db()
    create_scheduler(application.bot)

    application.add_handler(CommandHandler("start", start))
    application.add_handler(CallbackQueryHandler(button_handler))

    application.run_polling()

if __name__ == '__main__':
    main()


### فایل database.py

import sqlite3

def init_db():
    conn = sqlite3.connect("users.db")
    c = conn.cursor()
    c.execute("""
        CREATE TABLE IF NOT EXISTS users (
            user_id INTEGER PRIMARY KEY,
            subscribed INTEGER DEFAULT 0
        )
    """)
    conn.commit()
    conn.close()

def set_user_subscription(user_id, subscribed):
    conn = sqlite3.connect("users.db")
    c = conn.cursor()
    c.execute("REPLACE INTO users (user_id, subscribed) VALUES (?, ?)", (user_id, int(subscribed)))
    conn.commit()
    conn.close()

def get_user_subscription(user_id):
    conn = sqlite3.connect("users.db")
    c = conn.cursor()
    c.execute("SELECT subscribed FROM users WHERE user_id = ?", (user_id,))
    result = c.fetchone()
    conn.close()
    return result and result[0] == 1
