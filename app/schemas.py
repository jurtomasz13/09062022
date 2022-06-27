from pydantic import BaseModel


class PlayerCreate(BaseModel):
    name: str
    profession: str
    hp: int
    attack_power: int


class Player(BaseModel):
    rowid: int
    name: str
    profession: str
    hp: int
    attack_power: int
    status: str
    kills: int
    deaths: int

    class Config:
        orm_mode = True
