from pydantic import BaseModel


class FrameAdd(BaseModel):
    movie_id: str
    frame: int
