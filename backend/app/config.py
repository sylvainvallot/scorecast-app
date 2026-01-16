import tomllib
import json
from pydantic_settings import BaseSettings
from pathlib import Path

BASE_DIR: Path = Path(__file__).resolve().parents[2]


class Settings(BaseSettings):
    TITLE: str = "Scorecast API"
    DESCRIPTION: str = "API for Scorecast application"
    VERSION: str = "1.0.0"
    API_STR: str = "/api/py"
    USER_CONFIG: dict = tomllib.load(open(BASE_DIR / "config.toml", "rb"))
    USER_DB: dict = json.load(open(BASE_DIR / "db.json", "r"))


class Paths(BaseSettings):
    USER_PLAYERS_CSV: Path = BASE_DIR / "players.csv"
    BASE_DIR: Path = Path(__file__).resolve().parents[2]
    ASSETS_PATH: Path = BASE_DIR / "assets"
    FONTS_PATH: Path = ASSETS_PATH / "fonts"
    PLAYERS_PATH: Path = ASSETS_PATH / "players"
    TEAMS_LOGO_PATH: Path = ASSETS_PATH / "logos"
    RESULTS_OVERLAY_PATH: Path = ASSETS_PATH / "result_overlays"

    OUTPUT_VIDEOS_PATH: Path = BASE_DIR / "output_scorecasts"


settings = Settings()
paths = Paths()
