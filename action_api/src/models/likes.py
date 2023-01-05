from pydantic import BaseModel, UUID4, Field
from datetime import datetime
from bson import ObjectId


class PyObjectId(ObjectId):
    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, v):
        if not ObjectId.is_valid(v):
            raise ValueError('Invalid objectid')
        return str(v)

    @classmethod
    def __modify_schema__(cls, field_schema):
        field_schema.update(type='string')


class Like(BaseModel):
    """Like docs from collection likes."""

    id: PyObjectId = Field(default_factory=PyObjectId, alias='_id')
    user_id: UUID4
    movie_id: UUID4
    like: int
    created: datetime
    modified: datetime

    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}


class Review(BaseModel):
    """Review docs from collection reviews."""

    id: PyObjectId = Field(default_factory=PyObjectId, alias='_id')
    user_id: UUID4
    movie_id: UUID4
    review: str
    like: int | None = None
    created: datetime
    modified: datetime

    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}


class Bookmark(BaseModel):
    """Bookmark docs from collection bookmarks."""

    id: PyObjectId = Field(default_factory=PyObjectId, alias='_id')
    user_id: UUID4
    movie_id: UUID4
    created: datetime

    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}
