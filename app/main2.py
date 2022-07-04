"""Main module for application"""
# pylint: disable=unused-argument
# pylint: disable=redefined-outer-name
# pylint: disable=missing-function-docstring
# pylint: disable=no-value-for-parameter

from json import JSONDecodeError

from sqlalchemy.exc import IntegrityError
from starlette import status
from starlette.applications import Starlette
from starlette.authentication import requires
from starlette.exceptions import HTTPException
from starlette.middleware.authentication import AuthenticationMiddleware
from starlette.middleware.sessions import SessionMiddleware
from starlette.requests import Request
from starlette.responses import JSONResponse, RedirectResponse

import config
import crud
import models
import service
from database import engine
from exceptions import (
    PlayerAlreadyOffline,
    PlayerAlreadyOnline,
    StatusOffline,
    UnknownProfession,
)
from middleware import JWTAuthenticationBackend
from security2 import PROVIDERS_KEYS, google

models.Base.metadata.create_all(bind=engine)

app = Starlette(debug=True)

app.add_middleware(
    SessionMiddleware, secret_key=config.SESSION_SECRET_KEY, https_only=True
)


def on_auth_error(exc: Exception):
    """Returns error if authentication fails"""
    return JSONResponse(
        {"error": str(exc), "status_code": status.HTTP_401_UNAUTHORIZED},
        status_code=status.HTTP_401_UNAUTHORIZED,
    )


app.add_middleware(
    AuthenticationMiddleware,
    backend=JWTAuthenticationBackend(providers_keys=PROVIDERS_KEYS),
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
        data = await request.json()
        player_name = data["player_name"]
        enemy_name = data["enemy_name"]
        if enemy_name == player_name:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="You cannot attack yourself",
            )

        player = crud.get_player_by_name(player_name)
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
        data = await request.json()
        player_name = data["player_name"]
        enemy_name = data["enemy_name"]
        if enemy_name == player_name:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="You cannot attack yourself",
            )

        player = crud.get_player_by_name(name=player_name)
        enemy = crud.get_player_by_name(name=enemy_name)

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


@app.route("/login")
async def log(request):
    redirect_uri = request.url_for("auth")
    return await google.authorize_redirect(request, redirect_uri)


@app.route("/auth")
async def auth(request: Request):
    token = await google.authorize_access_token(request)
    request.session["token"] = token
    return RedirectResponse(request.url_for("info"))


@app.route("/info")
async def info(request: Request):
    data = request.session["token"]
    if data:
        return JSONResponse(
            {"access_token": data["id_token"], "token_type": data["token_type"]}
        )
    RedirectResponse(request.url_for("login"))
