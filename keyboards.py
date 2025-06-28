from telegram import InlineKeyboardButton, InlineKeyboardMarkup

def main_menu():
    buttons = [
        [
            InlineKeyboardButton("🔄 تست ربات", callback_data="test_bot"),
            InlineKeyboardButton("📩 دریافت اخبار اقتصادی", callback_data="toggle_news")
        ]
    ]
    return InlineKeyboardMarkup(buttons)
