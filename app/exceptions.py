class PlayerAlreadyOffline(Exception):
    def __init__(self, message=None):
        self.message = message


class PlayerAlreadyOnline(Exception):
    def __init__(self, message=None):
        self.message = message


class StatusOffline(Exception):
    def __init__(self, message=None):
        self.message = message


class UnknownProfession(Exception):
    def __init__(self, message=None):
        self.message = message
