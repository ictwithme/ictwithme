from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes

# دیتابیس موقت (در عمل باید با پایگاه‌داده SQLite جایگزین شود)
user_settings = {}

# پیام خوش‌آمدگویی و دکمه‌ها
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton("📢 دریافت اخبار اقتصادی", callback_data="toggle_news_on")],
        [InlineKeyboardButton("🔕 توقف دریافت اخبار", callback_data="toggle_news_off")],
        [InlineKeyboardButton("📺 عضویت در کانال", url="https://t.me/ictwithme")],
        [InlineKeyboardButton("✅ تست عملکرد ربات", callback_data="test_bot")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    await update.message.reply_text(
        "سلام 👋\nبه ربات تحلیل اخبار اقتصادی خوش آمدید!\n\nاز منوی زیر یکی از گزینه‌ها را انتخاب کنید:",
        reply_markup=reply_markup
    )

# مدیریت کلیک روی دکمه‌ها
async def handle_button_click(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    user_id = query.from_user.id
    data = query.data

    if data == "toggle_news_on":
        user_settings[user_id] = True
        await query.edit_message_text("✅ دریافت اخبار اقتصادی برای شما *فعال* شد.", parse_mode="Markdown")
    elif data == "toggle_news_off":
        user_settings[user_id] = False
        await query.edit_message_text("🔕 دریافت اخبار اقتصادی برای شما *غیرفعال* شد.", parse_mode="Markdown")
    elif data == "test_bot":
        await query.edit_message_text("🤖 ربات به‌درستی فعال است و آماده خدمت‌رسانی می‌باشد.")

# پاسخ به پیام‌های متنی عادی (اگر کاربر مستقیم پیام دهد)
async def handle_text_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("لطفاً از دکمه‌های زیر استفاده کنید. 👇")
