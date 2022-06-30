import requests


class Client:
    def __init__(self, player_name=None, enemy_name=None, profession=None) -> None:
        self.url = "http://localhost:8000"
        self.player_name: str | None = player_name
        self.enemy_name: str | None = enemy_name
        self.profession: str | None = profession
        self.token: str | None = None
        self.response: requests.Response | None = None

    @property
    def header(self) -> dict:
        return {"Authorization": f"Bearer {self.token}"}

    @property
    def return_checked_response(self) -> dict:
        result: dict = {}
        try:
            if self.response.ok:
                result = self.response.json()
            else:
                result = {self.response.status_code: self.response.text}
        except AttributeError:
            pass
        return result

    def get_player(self) -> dict:
        if self.player_name is None:
            return {"message": "You need to provide a player name"}

        self.response = requests.get(
            self.url + f"/api/player?name={self.player_name}")

        return self.return_checked_response

    def get_players(self) -> dict:
        self.response = requests.get(self.url + "/api/players")

        return self.return_checked_response

    def create_player(self) -> dict:
        if self.player_name is None and self.profession is None:
            return {"message": "You need to provide a player name and a profession"}
        if self.player_name is None:
            return {"message": "You need to provide a player name"}
        if self.profession is None:
            return {"message": "You need to provide a profession"}

        body = {"name": self.player_name, "profession": self.profession}

        self.response = requests.post(self.url + "/api/player", json=body)

        return self.return_checked_response

    def get_token(self) -> dict:
        if self.player_name is None:
            return {"message": "You need to provide a player name"}

        self.response = requests.post(
            self.url + "/token", json={"name": self.player_name}
        )
        if self.response.ok:
            self.token = self.response.json()["access_token"]

        return self.return_checked_response

    def login(self) -> dict:
        if self.player_name is None:
            return {"message": "You need to provide a player name"}

        self.response = requests.post(
            self.url + f"/api/player/{self.player_name}/login"
        )

        return self.return_checked_response

    def logout(self) -> dict:
        if self.player_name is None:
            return {"message": "You need to provide a player name"}

        self.response = requests.post(
            self.url + f"/api/player/{self.player_name}/logout"
        )

        return self.return_checked_response

    def attack(self) -> dict:
        if self.player_name is None and self.enemy_name is None:
            return {"message": "You need to provide a player and an enemy names"}
        if self.player_name is None:
            return {"message": "You need to provide a player name"}
        if self.enemy_name is None:
            return {"message": "You need to provide an enemy name"}

        self.get_token()
        self.response = requests.post(
            self.url + "/api/player/attack",
            json={"name": self.enemy_name},
            headers=self.header,
        )

        return self.return_checked_response

    def duel(self) -> dict:
        if self.player_name is None and self.enemy_name is None:
            return {"message": "You need to provide a player and an enemy names"}
        if self.player_name is None:
            return {"message": "You need to provide a player name"}
        if self.enemy_name is None:
            return {"message": "You need to provide an enemy name"}

        self.get_token()
        self.response = requests.post(
            self.url + "/api/player/attack",
            json={"name": self.enemy_name},
            headers=self.header,
        )

        return self.return_checked_response
