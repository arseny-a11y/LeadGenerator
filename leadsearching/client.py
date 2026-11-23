from telethon import TelegramClient
import asyncio
from config.config import settings

class TelegramParserClient:
    def __init__(self, api_id: int, api_hash: str, session_name: str = "leadsearching/telethon") -> None:
        self.api_id = api_id
        self.api_hash = api_hash
        self.session_name = session_name
        self.client = TelegramClient(
            self.session_name,
            self.api_id,
            self.api_hash,
        )

    async def connect(self) -> TelegramClient:
        await self.client.start()
        return self.client
    
    async def disconnect(self) -> None:
        if self.client.is_connected():
           await self.client.disconnect()

