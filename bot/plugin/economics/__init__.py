import crescent

from bot.plugin.locale import locales

group = crescent.Group(
    name=locales.LocaleBuilder(
        "economics",
        russian="экономика",
        ukrainian="економіка",
    ),
    description=locales.LocaleBuilder(
        "Economics",
        russian="Экономика",
        ukrainian="Економіка",
    ),
)
