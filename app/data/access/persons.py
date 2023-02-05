from app.data.access.dao import DAO
from app.data.models.persons import Person


class PersonDAO(DAO[Person]):

    def __init__(self) -> None:
        super().__init__(Person)
