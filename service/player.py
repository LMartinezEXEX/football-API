from typing import List, Dict

def filter_players_by_team(
    players: List[Dict[str, str]],
    team_name: str
    ) -> List[Dict[str, str]]:

    return list(filter(lambda p: p['team'] == team_name, players))