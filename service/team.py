from Database.service.team import team_in_database, get_team_by_name, get_team_players, get_team_coach
from model.TeamDataRequestEnum import TeamDataRequest
from typing import Dict

def loaded_team(
    team_name: str
    ) -> bool:

    return team_in_database(team_name)

def retrieve_team_data(
    team_name: str
    ) -> Dict[str, str]:

    return get_team_by_name(team_name)

def retrieve_team_members(
    team_name: str, 
    which: TeamDataRequest
    ) -> Dict[str, any]:

    data = {}
    if which is TeamDataRequest.ALL:
        data['players'] = get_team_players(team_name)
        data['coach'] = get_team_coach(team_name)

    elif which is TeamDataRequest.ONLY_PLAYERS:
        data['players'] = get_team_players(team_name)
        
    elif which is TeamDataRequest.ONLY_COACH:
        data['coach'] = get_team_coach(team_name)

    return data