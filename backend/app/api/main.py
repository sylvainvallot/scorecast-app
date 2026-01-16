from fastapi import APIRouter
from app.api.routes import utils, teams, scorecast, players

api_router = APIRouter()
api_router.include_router(utils.router)
api_router.include_router(teams.router)
api_router.include_router(players.router)
api_router.include_router(scorecast.router)
