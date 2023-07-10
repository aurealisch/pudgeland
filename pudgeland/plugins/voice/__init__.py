import crescent

from ..modules import locales


group = crescent.Group(
    name=locales.LocaleBuilder(
        "voice",
        russian="голос",
        ukrainian="голос",
    ),
    description=locales.LocaleBuilder(
        "Voice",
        russian="Голос",
        ukrainian="Голос",
    ),
)
