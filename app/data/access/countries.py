from typing import Any, Optional
from app.data.access.dao import DAO
from app.data.models.countries import Country
from sqlalchemy.sql.expression import update, delete
from sqlalchemy.orm import Session
from app.database import engine_


class CountryDAO(DAO[Country]):

    def __init__(self) -> None:
        super().__init__(Country)

    def update(self, id: Any, values: dict) -> Optional[dict]:

        with Session(engine_) as session:
            with session.begin():

                raws = session.scalars(
                    update(self.model)
                    .returning(self.model)
                    .where(self.model.code == id)
                    .values(values)
                    .execution_options(
                        synchronize_session="evaluate"
                    )
                )

                return raws.one_or_none().__dict__

    def delete(self, id: str) -> None:

        with Session(engine_) as session:
            with session.begin():

                session.execute(
                    delete(self.model)
                    .returning(self.model)
                    .where(self.model.code == id)
                    .execution_options(
                        synchronize_session="evaluate"
                    )
                )

                return None
