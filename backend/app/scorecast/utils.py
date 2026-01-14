def format_score(score: int) -> str:
    """Format score to always have two digits

    Args:
        score (int): score

    Returns:
        str: 2 digits score
    """
    return f"{score:02d}"


def draw_text_center(draw, center, text, font, fill):
    """Draw text centered at a given position"""
    text_bbox = draw.textbbox((0, 0), text, font=font)

    text_width = text_bbox[2] - text_bbox[0]
    text_height = text_bbox[3] - text_bbox[1]

    x = center[0] - text_width // 2
    y = center[1] - text_height // 2 - text_bbox[1]

    draw.text((x, y), text, font=font, fill=fill)
