from http import HTTPStatus
from math import ceil

import pytest


@pytest.mark.asyncio
async def test_likes_list(insert_likes, likes_docs, auth_bearer, make_request):
    url = '/likes/list/'
    #body = {'email': 'refresh@mail.ru', 'password': 'refresh_token', 'full_name': 'refresh_token'}
    header, user_id = auth_bearer

    response = await make_request(url, method='GET', headers=header)
    items = response.body['items']
    response_user_id = items[0]['user_id']
    assert response_user_id == str(user_id)




