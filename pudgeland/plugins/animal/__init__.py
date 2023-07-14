import crescent

from ...locales.plugins import locale

group = crescent.Group(
    name=locale.LocaleBuilder(
        "animal",
        russian="животное",
        ukrainian="тварина",
    ),
    description=locale.LocaleBuilder(
        "Animal",
        russian="Животное",
        ukrainian="Тварина",
    ),
)
