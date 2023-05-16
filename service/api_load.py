import requests
from service.competition import loaded_competition
from Database.database import *
from Database.service.competition import save_competition, save_team_in_competition
from Database.service.team import save_team, add_player_to_team, register_coach_in_team, register_competition_in_team, team_in_database, get_team_id
from Database.service.player import save_player
from Database.service.coach import save_coach
from typing import List, Dict, Optional

BASE_API = 'https://api.football-data.org/v4'
HEADERS = { 'X-Auth-Token': 'a373dc0b3c2c4fb7b4710ee79a5df629' }

def load_league(
    code: str
    ) -> Optional[str]:

    if loaded_competition(code):
        return "Competition already in database"

    uri = BASE_API + '/competitions/{}'.format(code)
    
    response =  requests.get(uri, headers=HEADERS)
    if (response.status_code != 200):
        return "Error during competition data request"

    competition_code = save_competition(response.json())
    return load_teams_from_league(competition_code)


def load_teams_from_league(
    code: str
    ) -> Optional[str]:
    
    uri = BASE_API + '/competitions/{}/teams'.format(code)

    response =  requests.get(uri, headers=HEADERS)
    if (response.status_code != 200):
        return "Error during competition teams data request"

    save_teams(response.json()['teams'], code)


def save_teams(
    teams: List[Dict[str, str]], 
    competition_code: str
    ) -> None:

    for team in teams:
        if team_in_database(team['name']):
            team_id = get_team_id(team['name'])
            register_competition_in_team(team_id, competition_code)
            continue

        team_id = save_team(team, competition_code)

        coach_id = save_coach(team['coach'], team_id)
        register_coach_in_team(team_id, coach_id)

        for player in team['squad']:
            player_id = save_player(player, team_id)
            add_player_to_team(team_id, player_id)

        save_team_in_competition(competition_code, team_id)