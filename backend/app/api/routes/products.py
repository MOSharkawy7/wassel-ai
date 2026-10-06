from decimal import Decimal

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.models import Product


router = APIRouter(
    prefix="/products",
    tags=["Products"],
)


@router.post("/")
def create_product(
    business_id: int,
    name: str,
    price: Decimal,
    description: str | None = None,
    currency: str = "EGP",
    is_available: bool = True,
    db: Session = Depends(get_db),
):
    product = Product(
        business_id=business_id,
        name=name,
        description=description,
        price=price,
        currency=currency,
        is_available=is_available,
    )

    db.add(product)
    db.commit()
    db.refresh(product)

    return product