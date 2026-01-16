from fastapi import APIRouter
import app.api.player_selector as player_selector

router = APIRouter(prefix="/players", tags=["players"])


# @router.get("/{player_id}")
# def get_player(player_id: int):
#     """Get player information by player ID."""
#     # Placeholder implementation
#     return {"player_id": player_id, "name": "Player Name", "team": "Team Name"}


@router.get("/select-player")
async def select_player():
    """Select a random player who hasn't been selected before."""
    # player = player_selector.select_random_player()
    player = player_selector.select_random_player(subteam="TEAM B")
    # player = player_selector.select_random_player(sex="F")
    # player = player_selector.select_random_player(subteam="TEAM A", sex="F")
    return player
