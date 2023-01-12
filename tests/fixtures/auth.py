import pytest
import uuid
import jwt
from datetime import datetime, timedelta

from ..settings import settings


# fixture auth
@pytest.fixture(scope='session')
def auth_bearer(user_movie_ids) -> tuple:
    """
    authorization via jvt-token

    return tuple(
        heaher HTTPBearer,
        user_id
    ) 
    """
    user_ids, movie_ids = user_movie_ids
    user_id = user_ids[0]
    lat = datetime.utcnow()
    exp = lat + timedelta(hours=24)
    jti = str(uuid.uuid4())
    payload = {
        'user': str(user_id),
        'roles': ['user', ],
        'lat': int(datetime.timestamp(lat)),
        'exp': int(datetime.timestamp(exp)),
        'jti': jti
    }
    token = jwt.encode(
        payload, 
        settings.access_token_secret_key, 
        settings.token_algoritm
    )
    header_bearer = {'Authorization': f'Bearer {token}'}
    return header_bearer, str(user_id)