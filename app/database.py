from typing import Annotated, Iterator

from fastapi import Depends
from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker

from app.core.config import settings
from app.models import Base

engine = create_engine(settings.DATABASE_URL)

SessionMaker = sessionmaker(engine)

def get_db() -> Iterator[Session]:
    db = SessionMaker()
    try:
        yield db
    finally:
        db.close()


DBSession = Annotated[Session, Depends(get_db())]
