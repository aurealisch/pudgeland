import crescent

from ...locale import locales

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
