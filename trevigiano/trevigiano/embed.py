import typing

import hikari

Color = typing.Literal[
    "default",
    "error",
    "success",
]

COLORS = {
    "default": "#f0a43c",
    "error": "#ff4b4b",
    "success": "#77b35a",
}


def embed(
    color: Color,
    title: typing.Optional[str] = None,
    description: typing.Optional[str] = None,
) -> hikari.Embed:
    COLOR = hikari.Color.of(COLORS[color])

    EMBED = hikari.Embed(
        title=title,
        description=description,
        color=COLOR,
    )

    return EMBED
