import crescent

from bot.plugin.locale import locales

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
