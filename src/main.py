import asyncio
from aiogram import Bot, Dispatcher
from config import settings  
from handlers import user_handlers, support_handlers

async def main():
    bot = Bot(token=settings.BOT_TOKEN)  
    dp = Dispatcher()
    
    dp.include_router(user_handlers.router)
    dp.include_router(support_handlers.router)
    
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())  