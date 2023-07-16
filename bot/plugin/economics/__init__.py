import crescent

from ...locales.plugins import locale


group = crescent.Group(
    name=locale.LocaleBuilder(
        "economics",
        russian="экономика",
        ukrainian="економіка",
    ),
    description=locale.LocaleBuilder(
        "Economics",
        russian="Экономика",
        ukrainian="Економіка",
    ),
)
