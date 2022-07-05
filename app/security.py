"""Module holding functions related to security"""

from datetime import datetime, timedelta

from jose import jwt

import config
from crud import get_player_by_name


def authenticate_user(username: str):
    """Authenticates the user and returns it"""
    user = get_player_by_name(username)
    if not user:
        return False
    return user


def create_access_token(username):
    """Creates a new access token for the given username"""
    to_encode = {
        "sub": username,
        "iat": datetime.utcnow(),
        "exp": datetime.utcnow()
        + timedelta(minutes=config.JWT_TOKEN_EXPIRE_TIME_IN_MINUTES),
    }
    encoded_jwt = jwt.encode(
        to_encode, key=config.JWT_SECRET_KEY, algorithm=config.JWT_ALGORITHM
    )
    return encoded_jwt
