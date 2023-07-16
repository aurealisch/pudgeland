import crescent
import hikari

from bot.plugin import action, plugins
from bot.plugin.locale import locales
from bot.plugin.middleware.action import pokes

plugin = plugins.Plugin()


@action.group.child
@plugin.include
@crescent.command(
    name=locales.LocaleBuilder(
        "poke",
        ru="тыкнуть",
        uk="тицьнути",
    ),
    description=locales.LocaleBuilder(
        "Poke",
        ru="Тыкнуть пользователя",
        uk="Тицьнути користувача",
    ),
)
class Poke:
    user = crescent.option(
        hikari.User,
        name=locales.LocaleBuilder(
            "user",
            ru="пользователь",
            uk="користувач",
        ),
        description=locales.LocaleBuilder(
            "User",
            ru="Пользователь",
            uk="Користувач",
        ),
    )

    # noinspection PyMethodMayBeStatic
    async def callback(self, context: crescent.Context) -> None:
        await pokes.Middleware(plugin).callback(context)
