import crescent

from ...locale.plugin import locales


group = crescent.Group(
    name=locales.LocaleBuilder(
        "server",
        russian="сервер",
        ukrainian="сервер",
    ),
    description=locales.LocaleBuilder(
        "Server",
        russian="Сервер",
        ukrainian="Сервер",
    ),
)
