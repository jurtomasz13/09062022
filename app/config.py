from starlette.config import Config

config = Config('.env')

JWT_SECRET_KEY = config.get('JWT_SECRET_KEY')
JWT_ALGORITHM = config.get('JWT_ALGORITHM')
JWT_TOKEN_EXPIRE_TIME_IN_MINUTES = config.get(
    'JWT_TOKEN_EXPIRE_TIME_IN_MINUTES', cast=int)
