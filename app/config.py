from starlette.config import Config

config = Config('.env')

JWT_SECRET_KEY = config.get('JWT_SECRET_KEY', default='')
JWT_ALGORITHM = config.get('JWT_ALGORITHM', default='')
JWT_TOKEN_EXPIRE_TIME_IN_MINUTES = config.get(
    'JWT_TOKEN_EXPIRE_TIME_IN_MINUTES', cast=int, default=0)
TEST = config.get('TEST', default=True, cast=bool)
