from http import HTTPStatus

from fastapi import APIRouter, Depends

from models.response_models import Response
from models.request_models import FrameAdd
from services_base.composition_services import get_movie_service
from services_base.base_movie import BaseMovieService
from api.v1.auth import TokenData, authenticate

router = APIRouter()


@router.post('/add', response_model=Response, description='Add a frame to the movie')
async def add_frame(
    frame: FrameAdd,
    frame_service: BaseMovieService = Depends(get_movie_service),
    token_data: TokenData = Depends(authenticate),
) -> Response:
    """Add a frame to the movie."""
    user_id = token_data.user
    result = await frame_service.add_frame_movie(
        user_id=user_id, movie_id=frame.movie_id, frame=frame.frame
    )
    return result
