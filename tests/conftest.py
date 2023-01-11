import asyncio
import uuid
from dataclasses import dataclass

import aiohttp
import pytest
from pymongo import MongoClient
from multidict import CIMultiDictProxy

from .settings import settings


pytest_plugins = ('tests.fixtures.docs', 
                  'tests.fixtures.auth')


@pytest.fixture
def event_loop():
    yield asyncio.get_event_loop()


def pytest_sessionfinish(session, exitstatus):
    asyncio.get_event_loop().close()


@dataclass
class HTTPResponse:
    body: dict
    headers: CIMultiDictProxy[str]
    status: int


@pytest.fixture(scope='session')
async def mondo_db():
    client = MongoClient(
        settings.mongodb_local_url, 
        uuidRepresentation='pythonLegacy',
    )
    db = client[settings.mongodb_db]
    yield db
    client.close()


@pytest.fixture(scope='session')
async def session():
    session = aiohttp.ClientSession()
    yield session
    await session.close()


@pytest.fixture
def make_request(session):
    async def inner(uri: str,
                    method: str = 'GET',
                    params: dict | None = None,
                    headers: dict | None = None,
                    body: dict | None = None) -> HTTPResponse:
        params = params or {}
        headers = headers or {}
        body = body or {}
        url = settings.service_url + uri

        #add X-Request-Id
        request_id = str(uuid.uuid4())
        headers['X-Request-Id'] = request_id

        if method.upper() == 'GET':
            session_method = session.get
        elif method.upper() == 'POST':
            session_method = session.post
        elif method.upper() == 'PATCH':
            session_method = session.patch
        elif method.upper() == 'DELETE':
            session_method = session.delete
        else:
            raise ValueError('Unknown method')
        async with session_method(url, params=params, headers=headers, json=body) as response:
            return HTTPResponse(
                body=await response.json(),
                headers=response.headers,
                status=response.status,
            )
    return inner
