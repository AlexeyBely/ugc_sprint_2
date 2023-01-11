from http import HTTPStatus
from fastapi import APIRouter, Depends, HTTPException, Body, status
from fastapi.responses import Response
import uuid

from models.response import PaginatedReviews
from models.request import IdMovie, PaginatedParams, AddReview
from models.likes import Review
from services_abc.reviews_abc import BaseReviewsService
from services_abc.composition_services import get_reviews_service

from api.v1.auth import TokenData, authenticate
import api.messages as messages

router = APIRouter()


@router.post(
    '/',
    response_model=Review,
    summary='Добавить или изменить рецензию',
    description='Добавить (изменить) рецензию к кинопроизведению с movie_id',
    response_description='Полная информация по рецензию',
)
async def add_review(
    add_review: AddReview = Body(...),
    review_service: BaseReviewsService = Depends(get_reviews_service),
    token_data: TokenData = Depends(authenticate),
) -> Review:
    """Add new review."""
    user_id = uuid.UUID(token_data.user)
    review = await review_service.add_review(user_id, 
                                             add_review.movie_id, 
                                             add_review.review)
    if not review:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail=messages.FAULT_BOBY)
    return Review(**review)


@router.delete(
    '/',
    response_model=Review,
    summary='Удалить рецензию',
    description='Удалить рецензию к кинопроизведению с movie_id',
    response_description='Полная информация по удаленной рецензии',
)
async def delete_review(
    add_review: AddReview = Body(...),
    review_service: BaseReviewsService = Depends(get_reviews_service),
    token_data: TokenData = Depends(authenticate),
) -> Review:
    """Delete review."""
    user_id = uuid.UUID(token_data.user)
    result = await review_service.delete_review(user_id, add_review.movie_id)
    if result is None:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail=messages.FAULT_BOBY)
    return Review(**result)


@router.get(
    '/{id}',
    response_model=Review,
    summary='Информация по рецензии',
    description='Поиск лайка по _id',
    response_description='Полная информация по лайку',
)
async def review_details(
    id: str,
    review_service: BaseReviewsService = Depends(get_reviews_service),
    token_data: TokenData = Depends(authenticate),
) -> Review:
    """Show a review by its UUID."""
    review = await review_service.id_details(id)
    if not review:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, 
                            detail=messages.REVIEW_NOT_FOUND)
    return Review(**review)


@router.get(
    '/list/',
    response_model=PaginatedReviews,
    summary='Список рецензий',
    description='Поиск рецензий по user_id или movie_id',
    response_description='Список информации по рецензиям с паджинацией',
)
async def reviews_list(
    query_movie_id: IdMovie = Depends(IdMovie),
    paginate: PaginatedParams = Depends(PaginatedParams),
    review_service: BaseReviewsService = Depends(get_reviews_service),
    token_data: TokenData = Depends(authenticate),
) -> PaginatedReviews:
    """Show reviews from user_id or movie_id."""
    user_id = uuid.UUID(token_data.user)
    movie_id = query_movie_id.movie_id
    reviews = await review_service.read_reviews(
        user_id, movie_id, paginate.size, paginate.page
    )
    if not reviews:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail=messages.FAULT_BOBY)
    return PaginatedReviews(**reviews)
