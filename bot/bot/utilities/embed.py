import typing

import hikari

Color = typing.Literal[
    "error",
    "cooldown",
    "banana",
    "monkey",
    "coin",
    "diamond",
    "netherite",
    "profile",
]

colors: typing.Mapping[Color, hikari.Colorish] = {
    "error": "#ff4b4b",
    "cooldown": "#000000",
    "banana": "#f9e9b1",
    "monkey": "#cf8d5d",
    "coin": "#fbcd7a",
    "diamond": "#b3fcee",
    "netherite": "#441c14",
    "profile": "#24649c",
}

Title = typing.Literal[
    "error",
    "cooldown",
    "leaders-banana",
    "leaders-coin",
    "leaders-diamond",
    "leaders-monkey",
    "leaders-netherite",
    "purchase-coin",
    "purchase-diamond",
    "purchase-netherite",
    "sale-coin",
    "sale-diamond",
    "sale-netherite",
    "collecting",
    "domestication",
    "profile",
]

titles: typing.Mapping[Title, str] = {
    "error": "https://i.ibb.co/8B7wzBV/image.png",
    "cooldown": "https://i.ibb.co/sjdMw6P/image.png",
    "leaders-banana": "https://i.ibb.co/cXcD7yT/image.png",
    "leaders-coin": "https://i.ibb.co/d2FDvqk/image.png",
    "leaders-diamond": "https://i.ibb.co/7JdB6xK/image.png",
    "leaders-monkey": "https://i.ibb.co/4sv9VVM/image.png",
    "leaders-netherite": "https://i.ibb.co/TkBBsmK/image.png",
    "purchase-coin": "https://i.ibb.co/vdx0tY3/image.png",
    "purchase-diamond": "https://i.ibb.co/zngyGFJ/image.png",
    "purchase-netherite": "https://i.ibb.co/BK27kkk/image.png",
    "sale-coin": "https://i.ibb.co/wp9v6Vs/image.png",
    "sale-diamond": "https://i.ibb.co/s90YqGZ/image.png",
    "sale-netherite": "https://i.ibb.co/m4NGDvb/image.png",
    "collecting": "https://i.ibb.co/thyvDNC/image.png",
    "domestication": "https://i.ibb.co/jDGy2bL/image.png",
    "profile": "https://i.ibb.co/rGjmy9Y/image.png",
}


def embed(
    color: Color, title: Title, description: typing.Optional[str] = None
) -> typing.Sequence[hikari.Embed]:
    return [
        hikari.Embed(color=hikari.Color.of(colors[color])).set_image(titles[title]),
        hikari.Embed(description=description, color=hikari.Color.of("#04bcd4")),
    ]
