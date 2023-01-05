from pydantic import BaseModel
from models.likes import Like, Review, Bookmark


class PaginatedList(BaseModel):
    prev: int | None
    next: int | None
    total: int | None
    items: list  # list of objects


class CountModel(BaseModel):
    count: int | None


class PaginatedLikes(PaginatedList):
    items: list[Like]


class InfoLikes(BaseModel):
    count_likes: int
    raiting: float


class PaginatedReviews(PaginatedList):
    items: list[Review]


class PaginatedBookmarks(PaginatedList):
    items: list[Bookmark]
