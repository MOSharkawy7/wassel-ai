from datetime import datetime

from sqlalchemy import DateTime, ForeignKey, String, Text, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base


class Message(Base):
    __tablename__ = "messages"

    id: Mapped[int] = mapped_column(
        primary_key=True,
        autoincrement=True,
    )

    conversation_id: Mapped[int] = mapped_column(
        ForeignKey("conversations.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )

    direction: Mapped[str] = mapped_column(
        String(20),
        nullable=False,
    )

    sender_type: Mapped[str] = mapped_column(
        String(20),
        nullable=False,
    )

    message_type: Mapped[str] = mapped_column(
        String(30),
        nullable=False,
        default="text",
    )

    content: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
    )

    whatsapp_message_id: Mapped[str | None] = mapped_column(
        String(255),
        nullable=True,
        unique=True,
        index=True,
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False,
    )

    conversation = relationship(
        "Conversation",
        back_populates="messages",
    )