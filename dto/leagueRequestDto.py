from pydantic import BaseModel

class LeagueRequestDto(BaseModel):
    code: str