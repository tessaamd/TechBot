from aiogram import Router, types
from config import settings
from database.db import db

router = Router()

@router.callback_query(lambda c: c.data.startswith("reply_"))
async def process_reply_callback(callback: types.CallbackQuery):
    ticket_id = int(callback.data.split("_")[1])
    await callback.message.answer(f"💬 Введите ответ на тикет #{ticket_id}:")
    await callback.answer()

@router.message(lambda message: message.reply_to_message and 
                message.chat.id == settings.SUPPORT_CHAT_ID)
async def handle_support_reply(message: types.Message):
    try:
        text = message.reply_to_message.text
        ticket_id = int(text.split("#")[1].split("\n")[0])
    except (IndexError, ValueError):
        return
    
    answer = message.text.strip()
    if len(answer) > settings.MAX_LENGTH:
        return await message.reply(
            f"❌ Ответ превышает {settings.MAX_LENGTH} символов!"
        )
    
    ticket = db.get_ticket(ticket_id)
    if not ticket or ticket[5] != 'open':
        return await message.reply("❌ Тикет уже закрыт или не существует!")
    
    db.close_ticket(ticket_id, answer)
    
    await message.bot.send_message(
        chat_id=ticket[1],  
        text=f"🔔 Получен ответ от поддержки:\n\n{answer}"
    )
    await message.reply("✅ Ответ отправлен пользователю!")