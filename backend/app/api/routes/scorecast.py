from io import BytesIO
from fastapi import APIRouter, Response
from fastapi.responses import FileResponse
from app.models import (
    ScorecastPayload,
    PlayerCard,
    PlayerCardPayload,
    Player,
    TeamPartial,
    TeamScoreBoard,
)
from app.api.routes.teams import get_team_data, my_team
import app.scorecast.main as sc
from app.scorecast.players import generate_playercard
from app.config import paths

router = APIRouter(prefix="/scorecast", tags=["scorecast"])


def game_result(home_score: int, away_score: int) -> str:
    result = "win" if home_score > away_score else "loss"
    if home_score == away_score:
        result = "draw"
    return result


@router.post("/generate", response_class=Response)
async def generate_scorecast(payload: ScorecastPayload):
    """Generate a game scorecast reel using the provided payload."""

    # Generate the scoreboard
    home_team_data = get_team_data(payload.home_team)
    away_team_data = get_team_data(payload.away_team)

    if not home_team_data or not away_team_data:
        raise ValueError("Invalid team data")

    scoreboard = sc.generate_scoreboard(
        TeamScoreBoard(
            id=payload.home_team,
            score=payload.home_score,
            color=home_team_data.color,
            subteam=payload.home_subteam if payload.home_subteam else None
        ),
        TeamScoreBoard(
            id=payload.away_team,
            score=payload.away_score,
            color=away_team_data.color,
            subteam=payload.away_subteam if payload.away_subteam else None
        )
    )

    result = game_result(payload.home_score, payload.away_score)

    filename = f"scorecast_{result}_{payload.home_team}_vs_{payload.away_team}"

    sc.generate_video(
        filename, scoreboard, result, "test"
    )

    return FileResponse(
        paths.OUTPUT_VIDEOS_PATH / f"{filename}.mp4",
        media_type="video/mp4",
        filename=f"{filename}.mp4",
        headers={
            "Content-Disposition": f"attachment; filename={filename}.mp4"
        },
    )


@router.post("/playercard")
async def generate_playercard_endpoint(
    payload: PlayerCardPayload
):
    """Generate a player card image.

    Args:
        payload (PlayerCardPayload): Payload containing player details.

    Returns:
        file: PNG image of the player card.
    """
    team = my_team()

    team_partial = TeamPartial(
        id=team.id,
        color=team.color
    )

    player = Player(
        name=payload.player_name,
        surname=payload.player_surname,
        player_number=payload.player_number
    )

    playercard = PlayerCard(
        player=player,
        team=team_partial
    )

    card_img = generate_playercard(playercard)
    card_bytes = BytesIO()
    card_img.save(card_bytes, format="PNG")
    card_bytes.seek(0)

    filename = f"playercard_{player.surname.lower()}.png"

    return Response(
        content=card_bytes.getvalue(),
        media_type="image/png",
        headers={
            "Content-Disposition": f"inline; filename={filename}"
        },
    )


@router.post("/scoreboard")
async def test_scoreboard(payload: ScorecastPayload):
    """Generate a scoreboard image for testing purposes."""

    home_team_data = get_team_data(payload.home_team)
    away_team_data = get_team_data(payload.away_team)

    if not home_team_data or not away_team_data:
        raise ValueError("Invalid team data")

    scoreboard = sc.generate_scoreboard(
        TeamScoreBoard(
            id=payload.home_team,
            score=payload.home_score,
            color=home_team_data.color,
            subteam=payload.home_subteam if payload.home_subteam else None
        ),
        TeamScoreBoard(
            id=payload.away_team,
            score=payload.away_score,
            color=away_team_data.color,
            subteam=payload.away_subteam if payload.away_subteam else None
        )
    )

    scoreboard_bytes = BytesIO()
    scoreboard.save(scoreboard_bytes, format="PNG")
    scoreboard_bytes.seek(0)

    return Response(
        content=scoreboard_bytes.getvalue(),
        media_type="image/png",
        headers={
            "Content-Disposition": "inline; filename=scoreboard.png"
        },
    )
