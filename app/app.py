from starlette.applications import Starlette
from starlette.responses import JSONResponse, PlainTextResponse
from starlette.routing import Route, Mount
from starlette.templating import Jinja2Templates
from starlette.staticfiles import StaticFiles
import crud


templates = Jinja2Templates(directory='static/templates')


async def homepage(request):
    return PlainTextResponse(content='Hello, world!')


async def get_player(request):
    name = request.path_params['name']
    player = crud.get_player_by_name(name)
    return JSONResponse(content=player)


async def get_players(request):
    players = crud.get_players()
    return JSONResponse(content=players)


async def html_get_player(request):
    name = request.path_params['name']
    players = crud.get_player_by_name(name)
    return templates.TemplateResponse('players.html', {'request': request, 'players': players})


async def html_get_players(request):
    players = crud.get_players()
    return templates.TemplateResponse('players.html', {'request': request, 'players': players})


# async def create_player(request):
#     pass

routes = [
    Route('/', homepage),
    Route('/api/players', get_players),
    Route('/api/player/{name}', get_player),
    Route('/players', html_get_players),
    Route('/player/{name}', html_get_player),
    Mount('/static', StaticFiles(directory='static'), name='static')
]

app = Starlette(debug=True, routes=routes)
