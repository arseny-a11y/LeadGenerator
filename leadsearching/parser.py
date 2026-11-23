from telethon import TelegramClient, events
from config.config import KEYWORDS, STOP_WORDS
from leadsearching.filters import is_lead_message

class GroupParser:
    def __init__(self, client: TelegramClient, chats: list[int | str] | None = None) -> None:
        self.client = client
        self.chats = chats

    def register(self) -> None:
        @self.client.on(events.NewMessage(chats=self.chats))
        async def hadle_new_message(event: events.NewMessage.Event) -> None:
            text = event.raw_text
            if not is_lead_message(text, KEYWORDS, STOP_WORDS):
                return

            sender = await event.get_sender()
            chat = await event.get_chat()

            #безопасно достаем username пользователя и название чата от куда поступило сообщение
            username = (f"@{sender.username}" if getattr(sender, "username", None) else "нет username")
            chat_title = (getattr(chat, "title", None) or getattr(chat, "username", None) or str(event.chat_id))

            print("🔥 Найден лид!")
            print(f"Чат: {chat_title} (ID: {event.chat_id})")
            print(f"От кого: {username} (ID: {event.sender_id})")
            print(f"Текст: {text}")
            print("-" * 40)