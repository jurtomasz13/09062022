"""Module holding functions related to security"""

import requests
from authlib.integrations.starlette_client import OAuth
from starlette.config import Config

config = Config(".env")

oauth = OAuth(config)

OPENID_CONF_URL = "https://accounts.google.com/.well-known/openid-configuration"
PROVIDERS_KEYS: dict = requests.get("https://www.googleapis.com/oauth2/v3/certs").json()

oauth.register(
    name="google",
    acces_token_url="https://www.googleapis.com/oauth2/v4/token",
    server_metadata_url=OPENID_CONF_URL,
    client_kwargs={"scope": "openid email"},
)

google = oauth.google
