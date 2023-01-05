import logging
import logging.config
from cfg import LOGGING

from datetime import datetime
from collection_data import map_collections

import pymongo
from pymongo import MongoClient
from pymongo.errors import PyMongoError

logging.config.dictConfig(LOGGING)
logger = logging.getLogger('research_mongo')
client = MongoClient(
    'mongodb://0.0.0.0:27019, 0.0.0.0:27020', uuidRepresentation='pythonLegacy'
)
db = client['actionsDb']


collect_find = [
    ('likes', 'user_id'),
]

if __name__ == '__main__':
    logger.info('---------------- start research ---------------------')
    coll_names = db.list_collection_names()
    logger.info(f'collections: {coll_names}')
    for coll_name in coll_names:
        collection = db[coll_name]
        cnt = collection.count_documents({})
        logger.info(f'in collection {coll_name} {cnt} docs')

    likes = []
    collection = db['likes']
    for i in range(0, 3):
        likes.append(collection.find()[i])

    # research liked movies by user
    for i in range(0, 3):
        user_id = likes[i]['user_id']
        find_coll = collection.find({'user_id': user_id})
        like_movies = [like['movie_id'] for like in find_coll]
        logger.info(f'{len(like_movies)} movies liked by the user_id {user_id}')

    # research liked movies by user
    for i in range(0, 3):
        user_id = likes[i]['user_id']
        find_coll = collection.find({'user_id': user_id})
        like_movies = []
        for like in find_coll:
            like_movies.append(like['movie_id'])
            if len(like_movies) > 100:
                break
        logger.info(f'{len(like_movies)} movies liked by the user_id {user_id}')

    # research liked users by movie
    for i in range(0, 3):
        movie_id = likes[i]['movie_id']
        find_coll = collection.find({'movie_id': movie_id})
        like_users = [like['user_id'] for like in find_coll]
        logger.info(f'{len(like_users)} users liked by the movie_id {movie_id}')

    # research bookmarks
    collection = db['bookmarks']
    for i in range(0, 3):
        user_id = likes[i]['user_id']
        find_coll = collection.find({'user_id': user_id})
        bookmarks_movie = [like['movie_id'] for like in find_coll]
        logger.info(f'{len(bookmarks_movie)} movies bookmarks per user_id {user_id}')

    # research save and read doc
    like = map_collections['likes']()
    collection = db['likes']
    like_id = collection.insert_one(like).inserted_id
    logger.info(f'insert like with _id {like_id}')
    find_coll = collection.find_one(
        {'user_id': like['user_id'], 'movie_id': like['movie_id'],}
    )
    like_ids = find_coll['_id']
    logger.info(f'read likes with _ids {like_ids}')
    find_coll = collection.find({'_id': like['_id']})
    like_ids = [like_fn['_id'] for like_fn in find_coll]
    logger.info(f'read likes with _ids {like_ids}')
    cnt = collection.count_documents({})
    logger.info(f'in collection {coll_name} {cnt} docs')

    logger.info('---------------- research OK -------------------')
