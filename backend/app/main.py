from fastapi import FastAPI
from sqlalchemy import text

from app.core.config import settings
from app.db.session import engine
from app.models import (
    Business,
    Customer,
    Product,
    Conversation,
    Message,
)

from app.api.routes import (
    businesses,
    customers,
    conversations,
    messages,
)
from app.models.base import Base

from app.api.routes import businesses, customers, conversations


app = FastAPI(
    title=settings.app_name,
    version=settings.app_version,
    debug=settings.debug,
)


app.include_router(
    businesses.router,
    prefix="/api",
)

app.include_router(
    customers.router,
    prefix="/api",
)

app.include_router(
    conversations.router,
    prefix="/api",
)

app.include_router(
    messages.router,
    prefix="/api",
)

@app.on_event("startup")
def create_tables():
    Base.metadata.create_all(bind=engine)


@app.get("/health")
def health_check():
    return {
        "status": "ok",
        "service": "wassel-ai",
    }


@app.get("/health/database")
def database_health_check():
    with engine.connect() as connection:
        connection.execute(text("SELECT 1"))

    return {
        "status": "ok",
        "database": "connected",
    }
    