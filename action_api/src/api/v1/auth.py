import requests

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import HTTPBearer
from jose import JWTError, jwt

from core.config import api_settings
from models.auth_models import TokenData


http_scheme = HTTPBearer()
router = APIRouter()


async def authenticate(credentials: HTTPBearer = Depends(http_scheme)) -> TokenData:
    try:
        Jwt_token = credentials.credentials.encode('UTF-8')
        payload = jwt.decode(
            Jwt_token,
            api_settings.access_token_secret_key,
            algorithms=[api_settings.token_algoritm],
        )
        token_data = TokenData(**payload)
    except JWTError as e:
        credentials_exception = HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=str(e),
            headers={'Authorization': 'Bearer'},
        )
        raise credentials_exception
    return token_data
