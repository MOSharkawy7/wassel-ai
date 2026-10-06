from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.models import (
    Business,
    Customer,
    Conversation,
    Message,
    Product,
)
from app.services.ai_service import generate_ai_response


router = APIRouter(
    prefix="/ai",
    tags=["AI"],
)


@router.post("/reply")
def generate_reply(
    conversation_id: int,
    message: str,
    db: Session = Depends(get_db),
):
    conversation = (
        db.query(Conversation)
        .filter(Conversation.id == conversation_id)
        .first()
    )

    if not conversation:
        raise HTTPException(
            status_code=404,
            detail="Conversation not found",
        )

    business = (
        db.query(Business)
        .filter(Business.id == conversation.business_id)
        .first()
    )

    customer = (
        db.query(Customer)
        .filter(Customer.id == conversation.customer_id)
        .first()
    )

    if not business or not customer:
        raise HTTPException(
            status_code=404,
            detail="Business or customer not found",
        )

    products = (
        db.query(Product)
        .filter(Product.business_id == business.id)
        .all()
    )

    customer_message = Message(
        conversation_id=conversation.id,
        direction="inbound",
        sender_type="customer",
        message_type="text",
        content=message,
    )

    db.add(customer_message)
    db.commit()

    ai_response = generate_ai_response(
        business=business,
        customer=customer,
        conversation=conversation,
        message=message,
        products=products,
    )

    assistant_message = Message(
        conversation_id=conversation.id,
        direction="outbound",
        sender_type="ai",
        message_type="text",
        content=ai_response,
    )

    db.add(assistant_message)
    db.commit()
    db.refresh(assistant_message)

    return {
        "conversation_id": conversation.id,
        "customer_message": message,
        "ai_response": ai_response,
        "message_id": assistant_message.id,
    }