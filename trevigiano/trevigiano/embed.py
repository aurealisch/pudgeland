import typing

import hikari

Color = typing.Literal[
    'default',
    'error',
    'success',
]

colors: typing.Mapping[Color, hikari.Colorish] = {
    'default': '#f0a43c',
    'error': '#ff4b4b',
    'success': '#77b35a',
}


def embed(color: Color,
          title: str | None = None,
          description: str | None = None) -> hikari.Embed:
    color = hikari.Color.of(colors.get(color))

    embed = hikari.Embed(
        title=title,
        description=description,
        color=color,
    )

    return embed
