from database.database import session_factory
from database.models import Leads
from sqlalchemy import select
from datetime import datetime, timedelta, timezone

async def save_leads(
    chat_id: str | None,
    chat_title: str | None,
    message_id: int,
    sender_id: int | None,
    sender_username: str | None,
    message_text: str,
    matched_keyword: str 
):
    if not sender_id:
        return
    
    normalized_text = " ".join(message_text.lower().split())
    cutoff = datetime.now(timezone.utc).replace(tzinfo=None) - timedelta(hours=6)

    async with session_factory() as session:

        #проверяем что повтороного сообщения от того же пользователя с интервалом 6 часов не было
        lead_in_db = await session.scalar(
            select(Leads.id)
            .where(Leads.message_text == normalized_text,
            Leads.sender_id == sender_id,
            Leads.created_at >= cutoff
            )
            .limit(1)
        )

        if lead_in_db is not None:
            return None

        lead = Leads(
            chat_id=chat_id,
            chat_title=chat_title,
            message_id=message_id,
            sender_id=sender_id,
            sender_username=sender_username,
            message_text=normalized_text,
            matched_keyword=matched_keyword,
        )

        session.add(lead)
        await session.commit()
        await session.refresh(lead)
        
        return lead