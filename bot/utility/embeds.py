import typing

import hikari

Mode = typing.Literal["default", "error", "success"]

modes_and_colors = {"default": "#4f686d", "error": "#ff4b4b", "success": "#77b35a"}


def embed(
    __mode: Mode, /, *, title: str | None, description: str | None
) -> hikari.Embed:
    color = hikari.Color.of(modes_and_colors[__mode])

    return hikari.Embed(title=title, description=description, color=color)
