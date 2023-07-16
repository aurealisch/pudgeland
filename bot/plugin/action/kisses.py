import crescent
import hikari

from bot.plugin import action, plugins
from bot.plugin.locale import locales
from bot.plugin.middleware.action import kisses

plugin = plugins.Plugin()


@action.group.child
@plugin.include
@crescent.command(
    name=locales.LocaleBuilder(
        "kiss",
        russian="поцеловать",
        ukrainian="поцілувати",
    ),
    description=locales.LocaleBuilder(
        "Kiss the user",
        russian="Поцеловать пользователя",
        ukrainian="Поцілувати користувача",
    ),
)
class Kiss:
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
        await kisses.Middleware(plugin).callback(context)
