from database import connection
from queries import *
from utils import *


def create_player(name, profession, hp, attack_power):
    with connection() as cursor:
        try:
            params = {
                'name': name,
                'profession': profession,
                'hp': hp,
                'attack_power': attack_power
            }
            cursor.execute(CREATE_PLAYER, params)
        finally:
            print('Player created!')


def get_player_by_name(name):
    with connection() as cursor:
        params = {
            'name': name
        }
        result = cursor.execute(SELECT_PLAYER_BY_NAME, params)
        player = result.fetchone()
        return to_json(player)


def get_players():
    with connection() as cursor:
        result = cursor.execute(SELECT_ALL_PLAYERS)
        players = result.fetchall()
        return to_json(players)
