from pydantic import BaseSettings, root_validator


class Settings(BaseSettings):
    mongodb_local_url = 'mongodb://0.0.0.0:27019, 0.0.0.0:27020'
    mongodb_db: str = 'actionsDb'
    mongodb_coll_likes: str = 'likes'
    mongodb_coll_reviews: str = 'reviews'
    mongodb_coll_bookmarks: str = 'bookmarks'
    access_token_secret_key: str = '256-bit-secret-key-1'
    token_algoritm: str = 'HS256'
    default_page_size: int = 20
    max_page_size: int = 100
    service_url: str | None = None
    action_host: str = '127.0.0.1'
    action_port: int = 8998

    @root_validator
    def compute_service_url(cls, values):
        if values.get('service_url', None) is None:
            port = values['action_port']
            host = values['action_host']
            values['service_url'] = f"http://{host}:{port}/action/api/v1"
        return values 


settings = Settings()
