import requests


class Client():
    url = 'http://localhost:8000'

    def __init__(self, player_name=None, enemy_name=None, profession=None) -> None:
        self.player_name: str = player_name
        self.enemy_name: str = enemy_name
        self.profession: str = profession
        self.token: str = None

    def get_player(self) -> dict:
        if self.player_name is None:
            return {'message': 'You need to provide a player name'}

        response = requests.get(
            self.url+f'/api/player?name={self.player_name}')

        if response.ok:
            result = response.json()
        return result

    def get_players(self) -> dict:
        response = requests.get(self.url+'/api/players')

        if response.ok:
            result = response.json()
        return result

    def create_player(self) -> dict:
        if self.player_name is None and self.profession is None:
            return {'message': 'You need to provide a player name and a profession'}
        elif self.player_name is None:
            return {'message': 'You need to provide a player name'}
        elif self.profession is None:
            return {'message': 'You need to provide a profession'}

        data = {
            'name': self.player_name,
            'profession': self.profession
        }

        response = requests.post(self.url+'/api/player', json=data)

        if response.ok:
            result = response.json()
        elif response.status_code == 409:
            result = {'message': 'Player with this name already exists'}

        return result

    def get_token(self,) -> dict:
        if self.player_name is None:
            return {'message': 'You need to provide a player name'}

        response = requests.post(
            self.url+'/token', json={'name': self.player_name})

        if response.ok:
            self.token = response.json()['access_token']
            result = response.json()

        return result

    def login(self) -> dict:
        if self.player_name is None:
            return {'message': 'You need to provide a player name'}

        response = requests.post(
            self.url+f'/api/player/{self.player_name}/login')

        if response.ok:
            result = response.json()
        return result

    def logout(self) -> dict:
        if self.player_name is None:
            return {'message': 'You need to provide a player name'}

        response = requests.post(
            self.url+f'/api/player/{self.player_name}/logout')

        if response.ok:
            result = response.json()
        return result

    def attack(self) -> dict:
        if self.player_name is None and self.enemy_name is None:
            return {'message': 'You need to provide a player and an enemy names'}
        elif self.player_name is None:
            return {'message': 'You need to provide a player name'}
        elif self.enemy_name is None:
            return {'message': 'You need to provide an enemy name'}

        self.get_token()
        response = requests.post(self.url+'/api/player/attack',
                                 json={'name': self.enemy_name}, headers=self.header)

        if response.ok:
            result = response.json()
        return result

    def duel(self) -> dict:
        self.token = self.get_token()
        response = requests.post(self.url+'/api/player/attack',
                                 json={'name': self.enemy_name}, headers=self.header)

        if response.ok:
            result = response.json()
        return result

    @property
    def header(self) -> dict:
        return {'Authorization': f'Bearer {self.token}'}
