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
        dateOfBirth = coach_data['dateOfBirth'],
        nationality = default_if_none(coach_data['nationality'], ''),
        team = team
    )

    commit()
    return coach.id

@orm.db_session
def coach_in_database(
    coach_data: Dict[str, str]
    ) -> bool:

    coach = db.Coach.get(name=default_if_none(coach_data['name'], ''), 
                        dateOfBirth=coach_data['dateOfBirth'], 
                        nationality=default_if_none(coach_data['nationality'], ''))

    return coach is not None

@orm.db_session
def get_coach_id(
    coach_data: Dict[str, str]
    ) -> bool:

    coach = db.Coach.get(name=default_if_none(coach_data['name'], ''), 
                        dateOfBirth=coach_data['dateOfBirth'], 
                        nationality=default_if_none(coach_data['nationality'], ''))
    return coach.id

@orm.db_session
def register_coach_in_competition(
    coach_id: int,
    competition_code: str
    ) -> int:

    competition = db.Competition[competition_code]
    coach = db.Coach[coach_id]
    coach.competitions.add(competition)

    return coach.id