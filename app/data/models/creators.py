from __future__ import annotations

from sqlalchemy import String, Integer, NUMERIC
from sqlalchemy.orm import mapped_column, Mapped

from app.database import Base
from app.utils import Updatable


class Creator(Updatable, Base):
    __tablename__ = "creators"

    id: Mapped[int] = mapped_column(
        Integer, primary_key=True, index=True, unique=True, nullable=False)
    movie: Mapped[str] = mapped_column(NUMERIC(6), nullable=False)
    person: Mapped[int] = mapped_column(Integer, nullable=False)
    job_title: Mapped[str] = mapped_column(String(80), nullable=False)
    role: Mapped[str] = mapped_column(String(80), nullable=False)
