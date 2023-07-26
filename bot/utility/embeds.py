import typing

import hikari

Mode = typing.Literal["default", "error", "success"]

modesAndColors = {"default": "#4f686d", "error": "#ff4b4b", "success": "#77b35a"}


def embed(
    __mode: Mode, /, *, title: str | None, description: str | None
) -> hikari.Embed:
    color = hikari.Color.of(modesAndColors[__mode])

    return hikari.Embed(title=title, description=description, color=color)
