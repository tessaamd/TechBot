from aiogram import Router, types
from aiogram.filters import Command
from config import settings
from database.db import db
from keybords import kb

router = Router()

@router.message(Command("start"))
async def cmd_start(message: types.Message):
    await message.answer(
        "👋 Привет! Я бот техподдержки.\n"
        "Нажми кнопку ниже чтобы задать вопрос:",
        reply_markup=kb.user_main_kb()
    )

@router.message(lambda message: message.text == "Написать в поддержку")
async def request_question(message: types.Message):
    await message.answer(
        f"✍️ Напишите ваш вопрос (макс. {settings.MAX_LENGTH} символов):",
        reply_markup=types.ReplyKeyboardRemove()
    )

@router.message()
async def handle_user_message(message: types.Message):
    if message.chat.type != "private":
        return
    
    question = message.text.strip()
    if len(question) > settings.MAX_LENGTH:
        return await message.answer(
            f"❌ Вопрос превышает {settings.MAX_LENGTH} символов!"
        )
    
    user_name = message.from_user.full_name
    if message.from_user.username:
        user_name += f" (@{message.from_user.username})"
    
    ticket_id = db.add_ticket(
        user_id=message.from_user.id,
        user_name=user_name,
        question=question
    )
    
    await message.bot.send_message(
        chat_id=settings.SUPPORT_CHAT_ID,
        text=(
            f"🆕 Новый тикет #{ticket_id}\n"
            f"👤 Пользователь: {user_name}\n"
            f"❓ Вопрос:\n{question}"
        ),
        reply_markup=kb.support_reply_kb(ticket_id)
    )
    
    await message.answer(
        "✅ Ваш вопрос отправлен в поддержку! Ожидайте ответа.",
        reply_markup=kb.user_main_kb()
    )