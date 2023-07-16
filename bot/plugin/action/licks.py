import crescent
import hikari

from bot.plugin import action, plugins
from bot.plugin.locale import locales
from bot.plugin.middleware.action import licks

plugin = plugins.Plugin()


@action.group.child
@plugin.include
@crescent.command(
    name=locales.LocaleBuilder(
        "lick",
        russian="лизнуть",
        ukrainian="лизнути",
    ),
    description=locales.LocaleBuilder(
        "Lick the user",
        russian="Лизнуть пользователя",
        ukrainian="Лизнути користувача",
    ),
)
class Lick:
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
        await licks.Middleware(plugin).callback(context)
