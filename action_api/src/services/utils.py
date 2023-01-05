import uuid
from core.config import api_settings as setting


class UtilsService:
    def __init__(self):
        self.db = None
        self.collection = None

    async def read_to_paginate(self, size: int, page: int, find: dict) -> dict:
        skip = (page - 1) * size
        cnt = await self.collection.count_documents(find)
        total = int(cnt / size) + 1
        cursor = self.collection.find(find).skip(skip).limit(size)
        pages = {
            'prev': (page - 1) if page > 1 else None,
            'next': (page + 1) if page < total else None,
            'total': total,
            'items': await cursor.to_list(setting.max_page_size),
        }
        return pages

    async def delete_doc(self, user_id: uuid.UUID, movie_id: uuid.UUID) -> bool:
        """
        delete the doc.
        
        return False - ok, True - fault
        """
        doc = await self.collection.find_one({'user_id': user_id, 'movie_id': movie_id})
        if doc is None:
            return True
        delete_result = await self.collection.delete_one({'_id': doc['_id']})
        if delete_result.deleted_count > 0:
            return False
        return True

    async def add_like_to_review(
        self, user_id: uuid.UUID, movie_id: uuid.UUID, raiting: int
    ) -> None:
        """Adds a like (rating) to a review."""
        review = await self.db[setting.mongodb_coll_reviews].find_one(
            {'user_id': user_id, 'movie_id': movie_id}
        )
        if review is None:
            return
        await self.db[setting.mongodb_coll_reviews].update_one(
            {'_id': review['_id']}, {'$set': {'like': raiting}}
        )
        return

    async def read_like_reiting(
        self, user_id: uuid.UUID, movie_id: uuid.UUID
    ) -> int | None:
        """Read like(rating) in likes collection."""
        like = await self.db[setting.mongodb_coll_likes].find_one(
            {'user_id': user_id, 'movie_id': movie_id}
        )
        if like is None:
            return None
        return like['like']
