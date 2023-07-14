import crescent
import hikari

from pudgeland.plugins import action
from pudgeland.locales.plugins import locale
from pudgeland.utilities.plugins import plugins
from pudgeland.components.plugins.action import kiss

plugin = plugins.Plugin()


@action.group.child
@plugin.include
@crescent.command(
    name=locale.LocaleBuilder(
        "kiss",
        russian="поцеловать",
        ukrainian="поцілувати",
    ),
    description=locale.LocaleBuilder(
        "Kiss the user",
        russian="Поцеловать пользователя",
        ukrainian="Поцілувати користувача",
    ),
)
class Kiss:
    user = crescent.option(
        hikari.User,
        name=locale.LocaleBuilder(
            "user",
            russian="пользователь",
            ukrainian="користувач",
        ),
        description=locale.LocaleBuilder(
            "User",
            russian="Пользователь",
            ukrainian="Користувач",
        ),
    )

    # noinspection PyMethodMayBeStatic
    async def callback(self, context: crescent.Context) -> None:
        await kiss.Component(plugin).callback(context)
