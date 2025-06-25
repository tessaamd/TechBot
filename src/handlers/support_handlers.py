from aiogram import Router, types, F
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from config import settings
from database import db
import logging

router = Router()

logger = logging.getLogger(__name__)

class SupportReplyState(StatesGroup):
    waiting_for_answer = State()

@router.callback_query(F.data.startswith("reply_"))
async def process_reply_callback(callback_query: types.CallbackQuery, state: FSMContext):
    try:
        ticket_id = int(callback_query.data.split('_')[1])
        await state.set_state(SupportReplyState.waiting_for_answer)
        await state.update_data(ticket_id=ticket_id)
        await callback_query.message.answer(f"✔ Введите ответ на тикет #{ticket_id}")
        await callback_query.answer()
    except Exception as e:
        logger.error(f"Ошибка при обработке callback: {e}")
        await callback_query.message.answer("❌ Ошибка при обработке запроса")

@router.message(StateFilter(SupportReplyState.waiting_for_answer))
async def handle_support_answer(message: types.Message, state: FSMContext):
    try:
        data = await state.get_data()
        ticket_id = data['ticket_id']
        answer = message.text.strip()
        if len(answer) > settings.MAX_LENGTH:
            await message.reply(f"✖ Ответ превышает {settings.MAX_LENGTH} символов!")
            return
        ticket = await db.get_ticket(ticket_id)
        if not ticket:
            await message.reply(f"✖ Тикет #{ticket_id} не найден")
            await state.clear()
            return
        if ticket['status'] != 'open':
            await message.reply(f"✖ Тикет #{ticket_id} уже закрыт")
            await state.clear()
            return
        await db.close_ticket(ticket_id, answer)
        logger.info(f"Тикет #{ticket_id} закрыт с ответом: {answer[:50]}...")
        await message.bot.send_message(
            chat_id=ticket['user_id'],
            text=f"✅ Ответ на ваш вопрос: {answer}"
        )
        await message.reply("✔ Ответ отправлен пользователю")
        await state.clear()
    except Exception as e:
        logger.error(f"Ошибка при обработке ответа: {e}")
        await message.reply(f"❌ Ошибка при отправке ответа: {e}")
        await state.clear()