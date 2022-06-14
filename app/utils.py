TABLE_COLUMNS = ['id', 'name', 'profession', 'hp',
                 'attack_power', 'status', 'kills', 'deaths']


def to_json(players):
    players_dict = {}
    players_dict['players'] = []
    try:
        if type(players) == list:
            for player in players:
                players_dict['players'].append(
                    dict(zip(TABLE_COLUMNS, player)))
        else:
            players_dict['players'].append(dict(zip(TABLE_COLUMNS, players)))
    finally:
        return players_dict
