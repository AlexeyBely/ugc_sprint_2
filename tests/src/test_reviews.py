import pytest
import uuid
from http import HTTPStatus

from utils import get_items_by_user_id


@pytest.mark.asyncio
async def test_reviews_list(insert_reviews, reviews_docs, auth_bearer, make_request):
    header, user_id = auth_bearer
    movie_id = str(reviews_docs[0]['movie_id'])

    url = '/reviews/list/'
    response = await make_request(url, method='GET', headers=header)

    assert response.status == HTTPStatus.OK

    response_items = response.body['items']
    response_user_id = response_items[0]['user_id']
    assert response_user_id == user_id

    url = f'/reviews/list/?movie_id={movie_id}'
    response = await make_request(url, method='GET', headers=header)

    assert response.status == HTTPStatus.OK

    response_items = response.body['items']
    response_movie_id = response_items[0]['movie_id']
    assert response_movie_id == movie_id


@pytest.mark.asyncio
async def test_reviews_list_paginate(insert_reviews, reviews_docs, auth_bearer, make_request):
    header, user_id = auth_bearer
    items_by_user = get_items_by_user_id(reviews_docs, user_id)

    url = '/reviews/list/'
    response = await make_request(url, method='GET', headers=header)
    res_boby = response.body

    total = res_boby['total']
    size = 20
    url = f'/reviews/list/?size={size}&page={total}'
    response = await make_request(url, method='GET', headers=header)
    res_boby = response.body

    assert response.status == HTTPStatus.OK

    count_items = len(res_boby['items'])
    len_docs = size * (total-1) + count_items
    assert len_docs == len(items_by_user)


@pytest.mark.asyncio
async def test_review_id(insert_reviews, reviews_docs, auth_bearer, make_request):    
    header, user_id = auth_bearer

    url = '/reviews/list/'
    response = await make_request(url, method='GET', headers=header)

    review = response.body['items'][1]
    review_id = review['_id']
    url = f'/reviews/{review_id}'
    response = await make_request(url, method='GET', headers=header)

    assert response.status == HTTPStatus.OK

    assert response.body == review


@pytest.mark.asyncio
async def test_add_review_and_delete(insert_reviews, reviews_docs, auth_bearer, make_request):
    header, user_id = auth_bearer
    movie_id = str(uuid.uuid4())

    url = '/reviews/'
    body = {'movie_id': movie_id, 'review': 'my review'}
    response = await make_request(url, method='DELETE', headers=header, body=body)
    assert response.status == HTTPStatus.NOT_FOUND

    response = await make_request(url, method='POST', headers=header, body=body)
    assert response.status == HTTPStatus.OK
    
    res_boby = response.body
    assert res_boby['review'] == 'my review'

    assert res_boby['user_id'] == user_id
    assert res_boby['movie_id'] == movie_id

    befor_update_id = res_boby['_id']
    body = {'movie_id': movie_id, 'review': 'my update review'}
    response = await make_request(url, method='POST', headers=header, body=body)
    assert response.status == HTTPStatus.OK

    assert response.body['review'] == 'my update review'
    assert response.body['_id'] == befor_update_id

    deleted_review = response.body
    response = await make_request(url, method='DELETE', headers=header, body=body)
    assert response.status == HTTPStatus.OK
    assert response.body == deleted_review

    response = await make_request(url, method='DELETE', headers=header, body=body)
    assert response.status == HTTPStatus.NOT_FOUND