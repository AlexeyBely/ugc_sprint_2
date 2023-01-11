import random
from datetime import datetime


USER_COUNT = 100
MOVIE_COUNT = 100
DOCS_IN_COLL_COUNT = 1000


def get_random_like(user_id, movie_id) -> dict:
    like = {
        'user_id': user_id,
        'movie_id': movie_id,
        'like': random.randint(0, 10),
        'created': datetime.now(),
        'modified': datetime.now(),
    }
    return like


def get_random_review(user_id, movie_id) -> dict:
    user_id = user_id
    movie_id = movie_id
    review = {
        'user_id': user_id,
        'movie_id': movie_id,
        'review': f'review from {user_id} on {movie_id}',
        'created': datetime.now(),
        'modified': datetime.now(),
    }
    return review


def get_random_bookmark(user_id, movie_id) -> dict:
    bookmark = {
        'user_id': user_id,
        'movie_id': movie_id,
        'created': datetime.now(),
    }
    return bookmark


map_collections = {
    'likes': get_random_like,
    'reviews': get_random_review,
    'bookmarks': get_random_bookmark,
}
