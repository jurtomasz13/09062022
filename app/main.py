"""Main module for application"""
# pylint: disable=unused-argument
# pylint: disable=redefined-outer-name
# pylint: disable=missing-function-docstring

from json import JSONDecodeError

from sqlalchemy.exc import IntegrityError
from starlette import status
from starlette.applications import Starlette
from starlette.authentication import requires
from starlette.exceptions import HTTPException
from starlette.middleware.authentication import AuthenticationMiddleware
from starlette.requests import Request
from starlette.responses import JSONResponse
from starlette_jwt import JWTAuthenticationBackend

import config
import crud
import models
import security
import service
from database import engine
from exceptions import (
    PlayerAlreadyOffline,
    PlayerAlreadyOnline,
    StatusOffline,
    UnknownProfession,
)

models.Base.metadata.create_all(bind=engine)


def on_auth_error(request: Request, exc: Exception):
    return JSONResponse(
        {"error": str(exc), "status_code": status.HTTP_401_UNAUTHORIZED},
        status_code=status.HTTP_401_UNAUTHORIZED,
    )


app = Starlette(debug=True)

app.add_middleware(
    AuthenticationMiddleware,
    backend=JWTAuthenticationBackend(
        username_field="sub",
        prefix="Bearer",
        secret_key=config.JWT_SECRET_KEY,
        algorithm=config.JWT_ALGORITHM,
    ),
    on_error=on_auth_error,
)


@app.route("/api/player", ["GET"])
async def get_player(request: Request):
    try:
        player_name = request.query_params["name"]
        player = crud.get_player_by_name(player_name)
        if not player:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User with specified name does not exist",
            )
        return JSONResponse(content=player)

    except KeyError as exc:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Bad input provided"
        ) from exc


@app.route("/api/player", ["POST"])
async def post_player(request: Request):
    try:
        data = await request.json()
        name, profession = data["name"], data["profession"]
        player = service.create_player(name, profession)
        return JSONResponse(content=player, status_code=status.HTTP_201_CREATED)

    except IntegrityError as exc:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Player with that name already exists",
        ) from exc
    except UnknownProfession as exc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Unknown profession"
        ) from exc
    except KeyError as exc:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Bad input provided"
        ) from exc
    except JSONDecodeError as exc:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Bad input provided"
        ) from exc


@app.route("/api/players")
async def players(request: Request):
    players = crud.get_players()
    if not players["players"]:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="No players were found"
        )

    return JSONResponse(content=players)


@app.route("/api/player/attack", ["POST"])
@requires("authenticated")
async def attack(request: Request):
    try:
        enemy_name = (await request.json())["name"]
        if enemy_name == request.user.username:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="You cannot attack yourself",
            )

        player = crud.get_player_by_name(request.user.username)
        enemy = crud.get_player_by_name(enemy_name)

        if not player:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Player not found"
            )
        if not enemy:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Enemy not found"
            )

        result = service.attack(player, enemy)
        return JSONResponse(content=result)

    except KeyError as exc:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Bad input provided"
        ) from exc
    except JSONDecodeError as exc:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Bad input provided"
        ) from exc
    except StatusOffline as exc:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Either you or enemy are not logged in",
        ) from exc


@app.route("/api/player/duel", ["POST"])
@requires("authenticated")
async def duel(request: Request):
    try:
        enemy_name = (await request.json())["name"]
        if enemy_name == request.user.username:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="You cannot attack yourself",
            )

        player = crud.get_player_by_name(request.user.username)
        enemy = crud.get_player_by_name(enemy_name)

        if not player:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Player not found"
            )
        if not enemy:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Enemy not found"
            )

        result = service.fight(player, enemy)
        return JSONResponse(content=result)

    except KeyError as exc:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Bad input provided"
        ) from exc
    except JSONDecodeError:
        pass
    except StatusOffline as exc:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Either you or enemy are not logged in",
        ) from exc


@app.route("/api/player/{name}/login", ["POST"])
async def login(request: Request):
    name = request.path_params["name"]
    if not crud.get_player_by_name(name):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Player with specified name does not exist",
        )

    try:
        result = service.login(name)
    except PlayerAlreadyOnline as exc:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT, detail="Player is already online"
        ) from exc

    return JSONResponse(content=result)


@app.route("/api/player/{name}/logout", ["POST"])
async def logout(request: Request):
    name = request.path_params["name"]
    if not crud.get_player_by_name:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Player with specified name does not exist",
        )

    try:
        result = service.logout(name)
    except PlayerAlreadyOffline as exc:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT, detail="Player is already offline"
        ) from exc

    return JSONResponse(content=result)


@app.route("/token", ["POST"])
async def token(request: Request):
    try:
        body = await request.json()
    except JSONDecodeError as exc:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Bad input provided"
        ) from exc
    username = body.get("name")
    user = security.authenticate_user(username)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid username"
        )

    access_token = security.create_access_token(username)
    return JSONResponse({"access_token": access_token, "token_type": "Bearer"})
