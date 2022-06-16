SELECT_PLAYER_BY_NAME = """
    SELECT rowid, * 
    FROM players 
    WHERE name = :name
"""

SELECT_PLAYER_BY_ID = """
    SELECT rowid, *
    FROM players
    WHERE rowid = :rowid
"""

SELECT_ALL_PLAYERS = """
    SELECT rowid, * 
    FROM players
"""

CREATE_PLAYER = """
    INSERT 
    INTO players (name, profession, hp, attack_power) 
    VALUES (:name, :profession, :hp, :attack_power)
"""

ADD_KILL = """
    UPDATE players
    SET kills = kills+1
    WHERE name = :name
"""

ADD_DEATH = """
    UPDATE players
    SET deaths = deaths+1
    WHERE name = :name
"""

SET_OFFLINE = """
    UPDATE players
    SET status = "offline"
    WHERE name = :name
"""

SET_ONLINE = """
    UPDATE players
    SET status = "online"
    WHERE name = :name
"""
