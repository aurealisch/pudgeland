import crescent
import hikari

from pudgeland.plugin import economy

from ..module import locales
from ..utility import plugins

plugin = plugins.Plugin()


@economy.group.child
@plugin.include
@crescent.command(
    name=locales.LocaleBuilder(
        "information",
        russian="информация",
        ukrainian="інформація",
    ),
    description=locales.LocaleBuilder(
        "Information",
        russian="Информация",
        ukrainian="Iнформація",
    ),
)
class Information:
    user = crescent.option(
        hikari.User,
        name=locales.LocaleBuilder(
            "user",
            russian="пользователь",
            ukrainian="користувач",
        ),
        description=locales.LocaleBuilder(
            "User",
            russian="Пользователь",
            ukrainian="Користувач",
        ),
    )

    # noinspection PyMethodMayBeStatic
    async def callback(self, context: crescent.Context) -> None:
        pass
