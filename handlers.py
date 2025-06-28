from telegram import Update
from telegram.ext import ContextTypes
from keyboards import main_menu
from database import add_user, set_receive_news

WELCOME_TEXT = """
به ربات اخبار اقتصادی خوش آمدید 📊
از دکمه‌های زیر برای دریافت اخبار و تحلیل‌ها استفاده کنید.
"""

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    add_user(user.id, user.username or "")
    await update.message.reply_text(WELCOME_TEXT, reply_markup=main_menu())

async def toggle_receive_news(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    user_id = query.from_user.id
    current = context.user_data.get("receive_news", False)
    new_state = not current
    set_receive_news(user_id, new_state)
    context.user_data["receive_news"] = new_state
    await query.answer("دریافت خبر {} شد ✅".format("فعال" if new_state else "غیرفعال"))
    await query.edit_message_reply_markup(reply_markup=main_menu())
