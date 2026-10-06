from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.models import Conversation


router = APIRouter(
    prefix="/conversations",
    tags=["Conversations"],
)


@router.post("/")
def create_conversation(
    business_id: int,
    customer_id: int,
    db: Session = Depends(get_db),
):
    conversation = Conversation(
        business_id=business_id,
        customer_id=customer_id,
    )

    db.add(conversation)
    db.commit()
    db.refresh(conversation)

    return conversation