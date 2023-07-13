import crescent

from ..module import locales

group = crescent.Group(
    name=locales.LocaleBuilder(
        "action",
        russian="действие",
        ukrainian="дія",
    ),
    description=locales.LocaleBuilder(
        "Action",
        russian="Действие",
        ukrainian="Дія",
    ),
)
