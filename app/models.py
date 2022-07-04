"""Module for SQLALCHEMY models"""
# pylint: disable=too-few-public-methods
# pylint: disable=missing-class-docstring

from sqlalchemy import Column, Integer, String
from database import Base


class Player(Base):
    __tablename__ = "players"

    rowid = Column(Integer, primary_key=True, nullable=False)
    name = Column(String, unique=True, nullable=False)
    profession = Column(String, nullable=False)
    hp = Column(Integer, nullable=False)
    attack_power = Column(Integer, nullable=False)
    status = Column(String, default="offline")
    kills = Column(Integer, default=0)
    deaths = Column(Integer, default=0)
