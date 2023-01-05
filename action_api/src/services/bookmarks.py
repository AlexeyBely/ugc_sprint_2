import uuid

from datetime import datetime
from motor.motor_asyncio import AsyncIOMotorClient
from bson import ObjectId

from services_abc.bookmarks_abc import BaseBookmarksService
from core.config import api_settings as setting
from services.utils import UtilsService


class MongoBookmarksService(BaseBookmarksService, UtilsService):
    """read/write docs to bookmarks collection."""

    def __init__(self, client: AsyncIOMotorClient):
        self.client = client
        self.db = self.client[setting.mongodb_db]
        self.collection = self.db[setting.mongodb_coll_bookmarks]

    async def read_bookmarks(
        self, user_id: uuid.UUID | None = None, size: int = 1, page: int = 20
    ) -> dict:
        """Load bookmarks from user_id."""
        find = {'user_id': user_id}
        pages = await self.read_to_paginate(size, page, find)
        return pages

    async def add_bookmark(self, user_id: uuid.UUID, movie_id: uuid.UUID) -> dict:
        """Add new review."""
        bookmark = await self.collection.find_one({'user_id': user_id, 
                                                   'movie_id': movie_id})
        if bookmark is not None:
            return bookmark
        new_bookmark = {
            'user_id': user_id,
            'movie_id': movie_id,
            'created': datetime.now(),
        }
        bm_insert = await self.collection.insert_one(new_bookmark)
        bookmark = await self.collection.find_one({'_id': bm_insert.inserted_id})
        return bookmark

    async def delete_bookmark(self, user_id: uuid.UUID, movie_id: uuid.UUID) -> bool:
        """delete the bookmark."""
        return await self.delete_doc(user_id, movie_id)
