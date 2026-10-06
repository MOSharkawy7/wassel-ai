from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.models import Customer


router = APIRouter(
    prefix="/customers",
    tags=["Customers"],
)


@router.post("/")
def create_customer(
    business_id: int,
    phone_number: str,
    name: str | None = None,
    email: str | None = None,
    notes: str | None = None,
    db: Session = Depends(get_db),
):
    customer = Customer(
        business_id=business_id,
        phone_number=phone_number,
        name=name,
        email=email,
        notes=notes,
    )

    db.add(customer)
    db.commit()
    db.refresh(customer)

    return customer