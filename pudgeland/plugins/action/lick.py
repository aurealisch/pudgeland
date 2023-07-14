import crescent
import hikari

from pudgeland.plugins import action
from pudgeland.locales.plugins import locale
from pudgeland.utilities.plugins import plugins
from pudgeland.components.plugins.action import lick

plugin = plugins.Plugin()


@action.group.child
@plugin.include
@crescent.command(
    name=locale.LocaleBuilder(
        "lick",
        russian="лизнуть",
        ukrainian="лизнути",
    ),
    description=locale.LocaleBuilder(
        "Lick the user",
        russian="Лизнуть пользователя",
        ukrainian="Лизнути користувача",
    ),
)
class Lick:
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
        await lick.Component(plugin).callback(context)
