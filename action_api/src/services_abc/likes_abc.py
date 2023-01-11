from abc import ABC, abstractmethod
import uuid


class BaseLikesService(ABC):
    @abstractmethod
    async def id_details(self, like_id: str) -> dict | None:
        """Load details like doc."""
        pass

    @abstractmethod
    async def read_likes(
        self,
        user_id: uuid.UUID,
        movie_id: uuid.UUID | None = None,
        size: int = 1,
        page: int = 20,
    ) -> dict:
        """
        Load likes from user_id or movie_id.
        
        If movie_id equal None, then read likes by user_id. Or
        movie_id not equal None, then read likes by movie_id.
        """
        pass

    @abstractmethod
    async def add_like(self, user_id: uuid.UUID, movie_id: uuid.UUID, like: int) -> dict:
        """Add new like."""
        pass

    @abstractmethod
    async def delete_like(self, user_id: uuid.UUID, movie_id: uuid.UUID) -> dict | None:
        """
        Delete the like.
        
        return deleted like
        """
        pass

    @abstractmethod
    async def info_likes(self, movie_id: uuid.UUID) -> dict:
        """info likes."""
        pass
