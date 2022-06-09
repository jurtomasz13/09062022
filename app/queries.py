SELECT_PLAYER_BY_NAME = """
    SELECT * FROM players WHERE name = '{}' 
"""

SELECT_ALL_PLAYERS = """
    SELECT * FROM players
"""

CREATE_PLAYER = """
    INSERT INTO players (name, profession, hp, attack_power) 
    values ('{}', '{}', {}, {})
"""
