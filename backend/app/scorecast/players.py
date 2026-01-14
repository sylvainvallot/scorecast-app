from dataclasses import dataclass
from PIL import Image, ImageDraw, ImageFont
from app.config import settings, paths
from app.models import Player, PlayerCard

USER_CONFIG = settings.USER_CONFIG


def get_team_logo(team_id: str) -> Image.Image:
    logo_path = paths.TEAMS_LOGO_PATH / f"{team_id}.png"
    logo = Image.open(logo_path).convert("RGBA")
    return logo


def load_font(font_name: str, font_size: int) -> ImageFont.FreeTypeFont:
    font_path = paths.FONTS_PATH / font_name
    font = ImageFont.truetype(str(font_path), font_size)
    return font


def get_text_size(text: str, font) -> tuple[float, float, float, float]:
    dummy_img = Image.new('RGB', (1, 1))
    draw = ImageDraw.Draw(dummy_img)
    bbox = draw.textbbox((0, 0), text, font=font)
    return bbox


def format_player_tag(player: Player) -> str:
    """Format a player's tag as 'N. SURNAME #number'."""
    return (
        f"{player.name[0].upper()}. {player.surname.upper()} "
        f"#{player.player_number}"
    )


@dataclass(frozen=True, slots=True)
class PlayerBBox:
    text_bbox: tuple[float, float, float, float]
    width: float
    text_width: float
    text_height: float


def get_player_bbox(player_tag: str, font) -> PlayerBBox:
    padding = USER_CONFIG['playercard']['padding_px']
    text_bbox = get_text_size(player_tag, font)

    text_width = text_bbox[2] - text_bbox[0]
    text_height = text_bbox[3] - text_bbox[1]

    player_bbox_width = text_width + 2 * padding

    return PlayerBBox(
        text_bbox=text_bbox,
        width=player_bbox_width,
        text_width=text_width,
        text_height=text_height,
    )


def generate_playercard(playercard: PlayerCard) -> Image.Image:

    font_size = USER_CONFIG['playercard']['text_pts']
    card_height = int(USER_CONFIG['playercard']['height_px'])
    padding = USER_CONFIG['playercard']['padding_px']

    font = load_font(
        USER_CONFIG['playercard']['font'],
        font_size,
    )

    player_tag = format_player_tag(playercard.player)

    player_bbox = get_player_bbox(player_tag, font)

    logo_img = get_team_logo(playercard.team.id)
    scale = 1.5
    logo_img = logo_img.resize(
        (int(card_height * scale), int(card_height * scale)))

    logo_position = (
        -5,
        (card_height - logo_img.height) // 2,
    )

    card_width = int(player_bbox.width + logo_img.width)

    img = Image.new('RGBA', (card_width, card_height), (255, 255, 255, 0))
    draw = ImageDraw.Draw(img)

    draw.rounded_rectangle(
        [(0, 0), (card_width, card_height)],
        fill=playercard.team.color["primary"],
        radius=10,
    )

    img.paste(logo_img, logo_position, logo_img)

    draw.rounded_rectangle(
        [(0, 0), (card_width, card_height)],
        outline="white",
        width=5,
        radius=10,
    )

    text_position = (
        logo_img.width + padding // 2,
        (card_height - player_bbox.text_height) // 2
        - player_bbox.text_bbox[1],
    )

    draw.text(
        text_position,
        player_tag,
        font=font,
        fill="white",
    )

    return img
