from starlette.applications import Starlette
from starlette.authentication import requires
from starlette.middleware import Middleware
from starlette.middleware.authentication import AuthenticationMiddleware
from starlette.requests import Request
from starlette.responses import JSONResponse
from starlette.routing import Route
from starlette.exceptions import HTTPException
from starlette import status
from starlette_jwt import JWTAuthenticationBackend
from sqlalchemy.exc import IntegrityError

from exceptions import UnknownProfession, StatusOffline, PlayerAlreadyOnline, PlayerAlreadyOffline
from database import engine
import config
import crud
import models
import service
import security


models.Base.metadata.create_all(bind=engine)


async def on_auth_error(request: Request, exc: Exception):
    return JSONResponse({'error': exc.message, 'status': exc.status_code}, status_code=exc.status_code)


async def player(request: Request):
    if request.method == 'GET':
        try:
            name = request.query_params['name']
            player = crud.get_player_by_name(name)
            if not player:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                    detail="User with specified name does not exist")
            return JSONResponse(content=player)

        except KeyError:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, detail="Bad input provided")

    elif request.method == 'POST':
        data = await request.json()
        try:
            name, profession = data['name'], data['profession']
            new_player = service.create_player(name, profession)
            return JSONResponse(content=new_player, status_code=status.HTTP_201_CREATED)

        except IntegrityError:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT, detail="User with that name already exists")
        except UnknownProfession:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Unknown profession")
        except KeyError:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, detail="Bad input provided")


async def players(request: Request):
    players = crud.get_players()
    if not players['players']:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="No players were found")

    return JSONResponse(content=players)


@requires('authenticated')
async def attack(request: Request):
    try:
        enemy_name = (await request.json())['name']
        if enemy_name == request.user.username:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT, detail="You cannot attack yourself")

        player = crud.get_player_by_name(request.user.username)
        enemy = crud.get_player_by_name(enemy_name)

        if not player:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Player not found")
        if not enemy:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Enemy not found")

        result = service.attack(player, enemy)
        return JSONResponse(content=result)

    except KeyError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Bad input provided")
    except StatusOffline:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail="Either you or enemy are not logged in")


@requires('authenticated')
async def duel(request: Request):
    try:
        enemy_name = (await request.json())['name']
        if enemy_name == request.user.username:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT, detail="You cannot attack yourself")

        player = crud.get_player_by_name(request.user.username)
        enemy = crud.get_player_by_name(enemy_name)

        if not player:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Player not found")
        if not enemy:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Enemy not found")

        result = service.fight(player, enemy)
        return JSONResponse(content=result)

    except KeyError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Bad input provided")
    except StatusOffline:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail="Either you or enemy are not logged in")


async def login(request: Request):
    name = request.path_params['name']
    if not crud.get_player_by_name:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="Player with specified name does not exist")

    try:
        result = service.login(name)
    except PlayerAlreadyOnline:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT,
                            detail="Player is already online")

    return JSONResponse(content=result)


async def logout(request: Request):
    name = request.path_params['name']
    if not crud.get_player_by_name:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="Player with specified name does not exist")

    try:
        result = service.logout(name)
    except PlayerAlreadyOffline:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT,
                            detail="Player is already offline")

    return JSONResponse(content=result)


async def token(request: Request):
    body = await request.json()
    username = body.get('name')
    user = security.authenticate_user(username)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid username")

    access_token = security.create_access_token(username)
    return JSONResponse({'access_token': access_token, 'token_type': 'Bearer'})


routes = [
    Route('/api/players', players),
    Route('/api/player', player, methods=['GET', 'POST']),
    Route('/api/player/{name}/login', login, methods=['POST']),
    Route('/api/player/{name}/logout', logout, methods=['POST']),
    Route('/api/player/attack', attack, methods=['POST']),
    Route('/api/player/duel', duel, methods=['POST']),
    Route('/token', token, methods=['POST'])
]

middleware = [
    Middleware(AuthenticationMiddleware,
               backend=JWTAuthenticationBackend(username_field='sub', prefix='Bearer', secret_key=config.JWT_SECRET_KEY, algorithm=config.JWT_ALGORITHM), on_error=on_auth_error)
]

app = Starlette(routes=routes, middleware=middleware)
