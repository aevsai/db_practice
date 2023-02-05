from __future__ import annotations

from sqlalchemy import ForeignKey, String, CHAR, NUMERIC, TIME, Integer
from sqlalchemy.orm import mapped_column, Mapped

from app.database import Base
from app.utils import Updatable


class Movie(Updatable, Base):
    __tablename__ = "movies"

    id: Mapped[int] = mapped_column(
        NUMERIC(6), primary_key=True, index=True, unique=True, nullable=False)
    name: Mapped[str] = mapped_column(String(50), nullable=False)
    studio: Mapped[str] = mapped_column(String(50), nullable=False)
    year: Mapped[int] = mapped_column(NUMERIC(4), nullable=False)
    country: Mapped[str] = mapped_column(
        CHAR(3), ForeignKey("countries.code"), nullable=False)
    duration: Mapped[str] = mapped_column(TIME, nullable=False)
    genre: Mapped[str] = mapped_column(
        Integer, ForeignKey("genres.id"), nullable=False)
