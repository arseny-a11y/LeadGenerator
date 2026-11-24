from aiogram import Bot, Dispatcher
from config.config import settings
from database.database import init_db
import asyncio
import logging

async def main():

    logging.basicConfig(level=logging.INFO)
    
    bot = Bot(settings.TOKEN)
    dp = Dispatcher()

    await init_db()
    # dp.include_router(monitor_router)
    try:
        print("Бот запущен!")
        await bot.delete_webhook(drop_pending_updates=True)
        await dp.start_polling(bot)

    finally:
        await bot.session.close()
        
if __name__ == "__main__":
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        print("Бот остановлен!")