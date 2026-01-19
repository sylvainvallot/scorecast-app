from random import randint
from pydantic import BaseModel
from typing import Optional, Any
from app.config import settings

USER_CONFIG = settings.USER_CONFIG


class Color(BaseModel):
    primary: str
    secondary: str

    def __getitem__(self, key: str) -> str:
        return getattr(self, key)

    @property
    def color_rgb(self):
        return {
            "primary": tuple(
                int(self.primary.lstrip('#')[i:i+2], 16)
                for i in (0, 2, 4)
            ),
            "secondary": tuple(
                int(self.secondary.lstrip('#')[i:i+2], 16)
                for i in (0, 2, 4)
            ),
        }


class Team(BaseModel):
    id: str
    name: str
    city: str
    color: Color
    subteams: list[str] = []

    def __getitem__(self, key: str) -> Any:
        return getattr(self, key)


class TeamScoreBoard(BaseModel):
    id: str
    color: Color
    score: int = 0
    subteam: str | None = None


class ScorecastPayload(BaseModel):
    home_team: str
    away_team: str
    home_score: int
    away_score: int
    home_subteam: Optional[str] = ""
    away_subteam: Optional[str] = ""
    team_type: Optional[str] = "mixed"
    player: Optional[str] = ""
    model_config = {
        "json_schema_extra": {
            "example": {
                "home_team": (
                    USER_CONFIG["config"]["my_team_id"]
                ),
                "away_team": (
                    USER_CONFIG["config"]["my_team_id"]
                ),
                "home_score": randint(0, 50),
                "away_score": randint(0, 50),
                "home_subteam": "",
                "away_subteam": "",
                "player": ""
            }
        }
    }


class Player(BaseModel):
    name: str
    surname: str
    player_number: int


class TeamPartial(BaseModel):
    id: str
    color: Color


class PlayerCard(BaseModel):
    player: Player
    team: TeamPartial


class PlayerCardPayload(BaseModel):
    player_name: str
    player_surname: str
    player_number: int

    model_config = {
        "json_schema_extra": {
            "example": {
                "player_name": "Tom",
                "player_surname": "Brady",
                "player_number": 12
            }
        }
    }
