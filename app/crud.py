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


def update_match(winner_player, loser_player):
    with connection() as cursor:
        new_kills = winner_player['kills'] + 1
        new_deaths = loser_player['deaths'] + 1
        cursor.execute(
            ADD_KILL, {'new_kills': new_kills, 'name': winner_player['name']})
        cursor.execute(
            ADD_DEATH, {'new_deaths': new_deaths, 'name': loser_player['name']})


def get_players():
    with connection() as cursor:
        result = cursor.execute(SELECT_ALL_PLAYERS)
        players = result.fetchall()
        return to_json(players)
