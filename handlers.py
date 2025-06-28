# handlers.py

from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton("📢 دریافت اخبار اقتصادی", callback_data="toggle_news_on")],
        [InlineKeyboardButton("🔕 عدم دریافت اخبار اقتصادی", callback_data="toggle_news_off")],
        [InlineKeyboardButton("📎 عضویت در کانال", url="https://t.me/ictwithme")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    await update.message.reply_text(
        "سلام 👋\nبه ربات تحلیل اخبار اقتصادی خوش آمدید.\nلطفاً از گزینه‌های زیر استفاده کنید:",
        reply_markup=reply_markup
    )
