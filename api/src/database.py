from typing import Annotated, Any, Generator
from fastapi import Depends
from sqlmodel import create_engine, Session
from .config import settings

engine = create_engine(settings.database_url)

def get_session() -> Generator[Session, Any, None]:
    with Session(engine) as session:
        yield session

SessionDep = Annotated[Session, Depends(get_session)]

