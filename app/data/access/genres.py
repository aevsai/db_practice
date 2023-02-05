from app.data.access.dao import DAO
from app.data.models.genres import Genres


class GenresDAO(DAO[Genres]):

    def __init__(self) -> None:
        super().__init__(Genres)
