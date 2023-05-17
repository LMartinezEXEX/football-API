from pony import orm
from Database.database import *
from Database.service.utils import default_if_none
from typing import List, Dict

@orm.db_session
def save_team(
    team_data: Dict[str, any],
    competition_code: str
    ) -> int:

    competition = db.Competition[competition_code]

    if db.Team.get(name=team_data['name']) is not None:
        team = db.Team.get(name=team_data['name'])
        team.competitions.add(competition)
        return team.id

    team = db.Team(
        name         = team_data['name'],
        shortName    = default_if_none(team_data['shortName'], ''),
        tla          = team_data['tla'],
        areaName     = team_data['area']['name'],
        address      = team_data['address']
    )
    team.competitions.add(competition)

    commit()
    return team.id

@orm.db_session
def team_in_database(
    team_name: str
    ) -> bool:

    return db.Team.get(name=team_name) is not None

@orm.db_session
def coach_in_team(
    team_id: int,
    coach_data: Dict[str, str]
    ) -> bool:

    for coach in list(db.Coach.select(lambda c: team_id in c.team.id)):
        if  coach.name == coach_data['name']  and \
            coach.dateOfBirth == coach_data['dateOfBirth'] and \
            coach.nationality == coach_data['nationality']:
            return True

    return False

@orm.db_session
def get_team_id(
    team_name: str
    ) -> int:

    team = db.Team.get(name=team_name)
    return team.id if team is not None else -1

@orm.db_session
def register_competition_in_team(
    team_id: int, 
    competition_code: str
    ) -> int:

    team = db.Team[team_id]
    competition = db.Competition[competition_code]
    team.competitions.add(competition)
    return team.id

@orm.db_session
def add_player_to_team(
    team_id: int, 
    player_id: int
    ) -> int:

    team = db.Team[team_id]
    player = db.Player[player_id]
    team.players.add(player)
    return team.id
    
@orm.db_session
def register_coach_in_team(
    team_id: int, 
    coach_id: int
    ) -> int:

    team = db.Team[team_id]
    coach = db.Coach[coach_id]
    team.coaches.add(coach)
    return team.id

@orm.db_session
def get_team_by_name(
    team_name: str
    ) -> Dict[str, str]:

    team_data = db.Team.get(name = team_name)
    team = {
        "name": team_data.name,
        "tla": team_data.tla,
        "shortName": team_data.shortName,
        "areaName": team_data.areaName,
        "address": team_data.address
    }

    return team

@orm.db_session
def get_team_players(
    team_name: str
    ) -> List[Dict[str, str]]:

    team_data = db.Team.get(name = team_name)

    players = []
    for player in list(db.Player.select(lambda p: p.team.id == team_data.id)):
        player_data = {
            "name": player.name,
            "dateOfBirth": player.dateOfBirth,
            "position": player.position,
            "nationality": player.nationality
        }
        players.append(player_data)

    return players

@orm.db_session
def get_all_team_coaches(
    team_name: str
    ) -> List[Dict[str, str]]:

    team_id = get_team_id(team_name)
    coaches = []
    for coach in list(db.Coach.select(lambda c: team_id in c.team.id)):
        coach_data = {
            "name": coach.name,
            "dateOfBirth": coach.dateOfBirth,
            "nationality": coach.nationality
        }
        coaches.append(coach_data)

    return [dict(s) for s in set(frozenset(d.items()) for d in coaches)]