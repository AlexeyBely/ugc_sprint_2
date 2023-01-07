import uuid

from datetime import datetime
from db.db_mongo import MotorClient
from bson import ObjectId

from services_abc.likes_abc import BaseLikesService
from core.config import api_settings as setting
from services.utils import UtilsService


class MongoLikesService(BaseLikesService, UtilsService):
    """read/write docs to likes collection."""

    def __init__(self, client: MotorClient):
        self.client = client.client_mongodb
        self.db = self.client[setting.mongodb_db]
        self.collection = self.db[setting.mongodb_coll_likes]

    async def id_details(self, like_id: str) -> dict | None:
        """Show a like by its UUID."""
        id = ObjectId(like_id)
        like = await self.collection.find_one({'_id': id})
        return like

    async def read_likes(
        self,
        user_id: uuid.UUID,
        movie_id: uuid.UUID | None = None,
        size: int = setting.default_page_size,
        page: int = 1,
    ) -> dict:
        """Load likes from user_id or movie_id."""
        if movie_id is not None:
            find = {'movie_id': movie_id}
        else:
            find = {'user_id': user_id}
        return await self.read_to_paginate(size, page, find)

    async def add_like(self, user_id: uuid.UUID, movie_id: uuid.UUID, 
                       rating: int) -> dict:
        """Add or modified like."""
        like = await self.collection.find_one({'user_id': user_id, 'movie_id': movie_id})
        if like is None:
            new_like = {
                'user_id': user_id,
                'movie_id': movie_id,
                'like': rating,
                'created': datetime.now(),
                'modified': datetime.now(),
            }
            like_obj = await self.collection.insert_one(new_like)
            like_id = like_obj.inserted_id
        else:
            update = {
                'like': rating,
                'modified': datetime.now(),
            }
            like_obj = await self.collection.update_one({'_id': like['_id']}, 
                                                        {'$set': update})
            like_id = like['_id']
        new_like = await self.collection.find_one({'_id': like_id})
        await self.add_like_to_review(user_id, movie_id, rating)
        return new_like

    async def delete_like(self, user_id: uuid.UUID, movie_id: uuid.UUID) -> bool:
        """
        delete the like.
        
        return False - ok, True - fault
        """
        return await self.delete_doc(user_id, movie_id)

    async def info_likes(self, movie_id: uuid.UUID) -> dict:
        """info likes."""
        cnt = await self.collection.count_documents({'movie_id': movie_id})
        avg = 0
        cursor = self.collection.find({'movie_id': movie_id})
        async for doc in cursor:
            avg += doc['like']
        avg = round(avg / cnt, 1)
        return {'count_likes': cnt, 'raiting': avg}
