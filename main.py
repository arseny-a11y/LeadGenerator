from aiogram import Bot, Dispatcher
from config.config import settings
from database.database import init_db
from bot.handlers.sender_leads import leads_router
from leadsearching.parser import GroupParser
from leadsearching.client import TelegramParserClient
import asyncio
import logging

async def main():

    logging.basicConfig(level=logging.INFO)
    
    bot = Bot(settings.TOKEN)
    dp = Dispatcher()

    await init_db()
    dp.include_router(leads_router)

    tg_client = TelegramParserClient(
            api_id=settings.API_ID,
            api_hash=settings.API_HASH
        )
    
    client = await tg_client.connect()

    chats = [settings.USERNAME_CHANNEL]

    parser = GroupParser(client=client, bot=bot, chat_id=5265247476, chats=chats)
    lead = parser.register()
    
    print("Мониторинг чатов запущен")
    
    try:
        print("Бот запущен!")
        await bot.delete_webhook(drop_pending_updates=True)
        await asyncio.gather(
            dp.start_polling(bot),
            client.run_until_disconnected()
        )

    finally:
        await bot.session.close()
        await client.disconnect()
        
if __name__ == "__main__":
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        print("Бот остановлен!")