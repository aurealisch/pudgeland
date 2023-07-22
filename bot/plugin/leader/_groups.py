import crescent

from bot.locale import locales


group = crescent.Group(
    name=locales.LocaleBuilder(
        "leaders",
        ru="лидеры",
        uk="лідери",
    ),
    description=locales.LocaleBuilder(
        "Leaders",
        ru="Лидеры",
        uk="Лідери",
    ),
)
