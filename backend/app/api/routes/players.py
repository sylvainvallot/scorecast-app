from typing import Optional
from fastapi import APIRouter
import app.api.player_selector as player_selector

router = APIRouter(prefix="/players", tags=["players"])


# @router.get("/{player_id}")
# def get_player(player_id: int):
#     """Get player information by player ID."""
#     # Placeholder implementation
#     return {"player_id": player_id, "name": "Player Name", "team": "Team Name"}


@router.get("/select-player")
async def select_player(
    subteam: Optional[str] = None, sex: Optional[str] = None
):
    """Select a random player who hasn't been selected before."""
    player = player_selector.select_random_player(
        subteam=subteam, sex=sex
    )
    return player
