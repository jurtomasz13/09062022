import schemas
import models

from random import randint
from enum import Enum


class Status(Enum):
    ONLINE = 'online'
    OFFLINE = 'offline'


PROFESSIONS = {
    'warrior': {
        'hp': 100,
        'attack_power': 20
    },
    'archer': {
        'hp': 80,
        'attack_power': 25
    },
    'mage': {
        'hp': 70,
        'attack_power': 30
    }
}


LOWER_MULTIPLIER = 0.6
HIGHER_MULTIPLIER = 1.4


def rand_dmg(player: dict) -> int:
    return randint(player['attack_power']
                   * LOWER_MULTIPLIER, player['attack_power'] * HIGHER_MULTIPLIER)


def to_json(player) -> dict:
    if type(player) is list:
        players_dict = {'players': []}
        for entity in player:
            entity = {**schemas.Player(rowid=entity.rowid, name=entity.name, profession=entity.profession, hp=entity.hp,
                                       attack_power=entity.attack_power, status=entity.status, kills=entity.kills, deaths=entity.deaths).dict()}
            players_dict['players'].append(entity)
        return players_dict
    if type(player) is models.Player:
        return {**schemas.Player(rowid=player.rowid, name=player.name, profession=player.profession, hp=player.hp,
                                 attack_power=player.attack_power, status=player.status, kills=player.kills, deaths=player.deaths).dict()}
