from sqlalchemy.orm import Session

import models
from database import get_db
from utils import to_json


@get_db
def create_player(db: Session, player_details: dict) -> int:
    player = models.Player(**player_details)
    db.add(player)
    db.commit()
    db.refresh(player)
    return to_json(player)


@get_db
def get_player_by_name(db: Session, name: str) -> dict:
    return to_json(db.query(models.Player).filter(models.Player.name == name).first())


@get_db
def get_player_by_id(db: Session, id: int) -> dict:
    return to_json(db.query(models.Player).filter(models.Player.rowid == id).first())


@get_db
def update_health(db: Session, name: str, hp: int) -> dict:
    player = db.query(models.Player).filter(models.Player.name == name).first()
    player.hp = hp
    db.commit()
    db.refresh(player)
    return to_json(player)


@get_db
def update_stats(db: Session, winner: str, loser: str) -> dict:
    winner = db.query(models.Player).filter(
        models.Player.name == winner).first()
    loser = db.query(models.Player).filter(models.Player.name == loser).first()

    winner.kills += 1
    loser.deaths += 1

    db.commit()
    db.refresh(winner)
    db.refresh(loser)

    result = {"killer": to_json(winner), "loser": to_json(loser)}

    return result


@get_db
def get_players(db: Session) -> dict:
    return to_json(db.query(models.Player).all())


@get_db
def set_status(db: Session, name: str, status: str) -> dict:
    status = str(status)
    player = db.query(models.Player).filter(models.Player.name == name).first()
    player.status = status
    db.commit()
    db.refresh(player)
    return to_json(player)
