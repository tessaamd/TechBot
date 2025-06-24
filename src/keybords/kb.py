from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton

def user_main_kb():
    return ReplyKeyboardMarkup(
        keyboard=[[KeyboardButton(text="Написать в поддержку")]],
        resize_keyboard=True
    )

def support_reply_kb(ticket_id):
    return InlineKeyboardMarkup(
        inline_keyboard=[[InlineKeyboardButton(text="Ответить", callback_data=f"reply_{ticket_id}")]]
    )