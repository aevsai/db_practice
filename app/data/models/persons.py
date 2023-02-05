from __future__ import annotations
from datetime import date

from sqlalchemy import ForeignKey, String, Integer, DATE, CHAR, func
from sqlalchemy.orm import mapped_column, Mapped

from app.database import Base
from app.utils import Updatable


class Person(Updatable, Base):
    __tablename__ = "persons"

    id: Mapped[int] = mapped_column(
        Integer, primary_key=True, index=True, unique=True, nullable=False)
    surname: Mapped[str] = mapped_column(String(80), nullable=False)
    names: Mapped[str] = mapped_column(String(160), nullable=False)
    country: Mapped[str] = mapped_column(
        CHAR(3), ForeignKey("countries.code"), nullable=False)
    birthday: Mapped[date] = mapped_column(DATE, nullable=False)
    day_of_death: Mapped[date] = mapped_column(DATE, nullable=True)
