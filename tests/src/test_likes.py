import pytest
import uuid
from http import HTTPStatus

from utils import get_items_by_movie_id, get_items_by_user_id


@pytest.mark.asyncio
async def test_likes_list(insert_likes, likes_docs, auth_bearer, make_request):
    header, user_id = auth_bearer
    movie_id = str(likes_docs[0]['movie_id'])

    url = '/likes/list/'
    response = await make_request(url, method='GET', headers=header)

    assert response.status == HTTPStatus.OK

    response_items = response.body['items']
    response_user_id = response_items[0]['user_id']
    assert response_user_id == user_id

    url = f'/likes/list/?movie_id={movie_id}'
    response = await make_request(url, method='GET', headers=header)

    assert response.status == HTTPStatus.OK

    response_items = response.body['items']
    response_movie_id = response_items[0]['movie_id']
    assert response_movie_id == movie_id    


@pytest.mark.asyncio
async def test_likes_list_paginate(insert_likes, likes_docs, auth_bearer, make_request):
    header, user_id = auth_bearer
    items_by_user = get_items_by_user_id(likes_docs, user_id)

    url = '/likes/list/'
    response = await make_request(url, method='GET', headers=header)
    res_boby = response.body

    total = res_boby['total']
    size = 20
    url = f'/likes/list/?size={size}&page={total}'
    response = await make_request(url, method='GET', headers=header)
    res_boby = response.body

    assert response.status == HTTPStatus.OK

    count_items = len(res_boby['items'])
    len_docs = size * (total-1) + count_items
    assert len_docs == len(items_by_user)


@pytest.mark.asyncio
async def test_likes_id(insert_likes, likes_docs, auth_bearer, make_request):    
    header, user_id = auth_bearer

    url = '/likes/list/'
    response = await make_request(url, method='GET', headers=header)

    like = response.body['items'][1]
    like_id = like['_id']
    url = f'/likes/{like_id}'
    response = await make_request(url, method='GET', headers=header)

    assert response.status == HTTPStatus.OK

    assert response.body == like


@pytest.mark.asyncio
async def test_likes_info(insert_likes, likes_docs, auth_bearer, make_request):    
    header, user_id = auth_bearer
    movie_id = str(likes_docs[1]['movie_id'])
    items_by_movie = get_items_by_movie_id(likes_docs, movie_id)
    cnt = len(items_by_movie)
    avg = 0
    for item in items_by_movie:
        avg += item['like']
    avg = round(avg / cnt, 1)

    url = f'/likes/info/?movie_id={movie_id}'
    response = await make_request(url, method='GET', headers=header)
    res_boby = response.body

    assert response.status == HTTPStatus.OK

    assert res_boby['count_likes'] == cnt
    assert res_boby['raiting'] == avg


@pytest.mark.asyncio
async def test_add_lake_and_delete(insert_likes, likes_docs, auth_bearer, make_request):
    header, user_id = auth_bearer
    movie_id = str(uuid.uuid4())

    url = '/likes/'
    body = {'movie_id': movie_id, 'like': 10}
    response = await make_request(url, method='DELETE', headers=header, body=body)
    assert response.status == HTTPStatus.NOT_FOUND

    response = await make_request(url, method='POST', headers=header, body=body)
    assert response.status == HTTPStatus.OK
    
    res_boby = response.body
    assert res_boby['like'] == 10

    assert res_boby['user_id'] == user_id
    assert res_boby['movie_id'] == movie_id

    befor_update_id = res_boby['_id']
    body = {'movie_id': movie_id, 'like': 5}
    response = await make_request(url, method='POST', headers=header, body=body)
    assert response.status == HTTPStatus.OK

    assert response.body['like'] == 5
    assert response.body['_id'] == befor_update_id

    deleted_like = response.body
    response = await make_request(url, method='DELETE', headers=header, body=body)
    assert response.status == HTTPStatus.OK
    assert response.body == deleted_like

    response = await make_request(url, method='DELETE', headers=header, body=body)
    assert response.status == HTTPStatus.NOT_FOUND

