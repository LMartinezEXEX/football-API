from pony import orm
from Database.database import *
from typing import List, Dict

@orm.db_session
def save_competition(
    competition_data: Dict[str, any]
    ) -> str:

    competition = db.Competition(
        name=competition_data['name'],
        code=competition_data['code'],
        areaName=competition_data['area']['name']
    )

    return competition.code

@orm.db_session
def competition_in_database(
    competition_code: str
    ) -> bool:
    
    return db.Competition.get(code=competition_code) is not None

@orm.db_session
def save_team_in_competition(
    competition_code: str, 
    team_id: int
    ) -> str:

    competition = db.Competition[competition_code]
    team = db.Team[team_id]
    competition.teams.add(team)

    return competition.code

@orm.db_session
def get_players(
    competition_code: str
    ) -> List[Dict[str, str]]:

    players = []
    for player in list(select(p for p in db.Player if db.Competition[competition_code] in p.team.competitions)):
        player_data = {
            "name": player.name,
            "dateOfBirth": player.dateOfBirth,
            "position": player.position,
            "nationality": player.nationality,
            "team": player.team.name
        }
        players.append(player_data)

    return players