import crescent
import hikari

from bot.plugin import action, plugins
from bot.plugin.locale import locales
from bot.plugin.middleware.action import kills

plugin = plugins.Plugin()


@action.group.child
@plugin.include
@crescent.command(
    name=locales.LocaleBuilder(
        "kill",
        ru="убить",
        uk="вбивати",
    ),
    description=locales.LocaleBuilder(
        "Kill",
        ru="Убить пользователя",
        uk="Вбивати користувача",
    ),
)
class Kill:
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
        await kills.Middleware(plugin).callback(context)
