from app.data.access.dao import DAO
from app.data.models.creators import Creator


class CreatorDAO(DAO[Creator]):

    def __init__(self) -> None:
        super().__init__(Creator)
