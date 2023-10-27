import typing

import hikari

Color = typing.Literal[
    "default",
    "error",
    "success",
    "coins",
    "berries",
    "foxes",
    "profile",
    "diamonds",
    "netheriteScraps",
]

colors: typing.Mapping[Color, hikari.Colorish] = {
    "default": "#f0a43c",
    "error": "#ff4b4b",
    "success": "#77b35a",
    "coins": "#fbcd7a",
    "berries": "#b51f2a",
    "foxes": "#a85c22",
    "profile": "#24649c",
    "diamonds": "#b3fcee",
    "netheriteScraps": "#441c14",
}


def embed(
    color: Color,
    title: typing.Optional[str] = None,
    description: typing.Optional[str] = None,
) -> hikari.Embed:
    """Description

    Parameters
    ----------
    color : Color
        Description
    title : typing.Optional[str]
        Defaults to `None`
        Description
    description : typing.Optional[str]
        Defaults to `None`
        Description

    Returns
    -------
    hikari.Embed
        Description
    """
    color = hikari.Color.of(colors.get(color))

    embed = hikari.Embed(title=title, description=description, color=color)

    return embed
