from abc import ABC, abstractmethod
from typing import Any, Generic, List, Optional, Sequence, Type, TypeVar

from sqlalchemy.sql.expression import select, update, insert, delete
from sqlalchemy.orm import Session
from app.database import engine_

ModelT = TypeVar('ModelT')


class DAO(Generic[ModelT], ABC):

    @abstractmethod
    def __init__(self, model: Type) -> None:
        self.model = model

    def get(self, id: Any) -> Optional[dict]:
        with Session(engine_) as session:
            with session.begin():
                raw = session.get(self.model, id)
                raw = raw.__dict__ if raw else {}
                return raw

    def get_all(self, filters: Optional[dict] = None, offset: Optional[int] = None, limit: Optional[int] = None) -> Sequence[dict]:

        with Session(engine_) as session:
            with session.begin():
                stmt = select(self.model)

                if filters:
                    for attr, value in filters.items():
                        if value:
                            stmt = stmt.filter(
                                getattr(self.model, attr).like("%%%s%%" % value))

                raws = session.scalars(
                    stmt
                    .offset(offset)
                    .limit(limit)
                )
                data = [i.__dict__ for i in raws.all()]
                _ = [i.pop('_sa_instance_state') for i in data]
                return data

    def create(self, values: dict) -> Optional[dict]:

        with Session(engine_) as session:
            with session.begin():
                raw = session.scalars(
                    insert(self.model)
                    .returning(self.model)
                    .values(values)
                    .execution_options(
                        synchronize_session="evaluate"
                    )
                ).one_or_none()

                return raw.__dict__ if raw else {}

    def update(self, id: Any, values: dict) -> Optional[dict]:

        with Session(engine_) as session:
            with session.begin():
                raw = session.scalars(
                    update(self.model)
                    .returning(self.model)
                    .where(self.model.id == id)
                    .values(values)
                    .execution_options(
                        synchronize_session="evaluate"
                    )
                ).one_or_none()

                return raw.__dict__ if raw else {}

    def delete(self, id: Any) -> None:

        with Session(engine_) as session:
            with session.begin():
                session.execute(
                    delete(self.model)
                    .where(self.model.id == id)
                    .execution_options(
                        synchronize_session="evaluate"
                    )
                )

                return None
