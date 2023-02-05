from __future__ import annotations

from sqlalchemy import String, Integer, func
from sqlalchemy.orm import mapped_column, Mapped

from app.database import Base
from app.utils import Updatable


class Genres(Updatable, Base):
    __tablename__ = "genres"

    id: Mapped[int] = mapped_column(
        Integer, primary_key=True, index=True, unique=True, nullable=False)
    name: Mapped[str] = mapped_column(String(30), nullable=False)
