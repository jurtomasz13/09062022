from json import JSONDecodeError
from starlette.applications import Starlette
from starlette.responses import JSONResponse, PlainTextResponse, RedirectResponse
from starlette.routing import Route, Mount
from starlette.templating import Jinja2Templates
from starlette.staticfiles import StaticFiles
from random import randint
import crud


templates = Jinja2Templates(directory='static/templates')


async def homepage(request):
    return PlainTextResponse(content='Hello, world!')


async def get_player(request):
    name = request.query_params['name']
    player = crud.get_player_by_name(name)
    if len(player['players']) == 0:
        return JSONResponse(content={'status': 404})
    return JSONResponse(content=player)


async def get_players(request):
    players = crud.get_players()
    return JSONResponse(content=players)


async def attack_player(request):
    LOWER_MULTIPLIER = 0.6
    HIGHER_MULTIPLIER = 1.4
    try:
        data = await request.json()
        player = crud.get_player_by_name(
            request.path_params['name'])['players'][0]
        enemy_player = crud.get_player_by_name(data['name'])['players'][0]
        while player['hp'] > 0 and enemy_player['hp'] > 0:
            player['hp'] -= randint(enemy_player['attack_power']
                                    * LOWER_MULTIPLIER, enemy_player['attack_power']*HIGHER_MULTIPLIER)
            if player['hp'] > 0 and enemy_player['hp'] > 0:
                enemy_player['hp'] -= randint(player['attack_power']
                                              * LOWER_MULTIPLIER, player['attack_power']*HIGHER_MULTIPLIER)
        if player['hp'] > 0:
            crud.update_stats(player, enemy_player)
            message = {'Winner': player['name']}
        else:
            crud.update_stats(enemy_player, player)
            message = {'Winner': enemy_player['name']}
    except JSONDecodeError:
        message = {
            'message': 'You didn\'t specify a player in a path or enemy in a body'}
    except IndexError:
        message = {
            'message': 'Your player or enemy with specified nickname does not exist'}
    return JSONResponse(content=message)


async def html_get_player(request):
    name = request.path_params['name']
    players = crud.get_player_by_name(name)
    return templates.TemplateResponse('players.html', {'request': request, 'players': players})


async def html_get_players(request):
    players = crud.get_players()
    return templates.TemplateResponse('players.html', {'request': request, 'players': players})


async def create_player(request):
    player_data = await request.form()
    print(player_data)
    crud.create_player(name=player_data['name'], profession=player_data['profession'],
                       hp=player_data['hp'], attack_power=player_data['attack_power'])
    return RedirectResponse(url='/players')


async def html_create_player(request):
    return templates.TemplateResponse('form.html', {'request': request})

routes = [
    Route('/', homepage),
    Route('/api/players', get_players),
    Route('/api/player', get_player),
    Route('/api/player', create_player, methods=['POST']),
    Route('/api/player/{name}/attack', attack_player, methods=['GET', 'POST']),
    Route('/players', html_get_players),
    Route('/player/{name}', html_get_player),
    Route('/player', html_create_player),
    Mount('/static', StaticFiles(directory='static'), name='static')
]

app = Starlette(debug=True, routes=routes)
