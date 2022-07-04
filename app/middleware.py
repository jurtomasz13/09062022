"""Module that holds middleware class for authentication"""

from typing import Tuple, Union

from authlib.jose import jwt
from starlette.authentication import (
    AuthCredentials,
    AuthenticationBackend,
    AuthenticationError,
    BaseUser,
    SimpleUser,
)


class JWTAuthenticationBackend(AuthenticationBackend):
    """Class that authenticates user using JWT from OAuth"""

    def __init__(
        self,
        prefix: str = "Bearer",
        username_field: str = "email",
        providers_keys: dict = None,
    ):
        self.prefix = prefix
        self.username_field = username_field
        self.providers_keys = providers_keys

    @classmethod
    def get_token_from_header(cls, authorization: str, prefix: str) -> str:
        """Parses the Authorization header and returns only the token"""
        try:
            scheme, token = authorization.split()
        except ValueError as exc:
            raise AuthenticationError(
                "Could not separate Authorization scheme and token"
            ) from exc
        if scheme.lower() != prefix.lower():
            raise AuthenticationError(f"Authorization scheme {scheme} is not supported")
        return token

    async def authenticate(self, conn) -> Union[None, Tuple[AuthCredentials, BaseUser]]:
        if "Authorization" not in conn.headers:
            return None

        auth = conn.headers["Authorization"]
        token = self.get_token_from_header(authorization=auth, prefix=self.prefix)
        try:
            payload = jwt.decode(token, key=self.providers_keys)
        except Exception as exc:
            raise AuthenticationError(str(exc)) from exc
        return AuthCredentials(["authenticated"]), SimpleUser(username=payload["email"])
