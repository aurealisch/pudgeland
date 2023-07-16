import crescent
import hikari

from bot.plugin import action, plugins
from bot.plugin.locale import locales
from bot.plugin.middleware.action import hugs

plugin = plugins.Plugin()


@action.group.child
@plugin.include
@crescent.command(
    name=locales.LocaleBuilder(
        "hug",
        russian="обнять",
        ukrainian="обійняти",
    ),
    description=locales.LocaleBuilder(
        "Hug the user",
        russian="Обнять пользователя",
        ukrainian="Обійняти користувача",
    ),
)
class Hug:
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
        await hugs.Middleware(plugin).callback(context)
