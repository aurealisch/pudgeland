import crescent

from ...locales.plugins import locale

group = crescent.Group(
    name=locale.LocaleBuilder(
        "action",
        russian="действие",
        ukrainian="дія",
    ),
    description=locale.LocaleBuilder(
        "Action",
        russian="Действие",
        ukrainian="Дія",
    ),
)
