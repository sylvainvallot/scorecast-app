import os
from pathlib import Path
from typing import Optional
import numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageFilter
from moviepy.video.io.VideoFileClip import VideoFileClip
from moviepy.video.VideoClip import ImageClip
from moviepy.video.compositing.CompositeVideoClip import CompositeVideoClip
from app.config import settings, paths
from app.models import TeamScoreBoard
from app.scorecast.utils import draw_text_center, format_score

USER_CONFIG = settings.USER_CONFIG


def generate_scoreboard(
    home_team: TeamScoreBoard,
    away_team: TeamScoreBoard,
    period: Optional[str] = "full_time",
    style: Optional[str] = "default",
) -> Image.Image:

    SQUARE_COUNT = 4
    SQUARE_SIZE = USER_CONFIG['scoreboard']['square_size_px']
    BG_COLOR = (0, 0, 0, 0)
    img_width, img_height = SQUARE_SIZE * SQUARE_COUNT, SQUARE_SIZE

    img = Image.new('RGBA', (img_width, img_height), BG_COLOR)
    draw = ImageDraw.Draw(img)

    colors = [
        tuple(home_team.color.color_rgb['primary']),
        tuple(home_team.color.color_rgb['secondary']),
        tuple(away_team.color.color_rgb['secondary']),
        tuple(away_team.color.color_rgb['primary']),
    ]

    # Draw squares
    for i, color in enumerate(colors):
        x1 = i * SQUARE_SIZE
        x2 = x1 + SQUARE_SIZE
        draw.rectangle([x1, 0, x2, img_height], fill=color)

    def logo_path(team_id: str, style: Optional[str] = "default") -> Path:
        logo_file = f"{team_id}_{style}.png"
        logo_path = paths.TEAMS_LOGO_PATH / logo_file
        if not os.path.exists(logo_path):
            logo_path = paths.TEAMS_LOGO_PATH / f"{team_id}.png"
        return logo_path

    def load_logo(path: Path, style: Optional[str] = "default") -> Image.Image:
        LOGO_MARGIN = 40
        if style == "modern":
            LOGO_MARGIN = 0
        logo = Image.open(path).convert("RGBA")
        logo = logo.resize(
            (SQUARE_SIZE - LOGO_MARGIN, SQUARE_SIZE - LOGO_MARGIN))
        return logo

    POSITION_OFFSET = 20

    if style == "modern":
        POSITION_OFFSET = 0

    # Load logos
    home_logo = load_logo(logo_path(home_team.id, style), style)

    img.paste(home_logo, (POSITION_OFFSET, POSITION_OFFSET), home_logo)

    if os.path.exists(logo_path(away_team.id, style)):
        away_logo = load_logo(logo_path(away_team.id, style), style)
        img.paste(away_logo, (SQUARE_SIZE * 3 +
                  POSITION_OFFSET, POSITION_OFFSET), away_logo)
    else:
        # FallBack to First Letter if Logo Missing
        draw_text_center(
            draw,
            (SQUARE_SIZE * 3 + SQUARE_SIZE // 2, img_height // 2),
            away_team.id[0].upper(),
            ImageFont.truetype(
                paths.FONTS_PATH / USER_CONFIG['scoreboard']['fallback_font'],
                USER_CONFIG['scores']['text_pts']
            ),
            "white",
        )

    BASE_FONT_SIZE = USER_CONFIG['scores']['text_pts']
    SCORE_FONT = USER_CONFIG['scores']['font']

    # Reduce font size if scores are over 2 digits
    if home_team.score > 99 or away_team.score > 99:
        BASE_FONT_SIZE = BASE_FONT_SIZE - 20

    scorefont = ImageFont.truetype(
        paths.FONTS_PATH / f"{SCORE_FONT}", BASE_FONT_SIZE)

    home_score = format_score(home_team.score or 0)
    away_score = format_score(away_team.score or 0)

    home_score_square = (SQUARE_SIZE * 1 + SQUARE_SIZE // 2, img_height // 2)
    away_score_square = (SQUARE_SIZE * 2 + SQUARE_SIZE // 2, img_height // 2)

    draw_text_center(
        draw,
        home_score_square,
        str(home_score),
        scorefont,
        "white",
    )

    draw_text_center(
        draw,
        away_score_square,
        str(away_score),
        scorefont,
        "white",
    )

    def draw_half_time_text(img):
        HT_H = USER_CONFIG["half_time"]["height_px"]
        HT_W = SQUARE_SIZE * 3
        PIXEL_OFFSET = 1

        ht_img = Image.new('RGBA', (img_width, img_height+HT_H), BG_COLOR)
        ht_img.paste(img, (0, HT_H))
        ht_img_draw = ImageDraw.Draw(ht_img)

        x1, y1 = SQUARE_SIZE, 0
        x2, y2 = HT_W - PIXEL_OFFSET, HT_H - PIXEL_OFFSET

        ht_img_draw.rectangle(
            [x1, y1, x2, y2],
            fill="white",
        )

        HALF_TIME_FONT = USER_CONFIG["half_time"]["font"]
        HALF_TIME_TEXT_PTS = USER_CONFIG["half_time"]["text_pts"]

        ht_font = ImageFont.truetype(
            paths.FONTS_PATH / f"{HALF_TIME_FONT}", size=HALF_TIME_TEXT_PTS)
        ht_text = USER_CONFIG["half_time"][period]

        ht_center = (img_width // 2, HT_H // 2)

        draw_text_center(ht_img_draw, ht_center, ht_text,
                         font=ht_font, fill="black")

        return ht_img

    ht_img = draw_half_time_text(img)

    def draw_subteam_text(img: Image.Image):
        ST_H = 40
        PIXEL_OFFSET = 1

        SUB_TEAM_FONT = USER_CONFIG["sub_teams"]["font"]
        SUB_TEAM_TEXT_PTS = USER_CONFIG["sub_teams"]["text_pts"]

        subteam_font = ImageFont.truetype(
            paths.FONTS_PATH / f"{SUB_TEAM_FONT}", size=SUB_TEAM_TEXT_PTS)
        subteam_img = Image.new(
            'RGBA', (img.width, img.height+ST_H), BG_COLOR)
        subteam_img.paste(img, (0, 0))
        subteam_draw = ImageDraw.Draw(subteam_img)

        def draw_tag_text(x1, y1, x2, y2, text: str):
            subteam_draw.rectangle(
                [x1, y1, x2, y2],
                fill="white",
            )
            subteam_bbox = subteam_draw.textbbox(
                (0, 0), text, font=subteam_font)
            subteam_text_width = subteam_bbox[2] - subteam_bbox[0]
            subteam_text_height = subteam_bbox[3] - subteam_bbox[1]
            subteam_x = (x1 + (x2 - x1) // 2) - (
                subteam_text_width // 2)
            subteam_y = y2 - (ST_H // 2) - (
                subteam_text_height // 2) - subteam_bbox[1]
            subteam_draw.text((subteam_x, subteam_y),
                              text, font=subteam_font, fill="black")

        if home_team.subteam:
            draw_tag_text(
                0,
                img.height,
                SQUARE_SIZE - PIXEL_OFFSET,
                img.height + ST_H,
                home_team.subteam.upper()
            )

        if away_team.subteam:
            draw_tag_text(
                SQUARE_SIZE * 3,
                img.height,
                SQUARE_SIZE * 4,
                img.height + ST_H,
                away_team.subteam.upper()
            )

        return subteam_img

    subteam_img = draw_subteam_text(ht_img)

    return subteam_img


def generate_video(
    filename: str,
    scoreboard: Image.Image,
    result: str,
    player_name: str,
):

    # Load celebration video
    video = VideoFileClip(
        paths.PLAYERS_PATH / f"{player_name}" / f"{result}_{player_name}.mov",
        has_mask=True)

    background_image = (
        ImageClip(paths.ASSETS_PATH / "bg_player.png", transparent=True)
        .with_duration(video.duration)
        .with_position(("center", "center"))
    )

    result_overlay = (
        ImageClip(
            paths.RESULTS_OVERLAY_PATH / f"overlay_{result}.png",
            transparent=True
        )
        .with_duration(video.duration)
        .with_position(("center", "center"))
    )

    # player_tag = (
    #     ImageClip(f"player_{player_name}.png", transparent=True)
    #     .with_duration(video.duration)
    #     .with_position(("center", "center"))
    # )

    score_board_np = np.array(scoreboard)
    score_board_position = (
        (video.w - score_board_np.shape[1]) // 2,
        video.h - score_board_np.shape[0] - 100
    )
    score_board = (
        ImageClip(score_board_np, transparent=True)
        .with_duration(video.duration)
        .with_position(score_board_position)
    )
    # score_board = resize(score_board, width=video.w * 0.8)

    # Composite text over video
    final = CompositeVideoClip([
        background_image,
        result_overlay,
        # player_tag,
        video,
        score_board,
    ])

    # Export
    final.write_videofile(
        paths.OUTPUT_VIDEOS_PATH / f"{filename}.mp4",
        codec="libx264",
        fps=30,
        audio=False
    )


def generate_image(
    scoreboard: Image.Image,
    subteam: Optional[str] = None,
) -> Image.Image:

    bg = Image.open(paths.ASSETS_PATH / "static_team_a.png").convert("RGBA")

    if subteam:
        # Load background based on subteam
        bg_path = paths.ASSETS_PATH / \
            f"static_{subteam.lower().replace(' ', '_')}.png"
        if os.path.exists(bg_path):
            bg = Image.open(bg_path).convert("RGBA")

    # Position scoreboard at bottom center
    sb_width, sb_height = scoreboard.size
    bg_width, bg_height = bg.size
    position = ((bg_width - sb_width) // 2, bg_height - sb_height - 50)

    # Composite scoreboard onto background
    combined = bg.copy()
    combined.paste(scoreboard, position, scoreboard)
    return combined
