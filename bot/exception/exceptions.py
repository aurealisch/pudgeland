import hikari

from bot.locale.plugin import locales


class YouCantDoThat(Exception):
    def __init__(self, locale: hikari.Locale) -> None:
        super().__init__(
            locales.of(
                locale,
                locale_builder=locales.LocaleBuilder(
                    "You can't do that",
                    ru="Так нельзя",
                    uk="Так не можна",
                ),
            )
        )
