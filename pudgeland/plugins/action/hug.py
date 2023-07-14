import crescent
import hikari

from pudgeland.plugins import action
from pudgeland.locales.plugins import locale
from pudgeland.utilities.plugins import plugins
from pudgeland.components.plugins.action import hug

plugin = plugins.Plugin()


@action.group.child
@plugin.include
@crescent.command(
    name=locale.LocaleBuilder(
        "hug",
        russian="обнять",
        ukrainian="обійняти",
    ),
    description=locale.LocaleBuilder(
        "Hug the user",
        russian="Обнять пользователя",
        ukrainian="Обійняти користувача",
    ),
)
class Hug:
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
        await hug.Component(plugin).callback(context)
