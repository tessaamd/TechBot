from aiogram import Router, types, F
from aiogram.filters import Command
from config import settings
from database import db
from keybords import kb
import logging

router = Router()

logger = logging.getLogger(__name__)

@router.message(Command("start"))
async def start(message: types.Message):
    await message.answer("Привет! Я бот техподдержки.", reply_markup=kb.user_main_kb())

@router.message(F.text == "Написать в поддержку")
async def ask_question(message: types.Message):
    await message.answer("Пожалуйста, напишите ваш вопрос.")

@router.message(F.chat.type == "private")
async def handle_user_message(message: types.Message):
    user_id = message.from_user.id
    user_name = message.from_user.username or message.from_user.first_name
    question = message.text
    ticket_id = db.add_ticket(user_id, user_name, question)
    logger.info(f"Создан тикет #{ticket_id} от пользователя {user_name}")
    await message.bot.send_message(
        chat_id=settings.SUPPORT_CHAT_ID,
        text=f"Новый тикет #{ticket_id}\nПользователь: {user_name}\nВопрос: {question}",
        reply_markup=kb.support_reply_kb(ticket_id)
    )
    await message.answer("Ваш вопрос отправлен в поддержку. Ожидайте ответа.")