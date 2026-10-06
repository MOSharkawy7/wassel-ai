from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.models import Message


router = APIRouter(
    prefix="/messages",
    tags=["Messages"],
)


@router.post("/")
def create_message(
    conversation_id: int,
    direction: str,
    sender_type: str,
    content: str | None = None,
    message_type: str = "text",
    whatsapp_message_id: str | None = None,
    db: Session = Depends(get_db),
):
    message = Message(
        conversation_id=conversation_id,
        direction=direction,
        sender_type=sender_type,
        message_type=message_type,
        content=content,
        whatsapp_message_id=whatsapp_message_id,
    )

    db.add(message)
    db.commit()
    db.refresh(message)

    return message