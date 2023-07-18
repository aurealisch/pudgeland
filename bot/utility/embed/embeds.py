import typing

import hikari

from bot.common import commons

Mode = typing.Literal["default", "error", "success"]

colors = {
    "default": commons.environment.default_mode_color,
    "error": commons.environment.error_mode_color,
    "success": commons.environment.success_mode_color,
}


def embed(
    *,
    mode: Mode,
    title: typing.Any = None,
    description: typing.Any = None,
) -> hikari.Embed:
    """
    Other parameters
    ----------------
    - `mode` : `Mode`
    - `title` : `typing.Any` = `None`
    - `description` : `typing.Any` = `None`

    Returns
    -------
    `hikari.Embed`
    """
    color = hikari.Color.of(colors[mode])

    return hikari.Embed(
        title=title,
        description=description,
        color=color,
    )
