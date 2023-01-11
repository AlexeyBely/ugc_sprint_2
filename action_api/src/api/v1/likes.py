from http import HTTPStatus
from fastapi import APIRouter, Depends, HTTPException, Body, status
from fastapi.responses import Response
import uuid

from models.response import PaginatedLikes, InfoLikes
from models.request import IdMovie, PaginatedParams, AddLike, IdMovieInfo
from models.likes import Like
from services_abc.likes_abc import BaseLikesService
from services_abc.composition_services import get_likes_service

from api.v1.auth import TokenData, authenticate
import api.messages as messages

router = APIRouter()


@router.post(
    '/',
    response_model=Like,
    summary='Добавить или изменить лайк',
    description='Добавить (изменить) лайк с рейтенгом к кинопроизведению с movie_id',
    response_description='Полная информация по лайку',
)
async def add_like(
    add_like: AddLike = Body(...),
    likes_service: BaseLikesService = Depends(get_likes_service),
    token_data: TokenData = Depends(authenticate),
) -> Like:
    """Add new like."""
    user_id = uuid.UUID(token_data.user)
    like = await likes_service.add_like(user_id, add_like.movie_id, add_like.like)
    if not like:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail=messages.FAULT_BOBY)
    return Like(**like)


@router.delete(
    '/',
    response_model=Like,
    summary='Удалить лайк',
    description='Удалить лайк к кинопроизведению с movie_id',
    response_description='Полная информация по удаленному лайку',
)
async def delete_like(
    add_like: AddLike = Body(...),
    likes_service: BaseLikesService = Depends(get_likes_service),
    token_data: TokenData = Depends(authenticate),
) -> Like:
    """Delete like."""
    user_id = uuid.UUID(token_data.user)
    result = await likes_service.delete_like(user_id, add_like.movie_id)
    if result is None:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail=messages.FAULT_BOBY)
    return Like(**result)


@router.get(
    '/{id}',
    response_model=Like,
    summary='Информация по лайку',
    description='Поиск лайка по _id',
    response_description='Полная информация по лайку',
)
async def like_details(
    id: str,
    likes_service: BaseLikesService = Depends(get_likes_service),
    token_data: TokenData = Depends(authenticate),
) -> Like:
    """Show a like by its UUID."""
    like = await likes_service.id_details(id)
    if not like:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, 
                            detail=messages.LIKE_NOT_FOUND)
    return Like(**like)


@router.get(
    '/list/',
    response_model=PaginatedLikes,
    summary='Список лайков',
    description='Поиск лайков по user_id или movie_id',
    response_description='Список информации по лайкам с паджинацией',
)
async def likes_list(
    query_movie_id: IdMovie = Depends(IdMovie),
    paginate: PaginatedParams = Depends(PaginatedParams),
    likes_service: BaseLikesService = Depends(get_likes_service),
    token_data: TokenData = Depends(authenticate),
) -> PaginatedLikes:
    """Show likes from user_id or movie_id."""
    user_id = uuid.UUID(token_data.user)
    movie_id = query_movie_id.movie_id
    likes = await likes_service.read_likes(user_id,
                                           movie_id, 
                                           paginate.size, 
                                           paginate.page)
    if not likes:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail=messages.FAULT_BOBY)
    return PaginatedLikes(**likes)


@router.get(
    '/info/',
    response_model=InfoLikes,
    summary='информация по лайкам',
    description='Информация по кинопроизведению movie_id',
    response_description='Количество рейтинг лайков',
)
async def likes_info(
    query_movie_id: IdMovieInfo = Depends(IdMovieInfo),
    likes_service: BaseLikesService = Depends(get_likes_service),
    token_data: TokenData = Depends(authenticate),
) -> InfoLikes:
    """Show likes from user_id or movie_id."""
    movie_id = query_movie_id.movie_id
    info = await likes_service.info_likes(movie_id)
    if not info:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail=messages.FAULT_BOBY)
    return InfoLikes(**info)
