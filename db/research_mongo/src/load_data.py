import logging
import logging.config
from cfg import LOGGING

from collection_data import map_collections, USER_COUNT

import pymongo
from pymongo import MongoClient
from pymongo.errors import PyMongoError


logging.config.dictConfig(LOGGING)
logger = logging.getLogger('load_data')
client = MongoClient('mongodb://0.0.0.0:27019, 0.0.0.0:27020')
db = client['actionsDb']


if __name__ == '__main__':
    logger.info('start')    
    coll_names = db.list_collection_names()
    logger.info(f'collections: {coll_names}')
    for coll_name in coll_names:
        collection = db[coll_name]
        values = []
        counter: int = 0
        count_docs = 1000 * USER_COUNT
        for i in range(0, count_docs):
            data = map_collections[coll_name]()        
            values.append(data)
            if len(values) >= 1000:
                try:
                    collection.insert_many(values)
                except PyMongoError as e:
                    logger.error(f'({e.code}) {e.message}')
                finally:
                    values = []
                    counter += 1000
                    logger.info(f'insert {counter} docs in collection {coll_name}')
    logger.info('load OK')





