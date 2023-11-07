import typing

import hikari

Color = typing.Literal[
    "default",
    "error",
    "success",
    "coins",
    "bananas",
    "monkeys",
    "profile",
    "diamonds",
    "netheriteScraps",
]

colors: typing.Mapping[Color, hikari.Colorish] = {
    "default": "#f0a43c",
    "error": "#ff4b4b",
    "success": "#77b35a",
    "coins": "#fbcd7a",
    "bananas": "#f9e9b1",
    "monkeys": "#cf8d5d",
    "profile": "#24649c",
    "diamonds": "#b3fcee",
    "netheriteScraps": "#441c14",
}


def embed(
    color: Color,
    title: typing.Optional[str] = None,
    description: typing.Optional[str] = None,
) -> hikari.Embed:
    """Description"""
    color = hikari.Color.of(colors.get(color))

    embed = hikari.Embed(title=title, description=description, color=color)

    return embed
