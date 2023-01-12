import pytest
from http import HTTPStatus


@pytest.mark.asyncio
async def test_bookmarks_list(insert_likes, likes_docs, auth_bearer, make_request):
    header, user_id = auth_bearer

    url = '/likes/list/'
    response = await make_request(url, method='GET')
    assert response.status == HTTPStatus.FORBIDDEN

    response = await make_request(url, method='GET', headers=header)
    assert response.status == HTTPStatus.OK
