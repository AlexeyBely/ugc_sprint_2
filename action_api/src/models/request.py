from pydantic import BaseModel, Field, UUID4
from fastapi import Query

from core.config import api_settings


class PaginatedParams(BaseModel):
    size: int = Query(
        api_settings.default_page_size,
        description='page[size]',
        ge=1,
        le=api_settings.max_page_size,
    )
    page: int = Query(1, description='page[number]', ge=1)


class IdMovie(BaseModel):
    movie_id: UUID4 | None = Query(None, description='movie_id or null')


class AddLike(BaseModel):
    movie_id: UUID4 | None = Field(None, description='movie_id')
    like: int = Field(1, description='reiting', ge=1, le=10)


class AddReview(BaseModel):
    movie_id: UUID4 | None = Field(None, description='movie_id')
    review: str = Field(description='text review')


class AddBookmark(BaseModel):
    movie_id: UUID4 | None = Field(None, description='movie_id')
