from telegram import Update
from telegram.ext import ContextTypes

async def handle_button_click(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    data = query.data

    if data == "toggle_news_on":
        await query.edit_message_text("📬 دریافت اخبار اقتصادی فعال شد.")
        # اینجا می‌تونی در دیتابیس وضعیت کاربر رو ذخیره کنی

    elif data == "toggle_news_off":
        await query.edit_message_text("🔕 دریافت اخبار اقتصادی غیرفعال شد.")
        # اینجا هم می‌تونی وضعیت رو غیرفعال کنی

    else:
        await query.edit_message_text("❓ فرمان ناشناخته.")
