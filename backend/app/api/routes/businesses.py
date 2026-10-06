from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.models import Business


router = APIRouter(
    prefix="/businesses",
    tags=["Businesses"],
)


@router.post("/")
def create_business(
    name: str,
    description: str | None = None,
    phone_number: str | None = None,
    db: Session = Depends(get_db),
):
    business = Business(
        name=name,
        description=description,
        phone_number=phone_number,
    )

    db.add(business)
    db.commit()
    db.refresh(business)

    return business