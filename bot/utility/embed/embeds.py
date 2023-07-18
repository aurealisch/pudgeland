import typing

import hikari

Color = typing.Literal["default", "exception", "success"]

colors = {
    "default": "#a93b3a",
    "exception": "#ff4b4b",
    "success": "#77b25a",
}


def embed(
    *,
    title: typing.Any,
    description: typing.Any,
    color: Color,
) -> hikari.Embed:
    """
    Other parameters
    ----------------
    - `title` : `typing.Any`
    - `description` : `typing.Any`
    - `color` : `Color`

    Returns
    -------
    `hikari.Embed`
    """
    _color = hikari.Color.of(colors[color])

    return hikari.Embed(
        title=title,
        description=description,
        color=_color,
    )
