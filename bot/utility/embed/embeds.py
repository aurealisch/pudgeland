import typing

import hikari

from bot.common import commons

Mode = typing.Literal["default", "error", "success"]

colors = {
    "default": commons.environment.DEFAULT_MODE_COLOR,
    "error": commons.environment.ERROR_MODE_COLOR,
    "success": commons.environment.SUCCESS_MODE_COLOR,
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
