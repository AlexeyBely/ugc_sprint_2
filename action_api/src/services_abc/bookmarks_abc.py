from abc import ABC, abstractmethod
import uuid


class BaseBookmarksService(ABC):
    @abstractmethod
    async def read_bookmarks(
        self, user_id: uuid.UUID | None = None, size: int = 1, page: int = 20
    ) -> dict:
        """
        Load bookmarks from user_id."""
        pass

    @abstractmethod
    async def add_bookmark(self, user_id: uuid.UUID, movie_id: uuid.UUID) -> dict:
        """Add new bookmark."""
        pass

    @abstractmethod
    async def delete_bookmark(self, user_id: uuid.UUID, movie_id: uuid.UUID) -> bool:
        """
        delete the bookmark.                
        return False - ok, True - fault
        """
        pass
