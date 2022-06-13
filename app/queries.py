SELECT_PLAYER_BY_NAME = """
    SELECT rowid, * FROM players WHERE name =:name
"""

SELECT_ALL_PLAYERS = """
    SELECT rowid, * FROM players
"""

CREATE_PLAYER = """
    INSERT INTO players (name, profession, hp, attack_power) 
    values (:name, :profession, :hp, :attack_power)
"""
