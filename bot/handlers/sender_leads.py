from aiogram import Bot, F, Router
from aiogram.types import Message, CallbackQuery
from aiogram.filters import Command, CommandStart

leads_router = Router()

@leads_router.message(CommandStart())
async def cmd_start(message: Message):
    text = (
        "👋 <b>Telegram Lead Generator Bot</b>\n\n"
        "Бот отслеживает новые сообщения в выбранных Telegram-чатах, "
        "фильтрует заявки по ключевым словам и сразу присылает лиды сюда.\n\n"
        "📌 <b>Доступные команды:</b>\n"
        "• /start_parser — запустить мониторинг чатов\n"
        "• /stop_parser — остановить мониторинг\n"
        "• /status — проверить состояние парсера и активные чаты\n"
        "• /set_chats — задать или обновить список отслеживаемых чатов\n\n"
        "🛡 Повторные сообщения от одного пользователя автоматически фильтруются в течение 6 часов."
    )

    await message.answer(text=text, parse_mode="HTML")

@leads_router.message(Command("start_parser"))
async def cmd_start_parser(message: Message):
    pass