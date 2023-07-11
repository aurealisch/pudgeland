import crescent

from ..module import locales


group = crescent.Group(
    name=locales.LocaleBuilder(
        "economy",
        russian="экономика",
        ukrainian="економіка",
    ),
    description=locales.LocaleBuilder(
        "Economy",
        russian="Экономика",
        ukrainian="Економіка",
    ),
)
