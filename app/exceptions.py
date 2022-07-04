"""Module for exceptions"""


class PlayerAlreadyOffline(Exception):
    """Exception raised when player is already offline"""


class PlayerAlreadyOnline(Exception):
    """Exception raised when player is already online"""


class StatusOffline(Exception):
    """Exception raised when player status is offline"""


class UnknownProfession(Exception):
    """Exception raised when specified profession does not exist"""
