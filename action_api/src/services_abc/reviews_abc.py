from abc import ABC, abstractmethod
import uuid


class BaseReviewsService(ABC):
    @abstractmethod
    async def id_details(self, review_id: str) -> dict:
        """Load details review doc."""
        pass

    @abstractmethod
    async def read_reviews(
        self,
        user_id: uuid.UUID,
        movie_id: uuid.UUID | None = None,
        size: int = 1,
        page: int = 20,
    ) -> dict:
        """
        Load review from user_id or movie_id.
        
        If movie_id equal None, then read reviews by user_id. Or
        movie_id not equal None, then read reviews by movie_id
        """
        pass

    @abstractmethod
    async def add_review(self, user_id: uuid.UUID, movie_id: uuid.UUID, 
                         text: str) -> dict:
        """Add new review."""
        pass

    @abstractmethod
    async def delete_review(self, user_id: uuid.UUID, movie_id: uuid.UUID) -> bool:
        """
        delete the review.
        
        return False - ok, True - fault
        """
        pass
