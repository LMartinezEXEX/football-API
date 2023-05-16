from pony import orm
from Database.database import *
from Database.service.utils import default_if_none
from typing import Dict

@orm.db_session
def save_player(
    player_data: Dict[str, str], 
    team_id: int
    ) -> int:
    
    team = db.Team[team_id]
    player = db.Player(
        name        = player_data['name'],
        position    = default_if_none(player_data['position'], ''),
        dateOfBirth = default_if_none(player_data['dateOfBirth'], ''),
        nationality = default_if_none(player_data['nationality'], ''),
        team = team
    )

    commit()
    return player.id