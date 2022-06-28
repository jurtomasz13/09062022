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
            entity_dict = entity.__dict__.copy()
            del entity_dict[list(entity_dict.keys())[0]]
            players_dict['players'].append(entity_dict)
        return players_dict
    if type(player) is models.Player:
        players_dict = player.__dict__.copy()
        del players_dict[list(players_dict.keys())[0]]
        return players_dict
