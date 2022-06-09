from database import connection
from queries import *

TABLE_COLUMNS = ['name', 'profession', 'hp',
                 'attack_power', 'status', 'kills', 'deaths']


def to_json(players):
    players_dict = {}
    players_dict['players'] = []
    if type(players) == list:
        for player in players:
            players_dict['players'].append(dict(zip(TABLE_COLUMNS, player)))
    else:
        players_dict['players'].append(dict(zip(TABLE_COLUMNS, players)))
    return players_dict


def create_player(name, profession, hp, attack_power):
    with connection() as cursor:
        try:
            cursor.execute(CREATE_PLAYER.format(
                name, profession, hp, attack_power))
        finally:
            print('Player created!')


def get_player_by_name(name):
    with connection() as cursor:
        result = cursor.execute(SELECT_PLAYER_BY_NAME.format(name))
        player = result.fetchone()
        return to_json(player)


def get_players():
    with connection() as cursor:
        result = cursor.execute(SELECT_ALL_PLAYERS)
        players = result.fetchall()
        return to_json(players)
