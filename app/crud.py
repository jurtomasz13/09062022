"""Module responsible for handling CRUD operations"""

from sqlalchemy.orm import Session

import models
from database import get_session
from utils import to_json


@get_session
def create_player(player_details: dict, session: Session | None = None) -> int:
    """Creates new player and returns it"""
    player = models.Player(**player_details)
    session.add(player)
    session.commit()
    session.refresh(player)
    return to_json(player)


@get_session
def get_player_by_name(name: str, session: Session | None = None) -> dict:
    """Returns player by its name"""
    return to_json(
        session.query(models.Player).filter(models.Player.name == name).first()
    )


@get_session
def get_player_by_id(row_id: int, session: Session | None = None) -> dict:
    """Returns player by its id"""
    return to_json(
        session.query(models.Player).filter(models.Player.rowid == row_id).first()
    )


@get_session
def update_health(name: str, health: int, session: Session | None = None) -> dict:
    """Updates player's health"""
    player_id = (
        session.query(models.Player)
        .filter(models.Player.name == name)
        .update({models.Player.hp: health})
    )
    session.commit()
    player = (
        session.query(models.Player).filter(models.Player.rowid == player_id).first()
    )
    return player


@get_session
def update_stats(winner: str, loser: str, session: Session | None = None) -> dict:
    """Updates players' fight result and returns theirs stats as a dict"""
    winner_id = (
        session.query(models.Player)
        .filter(models.Player.name == winner)
        .update({models.Player.kills: +1})
    )
    loser_id = (
        session.query(models.Player)
        .filter(models.Player.name == loser)
        .update({models.Player.deaths: +1})
    )
    session.commit()
    winner = (
        session.query(models.Player).filter(models.Player.rowid == winner_id).first()
    )
    loser = session.query(models.Player).filter(models.Player.rowid == loser_id).first()
    result = {"killer": to_json(winner), "loser": to_json(loser)}
    return result


@get_session
def get_players(session: Session | None = None) -> dict:
    """Returns a list of players"""
    players = to_json(session.query(models.Player).all())
    print(f"HEHE: {players}")
    return players


@get_session
def set_status(name: str, status: str, session: Session | None = None) -> dict:
    """Sets status of the player"""
    status = str(status)
    player = session.query(models.Player).filter(models.Player.name == name).first()
    player.status = status
    session.commit()
    session.refresh(player)
    return to_json(player)
