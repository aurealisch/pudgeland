import crescent
import hikari

from bot.plugin import action, plugins
from bot.plugin.locale import locales
from bot.plugin.middleware.action import bites

plugin = plugins.Plugin()


@action.group.child
@plugin.include
@crescent.command(
    name=locales.LocaleBuilder(
        "bite",
        russian="укусить",
        ukrainian="вкусити",
    ),
    description=locales.LocaleBuilder(
        "Bite the user",
        russian="Укусить пользователя",
        ukrainian="Вкусити користувача",
    ),
)
class Bite:
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
        await bites.Middleware(plugin).callback(context)
