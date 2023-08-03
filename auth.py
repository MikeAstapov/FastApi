import secrets

from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBasic
from fastapi.security import HTTPBasicCredentials

from models import get_user_from_db

security = HTTPBasic()


def auth_user(credentials: HTTPBasicCredentials = Depends(security)):
    user = get_user_from_db(credentials.username)
    if user is None or user.password != credentials.password:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
    return user
