from http import HTTPStatus
from fastapi import APIRouter, Depends, HTTPException, Body, status
from fastapi.responses import Response
import uuid

from models.response import PaginatedBookmarks
from models.request import IdMovie, PaginatedParams, AddBookmark
from models.likes import Bookmark
from services_abc.bookmarks_abc import BaseBookmarksService
from services_abc.composition_services import get_bookmarks_service

from api.v1.auth import TokenData, authenticate
import api.messages as messages

router = APIRouter()


@router.post(
    '/',
    response_model=Bookmark,
    summary='Добавить закладку',
    description='Добавить закладку к кинопроизведению с movie_id',
    response_description='Полная информация по закладке',
)
async def add_bookmark(
    add_bm: AddBookmark = Body(...),
    bm_service: BaseBookmarksService = Depends(get_bookmarks_service),
    token_data: TokenData = Depends(authenticate),
) -> Bookmark:
    """Add new bookmark."""
    user_id = uuid.UUID(token_data.user)
    bookmark = await bm_service.add_bookmark(user_id, add_bm.movie_id)
    if not bookmark:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail=messages.FAULT_BOBY)
    return Bookmark(**bookmark)


@router.delete(
    '/',
    response_model=Bookmark,
    summary='Удалить закладку',
    description='Удалить закладку к кинопроизведению с movie_id',
    response_description='Полная информация по удаленной закладке',
)
async def delete_bookmark(
    add_bm: AddBookmark = Body(...),
    bm_service: BaseBookmarksService = Depends(get_bookmarks_service),
    token_data: TokenData = Depends(authenticate),
) -> Bookmark:
    """Delete bookmark."""
    user_id = uuid.UUID(token_data.user)
    result = await bm_service.delete_bookmark(user_id, add_bm.movie_id)
    if result is None:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail=messages.FAULT_BOBY)
    return Bookmark(**result)


@router.get(
    '/list/',
    response_model=PaginatedBookmarks,
    summary='Список закладок',
    description='Поиск закладок по user_id',
    response_description='Список информации по закладкам с паджинацией',
)
async def reviews_list(
    paginate: PaginatedParams = Depends(PaginatedParams),
    bm_service: BaseBookmarksService = Depends(get_bookmarks_service),
    token_data: TokenData = Depends(authenticate),
) -> PaginatedBookmarks:
    """Show reviews from user_id or movie_id."""
    user_id = uuid.UUID(token_data.user)
    bookmarks = await bm_service.read_bookmarks(user_id, paginate.size, paginate.page)
    if not bookmarks:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail=messages.FAULT_BOBY)
    return PaginatedBookmarks(**bookmarks)
