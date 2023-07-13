import crescent

from ..module import locales

group = crescent.Group(
    name=locales.LocaleBuilder(
        "animal",
        russian="животное",
        ukrainian="тварина",
    ),
    description=locales.LocaleBuilder(
        "Animal",
        russian="Животное",
        ukrainian="Тварина",
    ),
)
