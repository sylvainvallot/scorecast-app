import os
from fastapi import APIRouter, HTTPException
from fastapi.responses import FileResponse
from app.models import Team, Color
from app.config import settings, paths

router = APIRouter(prefix="/teams", tags=["teams"])

DB = settings.USER_DB
USER_CONFIG = settings.USER_CONFIG


def get_team_data(team_id: str) -> Team | None:
    team = DB["teams"].get(team_id)
    if not team:
        return None
    return Team(
        id=team_id,
        name=team["name"],
        city=team["city"],
        color=Color(
            primary=team["color"]["primary"],
            secondary=team["color"]["secondary"],
        ),
        subteams=team.get("subteams", []),
    )


@router.get("/list", response_model=list[Team])
def get_teams():
    """Retrieve the list of all teams."""
    teams = []
    for team_id in DB["teams"]:
        team_data = get_team_data(team_id)
        if team_data:
            teams.append(team_data)
    teams_sorted = sorted(teams, key=lambda x: x.name)
    return teams_sorted


@router.get("/my-team", response_model=Team)
def my_team() -> Team:
    """Retrieve information about the user's team."""
    my_team_id = USER_CONFIG["config"]["my_team_id"]
    team = get_team_data(my_team_id)
    if not team:
        raise HTTPException(status_code=404, detail="User team not found")
    return team


@router.get("/id/{team_id}", response_model=Team)
def get_team(team_id: str):
    """Retrieve information about a specific team by its ID."""
    team_data = get_team_data(team_id)
    if not team_data:
        raise HTTPException(status_code=404, detail="Team not found")
    return team_data


@router.get("/id/{team_id}/logo", response_class=FileResponse)
async def get_logo(team_id: str):
    """Retrieve the logo for a specific team by its ID."""

    logo_path = paths.TEAMS_LOGO_PATH / f"{team_id}.png"

    if not os.path.exists(logo_path):
        raise HTTPException(status_code=404, detail="Logo not found")
    return FileResponse(logo_path, media_type="image/png")
