"""Module with helper methods"""
# pylint: disable=redefined-outer-name

from enum import Enum
from random import randint

import models


class Status(Enum):
    """ENUM for user's status"""

    ONLINE = "online"
    OFFLINE = "offline"


PROFESSIONS = {
    "warrior": {"hp": 100, "attack_power": 20},
    "archer": {"hp": 80, "attack_power": 25},
    "mage": {"hp": 70, "attack_power": 30},
}


LOWER_MULTIPLIER = 0.6
HIGHER_MULTIPLIER = 1.4


players_model_vars = [
    attr
    for attr in dir(models.Player)
    if not callable(getattr(models.Player, attr)) and not attr.startswith("_")
]


def rand_dmg(player: dict) -> int:
    """Returns a random number from chosen range"""
    return randint(
        player["attack_power"] * LOWER_MULTIPLIER,
        player["attack_power"] * HIGHER_MULTIPLIER,
    )


def to_json(players: list | models.Player) -> dict:
    """Converts players model to dict"""
    if isinstance(players, models.Player):
        player = players
        players_dict = {
            key: value
            for key, value in player.__dict__.items()
            if key in players_model_vars
        }
    if isinstance(players, list):
        players_dict = {"players": []}
        for player in players:
            player_as_dict = {
                key: value
                for key, value in player.__dict__.items()
                if key in players_model_vars
            }
            players_dict["players"].append(player_as_dict)
    return players_dict
