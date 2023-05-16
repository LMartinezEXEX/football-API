from Database.service.competition import competition_in_database, get_players
from typing import List, Dict

def loaded_competition(
    code: str
    ) -> bool:

    return competition_in_database(code)


def retrieve_competition_players(
    code: str
    ) -> List[Dict[str, str]]:

    return get_players(code)