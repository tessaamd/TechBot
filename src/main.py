import asyncio
from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage
from config import settings
from handlers import user_handlers, support_handlers
import logging

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)

async def main():
    bot = Bot(token=settings.BOT_TOKEN)
    dp = Dispatcher(storage=MemoryStorage())
    
    dp.include_router(user_handlers.router)
    dp.include_router(support_handlers.router)
    
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())