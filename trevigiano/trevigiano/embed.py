import typing

import hikari

Color = typing.Literal[
    "default",
    "error",
    "success",
]

COLORS: typing.Mapping[Color, hikari.Colorish] = {
    "default": "#f0a43c",
    "error": "#ff4b4b",
    "success": "#77b35a",
}

def embed(
    color: Color,
    title: str | None = None,
    description: str | None = None,
) -> hikari.Embed:
    COLOR = hikari.Color.of(COLORS.get(color))

    EMBED = hikari.Embed(
        title=title,
        description=description,
        color=COLOR,
    )

    return EMBED
