import uuid
import random

from datetime import datetime


user_ids = [str(uuid.uuid4()) for x in range(1000)]
movie_ids = [str(uuid.uuid4()) for x in range(1000)]


def get_random_like() -> dict:
    like = {
        'user_id': random.choice(user_ids),
        'movie_id': random.choice(movie_ids),
        'like': random.randint(0, 10),
        'created': datetime.now(),
        'modified': datetime.now(),    
    }
    return like


def get_random_review() -> dict:
    user_id = random.choice(user_ids)
    movie_id = random.choice(movie_ids)
    review = {
        'user_id': user_id,
        'movie_id': movie_id,
        'review': f'review from {user_id} on {movie_id}',
        'created': datetime.now(),
        'modified': datetime.now(),    
    }
    return review


def get_random_bookmark() -> dict:
    bookmark = {
        'user_id': random.choice(user_ids),
        'movie_id': random.choice(movie_ids),
        'created': datetime.now(),   
    }
    return bookmark


map_collections = {
    'likes': get_random_like,
    'reviews': get_random_review,
    'bookmarks': get_random_bookmark,
}
