import crescent
import hikari

from bot.plugin import action, plugins
from bot.plugin.locale import locales
from bot.plugin.middleware.action import pats

plugin = plugins.Plugin()


@action.group.child
@plugin.include
@crescent.command(
    name=locales.LocaleBuilder(
        "pat",
        ru="погладить",
        uk="погладити",
    ),
    description=locales.LocaleBuilder(
        "Pat",
        ru="Погладить пользователя",
        uk="Погладити користувача",
    ),
)
class Pat:
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
        await pats.Middleware(plugin).callback(context)
