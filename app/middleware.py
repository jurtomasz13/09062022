from typing import Tuple, Union

from starlette.authentication import (
    AuthCredentials,
    AuthenticationBackend,
    SimpleUser,
    AuthenticationError,
    BaseUser,
)
from authlib.jose import jwt


class JWTAuthenticationBackend(AuthenticationBackend):
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
        except ValueError:
            raise AuthenticationError(
                "Could not separate Authorization scheme and token"
            )
        if scheme.lower() != prefix.lower():
            raise AuthenticationError(f"Authorization scheme {scheme} is not supported")
        return token

    async def authenticate(
        self, request
    ) -> Union[None, Tuple[AuthCredentials, BaseUser]]:
        if "Authorization" not in request.headers:
            return None

        auth = request.headers["Authorization"]
        token = self.get_token_from_header(authorization=auth, prefix=self.prefix)
        try:
            payload = jwt.decode(token, key=self.providers_keys)
        except Exception as e:
            raise AuthenticationError(str(e))
        return AuthCredentials(["authenticated"]), SimpleUser(username=payload["email"])
