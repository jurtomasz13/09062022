from random import randint, sample

from exceptions import UnknownProfession, StatusOffline
import crud


def fight(player: dict, enemy: dict):
    if player['status'] == 'offline' or enemy['status'] == 'offline':
        raise StatusOffline()

    LOWER_MULTIPLIER = 0.6
    HIGHER_MULTIPLIER = 1.4

    def rand_dmg(player: dict) -> int:
        return randint(player['attack_power']
                       * LOWER_MULTIPLIER, player['attack_power']*HIGHER_MULTIPLIER)

    first, second = sample([player, enemy], 2)

    while first['hp'] > 0 and second['hp'] > 0:
        second['hp'] -= rand_dmg(first)
        if first['hp'] > 0 and second['hp'] > 0:
            first['hp'] -= rand_dmg(second)

    if first['hp'] > 0:
        result = crud.update_stats(first['name'], second['name'])
    result = crud.update_stats(second['name'], first['name'])

    return result


def create_player(name: str, profession: str):
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

    profession = profession.lower()

    if profession not in PROFESSIONS:
        raise UnknownProfession()

    player_details = {
        'name': name,
        'profession': profession.capitalize()
    }

    player_details.update(PROFESSIONS[profession])
    result = crud.create_player(player_details)

    return crud.get_player_by_id(result)
