import pytest
import uuid
import random

from ..testdata.collection_data import (USER_COUNT, MOVIE_COUNT, DOCS_IN_COLL_COUNT,
                                      map_collections)
from ..settings import settings


# fixture random user_ids, movie_ids
@pytest.fixture(scope='session')
def user_movie_ids() -> tuple:
    user_ids = [uuid.uuid4() for x in range(USER_COUNT)]
    movie_ids = [uuid.uuid4() for x in range(MOVIE_COUNT)]
    return user_ids, movie_ids


# fixture create likes docs
@pytest.fixture(scope='session')
def likes_docs(user_movie_ids) -> list:
    user_ids, movie_ids = user_movie_ids
    values = []
    for i in range(0, DOCS_IN_COLL_COUNT):
        doc = map_collections['likes'](
            random.choice(user_ids),
            random.choice(movie_ids),
        )
        values.append(doc)
    return values


# fixture create reviews docs
@pytest.fixture(scope='session')
def reviews_docs(user_movie_ids) -> list:
    user_ids, movie_ids = user_movie_ids
    values = []
    for i in range(0, DOCS_IN_COLL_COUNT):
        doc = map_collections['reviews'](
            random.choice(user_ids),
            random.choice(movie_ids),
        )
        values.append(doc)
    return values


# fixture create bookmarks docs
@pytest.fixture(scope='session')
def bookmarks_docs(user_movie_ids) -> list:
    user_ids, movie_ids = user_movie_ids
    values = []
    for i in range(0, DOCS_IN_COLL_COUNT):
        doc = map_collections['bookmarks'](
            random.choice(user_ids),
            random.choice(movie_ids),
        )
        values.append(doc)
    return values


@pytest.fixture(scope='session')
def insert_likes(likes_docs, mondo_db):
    collection = mondo_db[settings.mongodb_coll_likes]    
    collection.insert_many(likes_docs)


@pytest.fixture(scope='session')
def insert_reviews(reviews_docs, mondo_db):
    collection = mondo_db[settings.mongodb_coll_reviews]
    collection.insert_many(reviews_docs)


@pytest.fixture(scope='session')
def insert_bookmarks(bookmarks_docs, mondo_db):
    collection = mondo_db[settings.mongodb_coll_bookmarks]
    collection.insert_many(bookmarks_docs)