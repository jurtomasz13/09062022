from starlette.config import Config

config = Config(".env")

JWT_SECRET_KEY = config.get(
    "JWT_SECRET_KEY",
    default="eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJuYW1lIjoiVXNlcl8xIn0.qq-jNXgsfNRmzJN9ppE46LlRP9QYghafAy4spOXysDA",
)
JWT_ALGORITHM = config.get("JWT_ALGORITHM", default="HS256")
JWT_TOKEN_EXPIRE_TIME_IN_MINUTES = config.get(
    "JWT_TOKEN_EXPIRE_TIME_IN_MINUTES", cast=int, default=35
)
GOOGLE_CLIENT_ID = config.get("GOOGLE_CLIENT_ID")
GOOGLE_CLIENT_SECRET = config.get("GOOGLE_CLIENT_SECRET")
SESSION_SECRET_KEY = config.get("SESSION_SECRET_KEY")
