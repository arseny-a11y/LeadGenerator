from telethon import TelegramClient, events
from config.config import KEYWORDS, STOP_WORDS
from leadsearching.filters import is_lead_message
from database.save_leads import save_leads
from aiogram import Bot
from html import escape

class GroupParser:
    def __init__(self, client: TelegramClient, bot: Bot, chat_id: int, chats: list[int | str] | None = None) -> None:
        self.client = client
        self.bot = bot
        self.chat_id = chat_id
        self.chats = chats

    async def _send_leads(
            self,
            lead_chat_title: str,
            lead_chat_id: str,
            message_id: int,
            sender_id: int,
            sender_username: str,
            text: str,
            matched_keyword: str
        ) -> None:

        safe_title = escape(lead_chat_title)
        safe_text = escape(text)
        safe_username = sender_username if sender_username else "без username"
        safe_keyword = escape(matched_keyword)

        message_url = ""
        if str(lead_chat_id).startswith("-"): 
            message_url = f'🔗 <a href="https://t.me/{lead_chat_id}/{message_id}">Открыть сообщение</a>\n'

        message_text = (
            "🔥 <b>Новый лид!</b>\n\n"
            f"💬 <b>Чат:</b> {safe_title}\n"
            f"👤 <b>Отправитель:</b> {safe_username} (<code>{sender_id}</code>)\n"
            f"🔑 <b>Ключ:</b> <code>{safe_keyword}</code>\n"
            f"{message_url}\n"
            f"📝 <b>Текст:</b>\n<blockquote>{safe_text}</blockquote>"
        )

        await self.bot.send_message(
            chat_id=self.chat_id,
            text=message_text,
            parse_mode="HTML",
            disable_web_page_preview=True
        )
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
                sender_username=sender_username,
                message_text=text,
                matched_keyword=matched_keyword
            )

            if lead is None:
                return


            await self._send_leads(
                lead_chat_title=chat_title,
                lead_chat_id=chat_id,
                message_id=message_id,
                sender_id=sender_id,
                sender_username=sender_username,
                text=text,
                matched_keyword=matched_keyword,
            )