import pytest
import uuid
from http import HTTPStatus

from utils import get_items_by_user_id


@pytest.mark.asyncio
async def test_bookmarks_list(insert_bookmarks, bookmarks_docs, auth_bearer, make_request):
    header, user_id = auth_bearer

    url = '/bookmarks/list/'
    response = await make_request(url, method='GET', headers=header)

    assert response.status == HTTPStatus.OK

    response_items = response.body['items']
    response_user_id = response_items[0]['user_id']
    assert response_user_id == user_id


@pytest.mark.asyncio
async def test_bookmarks_list_paginate(insert_bookmarks, bookmarks_docs, auth_bearer, make_request):
    header, user_id = auth_bearer
    items_by_user = get_items_by_user_id(bookmarks_docs, user_id)

    url = '/bookmarks/list/'
    response = await make_request(url, method='GET', headers=header)
    res_boby = response.body

    total = res_boby['total']
    size = 20
    url = f'/bookmarks/list/?size={size}&page={total}'
    response = await make_request(url, method='GET', headers=header)
    res_boby = response.body

    assert response.status == HTTPStatus.OK

    count_items = len(res_boby['items'])
    len_docs = size * (total-1) + count_items
    assert len_docs == len(items_by_user)


@pytest.mark.asyncio
async def test_add_bookmarks_and_delete(insert_bookmarks, bookmarks_docs, auth_bearer, make_request):
    header, user_id = auth_bearer
    movie_id = str(uuid.uuid4())

    url = '/bookmarks/'
    body = {'movie_id': movie_id}
    response = await make_request(url, method='DELETE', headers=header, body=body)
    assert response.status == HTTPStatus.NOT_FOUND

    response = await make_request(url, method='POST', headers=header, body=body)
    assert response.status == HTTPStatus.OK    
    res_boby = response.body 

    assert res_boby['user_id'] == user_id
    assert res_boby['movie_id'] == movie_id

    befor_update_id = res_boby['_id']
    response = await make_request(url, method='POST', headers=header, body=body)

    assert response.status == HTTPStatus.OK
    assert response.body['_id'] == befor_update_id

    deleted_bookmark = response.body
    response = await make_request(url, method='DELETE', headers=header, body=body)
    assert response.status == HTTPStatus.OK
    assert response.body == deleted_bookmark

    response = await make_request(url, method='DELETE', headers=header, body=body)
    assert response.status == HTTPStatus.NOT_FOUND