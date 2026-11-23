import asyncio
from config.config import settings
from leadsearching.parser import GroupParser
from leadsearching.client import TelegramParserClient

async def start_worker() -> None:
    tg_client = TelegramParserClient(
        api_id=settings.API_ID,
        api_hash=settings.API_HASH
    )

    client = await tg_client.connect()

    chats = [settings.USERNAME_CHANNEL]

    parser = GroupParser(client=client, chats=chats)
    parser.register()

    print("Мониторинг чатов запущен")

    try:
        await client.run_until_disconnected()
    finally:
        await client.disconnect()

if __name__ == "__main__":
    asyncio.run(start_worker())