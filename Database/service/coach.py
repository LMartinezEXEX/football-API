from pony import orm
from Database.database import *
from Database.service.utils import default_if_none
from typing import Dict

@orm.db_session
def save_coach(
    coach_data: Dict[str, str], 
    team_id: int
    ) -> int:

    team = db.Team[team_id]
    coach = db.Coach(
        name        = default_if_none(coach_data['name'], ''),
        dateOfBirth = default_if_none(coach_data['dateOfBirth'], ''),
        nationality = default_if_none(coach_data['nationality'], ''),
        team = team
    )

    commit()
    return coach.id