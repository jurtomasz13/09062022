from random import sample

from exceptions import UnknownProfession, StatusOffline, PlayerAlreadyOnline, PlayerAlreadyOffline
import crud
import utils


def attack(player: dict, enemy: dict):
    STATUS = utils.Status.OFFLINE.name.lower()

    if player['status'] == STATUS or enemy['status'] == STATUS:
        raise StatusOffline()

    dmg = utils.rand_dmg(player)

    if enemy['hp'] > 0:
        enemy['hp'] -= dmg

    if enemy['hp'] <= 0:
        crud.set_status(enemy['name'], STATUS)
        crud.update_health(
            enemy['name'], utils.PROFESSIONS[enemy['profession'].lower()]['hp'])
        return crud.update_stats(player['name'], enemy['name'])

    crud.update_health(enemy['name'], enemy['hp'])
    return {'message': f"Attacked {enemy['name']} for {dmg} dmg"}


def fight(player: dict, enemy: dict):
    STATUS = utils.Status.OFFLINE.name.lower()

    if player['status'] == STATUS or enemy['status'] == STATUS:
        raise StatusOffline()

    first, second = sample([player, enemy], 2)

    while first['hp'] > 0 and second['hp'] > 0:
        second['hp'] -= utils.rand_dmg(first)
        if first['hp'] > 0 and second['hp'] > 0:
            first['hp'] -= utils.rand_dmg(second)

    if first['hp'] > 0:
        result = crud.update_stats(first['name'], second['name'])
    result = crud.update_stats(second['name'], first['name'])

    return result


def create_player(name: str, profession: str):
    profession = profession.lower()

    if profession not in utils.PROFESSIONS:
        raise UnknownProfession()

    player_details = {
        'name': name,
        'profession': profession.capitalize()
    }

    player_details.update(utils.PROFESSIONS[profession])

    return crud.create_player(player_details)


def login(name: str):
    STATUS = utils.Status.ONLINE.name.lower()

    player = crud.get_player_by_name(name)
    if player['status'] == STATUS:
        raise PlayerAlreadyOnline()
    result = crud.set_status(name, STATUS)
    print(result)
    return result


def logout(name: str):
    STATUS = utils.Status.OFFLINE.name.lower()

    player = crud.get_player_by_name(name)
    if player['status'] == STATUS:
        raise PlayerAlreadyOffline()

    return crud.set_status(name, STATUS)
