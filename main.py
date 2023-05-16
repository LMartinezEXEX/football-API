from typing_extensions import Annotated
from typing import Union
from fastapi import FastAPI, HTTPException, Query, Path
from slowapi.errors import RateLimitExceeded
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from starlette.requests import Request
from service.api_load import *
from service.competition import *
from service.player import *
from service.team import *
from model.TeamDataRequestEnum import TeamDataRequest
from dto.leagueRequestDto import LeagueRequestDto

limiter = Limiter(key_func=get_remote_address)
app = FastAPI()
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

@app.get("/")
def get_root():
    return {"v": "1.0"}


@app.post("/league")
@limiter.limit("10/minute")
def save_league(
    request: Request,
    request_dto: LeagueRequestDto
    ):

    err = load_league(request_dto.code)
    if err:
        raise HTTPException(status_code=400, detail=err)
    
    return {"code": request_dto.code}


@app.get("/{league_code}/players")
def get_players_from_league(
    league_code: Annotated[str, Path(title="Competition code", max_length=10)], 
    in_team: Annotated[Union[str, None], Query(max_length=50)] = None
    ):

    if not loaded_competition(league_code):
        raise HTTPException(status_code=400, detail="No data of this competition was loaded previously")

    players = retrieve_competition_players(league_code)
    if in_team is not None and len(players) != 0:
        players = filter_players_by_team(players, in_team)

    return {"players": players}


@app.get("/team/{name}")
def get_team(
    name: Annotated[str, Path(title="Team name", max_length=50)],
    detail: Union[TeamDataRequest, None] = None
    ):

    if not loaded_team(name):
        raise HTTPException(status_code=400, detail="Team is not present in the database")
    
    payload = {"team": retrieve_team_data(name)}
    
    if detail is not None:
        data = retrieve_team_members(name, detail)
        payload["team"]["requested"] = data
    
    return payload


@app.get("/team/{name}/players")
def get_players_from_team(
    name: Annotated[str, Path(title="Team name", max_length=50)]
    ):

    if not loaded_team(name):
        raise HTTPException(status_code=400, detail="Team is not present in the database")
    
    return retrieve_team_members(name, TeamDataRequest.ALL)