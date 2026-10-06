from datetime import datetime

from sqlalchemy import DateTime, String, Text, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base


class Business(Base):
    __tablename__ = "businesses"

    id: Mapped[int] = mapped_column(
        primary_key=True,
        autoincrement=True,
    )

    name: Mapped[str] = mapped_column(
        String(150),
        nullable=False,
    )

    description: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
    )

    phone_number: Mapped[str | None] = mapped_column(
        String(30),
        nullable=True,
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False,
    )

    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False,
    )

    customers: Mapped[list["Customer"]] = relationship(
        back_populates="business",
        cascade="all, delete-orphan",
    )

    products: Mapped[list["Product"]] = relationship(
        back_populates="business",
        cascade="all, delete-orphan",
    )

    conversations: Mapped[list["Conversation"]] = relationship(
        back_populates="business",
        cascade="all, delete-orphan",
    )