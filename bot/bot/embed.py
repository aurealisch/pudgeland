import typing

import hikari

from bot import types

Color = typing.Literal["default", "err", "success", "applications", "coins",
                       "bananas", "monkeys", "profile", "diamonds",
                       "netheriteScraps", "accept", "reject"]

colors: typing.Mapping[Color, hikari.Colorish] = {
    "default": "#f0a43c",
    "err": "#ff4b4b",
    "success": "#77b35a",
    "applications": "#bb7f53",
    "coins": "#fbcd7a",
    "bananas": "#f9e9b1",
    "monkeys": "#cf8d5d",
    "profile": "#24649c",
    "diamonds": "#b3fcee",
    "netheriteScraps": "#441c14"
}
colors["accept"] = colors["success"]
colors["reject"] = colors["err"]


def embed(color: Color,
          title: typing.Optional[types.Title] = None,
          desc: typing.Optional[types.Description] = None) -> hikari.Embed:
    return hikari.Embed(title=title,
                        description=desc,
                        color=hikari.Color.of(colors.get(color)))
