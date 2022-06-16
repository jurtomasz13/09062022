from database import connection


TABLE_COLUMNS = ['id', 'name', 'profession', 'hp',
                 'attack_power', 'status', 'kills', 'deaths']


def to_json(players) -> dict:
    if type(players) is tuple:
        return dict(zip(TABLE_COLUMNS, players))
    elif type(players) is list:
        players_dict = {'players': []}
        for player in players:
            players_dict['players'].append(dict(zip(TABLE_COLUMNS, player)))
    else:
        return {}
    return players_dict


def db_conn(func):
    def wrapper(*args):
        with connection() as cursor:
            return func(cursor, *args)
    return wrapper
