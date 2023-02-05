import logging

from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase

logger = logging.getLogger('uvicorn')

SQLALCHEMY_DATABASE_URL = "postgresql://admin:admin@localhost/movies"

engine_ = create_engine(SQLALCHEMY_DATABASE_URL)


class Base(DeclarativeBase):
    pass
