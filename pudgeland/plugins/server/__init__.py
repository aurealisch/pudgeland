import crescent

from ...locales.plugins import locale


group = crescent.Group(
    name=locale.LocaleBuilder(
        "server",
        russian="сервер",
        ukrainian="сервер",
    ),
    description=locale.LocaleBuilder(
        "Server",
        russian="Сервер",
        ukrainian="Сервер",
    ),
)
