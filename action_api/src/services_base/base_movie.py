from abc import ABC, abstractmethod


class BaseMovieService(ABC):
    @abstractmethod
    async def add_frame_movie(self, user_id: str, movie_id: str, frame: int) -> None:
        """Save movie frame in database."""
        pass
