import typing

import hikari

from .. import contexts

Color = typing.Literal[
    "default",
    "error",
    "success",
]

colors = {
    "default": "#4f686d",
    "error": "#ff4b4b",
    "success": "#77b35a",
}


def embed(
    color: Color,
    context: "contexts.Context",
    title: typing.Optional[str] = None,
    description: typing.Optional[str] = None,
    image: typing.Optional[hikari.Resourceish] = None,
) -> hikari.Embed:
    _color = hikari.Color.of(colors[color])

    contextual = context.user

    username = contextual.username
    avatar_url = contextual.avatar_url

    name = username
    icon = avatar_url

    _embed = (
        hikari.Embed(
            title=title,
            description=description,
            color=_color,
        )
        .set_author(
            name=name,
            icon=icon,
        )
        .set_image(image)
    )

    return _embed
