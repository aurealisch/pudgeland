import hikari

from bot.locale.plugin import locales


def helper(locale: hikari.Locale, localesBuilder: locales.LocaleBuilder) -> None:
    # Builds the locales for a command.
    _locales = localesBuilder.build()

    try:
        return _locales[locale]
    except KeyError:
        return localesBuilder.fallback
