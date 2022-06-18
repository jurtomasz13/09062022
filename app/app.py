from starlette.applications import Starlette
from starlette.requests import Request
from starlette.responses import JSONResponse, PlainTextResponse
from starlette.routing import Route
from starlette.exceptions import HTTPException
from starlette import status
from sqlite3 import IntegrityError

from exceptions import UnknownProfession, StatusOffline
import service
import crud


async def home(request: Request):
    return PlainTextResponse(content='Hello, world!')


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

    # Could be else but it is more transparent
    elif request.method == 'POST':
        data = await request.json()
        try:
            print(data)
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


async def attack(request: Request):
    try:
        # Could use method .get() here however I want to provide a feedback about wrong input
        player_name = request.path_params['name']
        enemy_name = (await request.json())['name']
        player = crud.get_player_by_name(player_name)
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
    try:
        # Could use method .get() here however I want to provide a feedback about wrong input
        name = request.path_params['name']
        if not crud.get_player_by_name:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail="Player with specified name does not exist")

    except KeyError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Bad input provided")

    result = crud.login(name)
    return JSONResponse(content=result)


async def logout(request: Request):
    try:
        # Could use method .get() here however I want to provide a feedback about wrong input
        name = request.path_params['name']
        if not crud.get_player_by_name:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail="Player with specified name does not exist")

    except KeyError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Bad input provided")

    result = crud.logout(name)
    return JSONResponse(content=result)


routes = [
    Route('/', home),
    Route('/api/players', players),
    Route('/api/player', player, methods=['GET', 'POST']),
    Route('/api/player/{name}/login', login),
    Route('/api/player/{name}/logout', logout),
    Route('/api/player/{name}/attack', attack, methods=['POST'])
]

app = Starlette(routes=routes)
