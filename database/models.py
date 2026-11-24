from sqlalchemy.orm import Mapped, mapped_column, DeclarativeBase
from sqlalchemy import Integer, String, Text, DateTime, func
from datetime import datetime

class Base(DeclarativeBase):
    pass

class Leads(Base):
    __tablename__ = "leads"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    chat_id: Mapped[str | None] = mapped_column(String(64), nullable=True)
    chat_title: Mapped[str | None] = mapped_column(Text, nullable=True)
    message_id: Mapped[int] = mapped_column(Integer, nullable=False)
    sender_id: Mapped[int | None] = mapped_column(Integer, nullable=False)
    sender_username: Mapped[str | None] = mapped_column(String(64), nullable=True)
    message_text: Mapped[str] = mapped_column(Text, nullable=False)
    matched_keyword: Mapped[str] = mapped_column(Text, nullable=False)
    created_at: Mapped[datetime] = mapped_column(server_default=func.now(), nullable=False)
