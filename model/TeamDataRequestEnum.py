from enum import Enum

class TeamDataRequest(str, Enum):
    ALL = 'ALL'
    ONLY_PLAYERS = 'PLAYERS'
    ONLY_COACHES = 'COACHES'