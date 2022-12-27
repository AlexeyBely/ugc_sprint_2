import logging
import logging.config
from cfg import LOGGING

from datetime import datetime

import pymongo
from pymongo import MongoClient
from pymongo.errors import PyMongoError

logging.config.dictConfig(LOGGING)
logger = logging.getLogger('research_mongo')
client = MongoClient('mongodb://0.0.0.0:27019, 0.0.0.0:27020')
db = client['actionsDb']


collect_find = [
    ('likes', 'user_id'),
]

if __name__ == '__main__':
    logger.info('start research')
    coll_names = db.list_collection_names()
    logger.info(f'collections: {coll_names}')
    for coll_name in coll_names:
        collection = db[coll_name]
        cnt = collection.count_documents({})
        logger.info(f'in collection {coll_name} {cnt} docs')       
    logger.info('research OK')




