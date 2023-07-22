import crescent

from bot.locale import locales


group = crescent.Group(
    name=locales.LocaleBuilder(
        "reputation",
        ru="репутация",
        uk="репутація",
    ),
    description=locales.LocaleBuilder(
        "Reputation",
        ru="Репутация",
        uk="Репутація",
    ),
)
