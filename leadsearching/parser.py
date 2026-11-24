from telethon import TelegramClient, events
from config.config import KEYWORDS, STOP_WORDS
from leadsearching.filters import is_lead_message
from database.save_leads import save_leads

class GroupParser:
    def __init__(self, client: TelegramClient, chats: list[int | str] | None = None) -> None:
        self.client = client
        self.chats = chats

    def register(self) -> None:
        @self.client.on(events.NewMessage(chats=self.chats))
        async def handle_new_message(event: events.NewMessage.Event) -> None:
            text = event.raw_text

            status, matched_keyword = is_lead_message(text, KEYWORDS, STOP_WORDS)
            if not status:
                return

            sender = await event.get_sender()
            chat = await event.get_chat()

            #безопасно достаем username пользователя и название чата от куда поступило сообщение
            chat_id = event.chat_id
            chat_title = (getattr(chat, "title", None) or getattr(chat, "username", None) or str(event.chat_id))
            message_id = event.message.id
            sender_id = event.sender_id or getattr(sender, "id", None)
            username = getattr(sender, "username", None)
            sender_username = f"@{username}" if username else None

            lead = await save_leads(
                chat_id=chat_id,
                chat_title=chat_title,
                message_id=message_id,
                sender_id=sender_id,
                sender_username=sender_username
            )

            