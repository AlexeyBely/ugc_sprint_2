def get_items_by_user_id(collection_docs: list, user_id: str) -> list:
    result = []
    for doc in collection_docs:
        if str(doc['user_id']) == user_id:
            result.append(doc)
    return result


def get_items_by_movie_id(collection_docs: list, movie_id: str) -> list:
    result = []
    for doc in collection_docs:
        if str(doc['movie_id']) == movie_id:
            result.append(doc)
    return result