from app.data.access.dao import DAO
from app.data.models.movies import Movie


class MovieDAO(DAO[Movie]):

    def __init__(self) -> None:
        super().__init__(Movie)
