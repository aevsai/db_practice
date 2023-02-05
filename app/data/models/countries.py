from __future__ import annotations

from sqlalchemy import String, CHAR
from sqlalchemy.orm import mapped_column, Mapped

from app.database import Base
from app.utils import Updatable


class Country(Updatable, Base):
    __tablename__ = "countries"

    code: Mapped[str] = mapped_column(
        CHAR(3), primary_key=True, index=True, unique=True, nullable=False)
    name: Mapped[str] = mapped_column(String(80), nullable=False)
