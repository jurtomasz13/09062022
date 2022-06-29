from starlette.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from contextlib import contextmanager
import pytest
import json

from database import TestConnection
from models import Base
from main import app

client = TestClient(app)

engine = create_engine('sqlite:///app/test.db',
                       connect_args={"check_same_thread": False})

TestingSessionLocal = sessionmaker(
    autocommit=False, autoflush=False, bind=engine)

JWT_TOKEN = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJVc2VyXzEifQ.Gp3B7nVorqYIeIeFsamt2vZfRvfGM5i4Fuyc5oUC0SM'


@contextmanager
def connection():
    db: Session = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


@pytest.fixture
def test_arrange():
    setattr(TestConnection, 'connection', connection)
    Base.metadata.create_all(bind=engine)


def test_create_player(test_arrange):
    data = {
        'name': 'User_1',
        'profession': 'Warrior'
    }

    expected = {
        'rowid': 1,
        'name': 'User_1',
        'profession': 'Warrior',
        'hp': 100,
        'attack_power': 20,
        'status': 'offline',
        'kills': 0,
        'deaths': 0
    }

    response = client.post('api/player', data=json.dumps(data))
    client.post(
        'api/player', data=json.dumps({'name': 'User_2', 'profession': 'Archer'}))

    assert response.status_code == 201
    assert response.json() == expected


def test_get_player():
    name = 'User_1'

    expected = {
        'rowid': 1,
        'name': 'User_1',
        'profession': 'Warrior',
        'hp': 100,
        'attack_power': 20,
        'status': 'offline',
        'kills': 0,
        'deaths': 0
    }

    response = client.get(f'api/player?name={name}')

    assert response.status_code == 200
    assert response.json() == expected


def test_get_players():
    expected = {
        'players': [
            {'rowid': 1,
             'name': 'User_1',
             'profession': 'Warrior',
             'hp': 100,
             'attack_power': 20,
             'status': 'offline',
             'kills': 0,
             'deaths': 0},
            {'rowid': 2,
             'name': 'User_2',
             'profession': 'Archer',
             'hp': 80,
             'attack_power': 25,
             'status': 'offline',
             'kills': 0,
             'deaths': 0},
        ]
    }

    response = client.get('api/players')

    assert response.status_code == 200
    assert response.json() == expected


def test_post_login():
    name = 'User_1'

    expected = {
        'rowid': 1,
        'name': 'User_1',
        'profession': 'Warrior',
        'hp': 100,
        'attack_power': 20,
        'status': 'online',
        'kills': 0,
        'deaths': 0
    }

    response = client.post(f'api/player/{name}/login')
    client.post(f'api/player/User_2/login')

    assert response.status_code == 200
    assert response.json() == expected


def test_post_logout():
    name = 'User_1'

    expected = {
        'rowid': 1,
        'name': 'User_1',
        'profession': 'Warrior',
        'hp': 100,
        'attack_power': 20,
        'status': 'offline',
        'kills': 0,
        'deaths': 0
    }

    response = client.post(f'api/player/{name}/logout')
    client.post(f'api/player/User_1/login')

    assert response.status_code == 200
    assert response.json() == expected


def test_post_token():
    name = 'User_1'

    response = client.post('token',
                           data=json.dumps({'name': name}))

    assert response.status_code == 200
    assert response.json().get('token_type', False) == 'Bearer'


def test_post_attack():
    headers = {'Authorization': 'Bearer {}'.format(JWT_TOKEN)}

    response = client.post('api/player/attack',
                           data=json.dumps({'name': 'User_2'}), headers=headers)

    assert response.status_code == 200
    assert response.json().get('message') or (response.json().get(
        'killer') and response.json().get('loser'))


def test_post_duel(test_cleanup):
    headers = {'Authorization': 'Bearer {}'.format(JWT_TOKEN)}

    response = client.post('api/player/duel',
                           data=json.dumps({'name': 'User_2'}), headers=headers)

    assert response.status_code == 200
    assert response.json().get('killer', False) and response.json().get('loser', False)


@ pytest.fixture
def test_cleanup():
    yield
    Base.metadata.drop_all(bind=engine)