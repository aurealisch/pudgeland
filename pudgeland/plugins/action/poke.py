import crescent
import hikari

from pudgeland.plugins import action
from pudgeland.locales.plugins import locale
from pudgeland.utilities.plugins import plugins
from pudgeland.components.plugins.action import poke

plugin = plugins.Plugin()


@action.group.child
@plugin.include
@crescent.command(
    name=locale.LocaleBuilder(
        "poke",
        ru="тыкнуть",
        uk="тицьнути",
    ),
    description=locale.LocaleBuilder(
        "Poke",
        ru="Тыкнуть пользователя",
        uk="Тицьнути користувача",
    ),
)
class Poke:
    user = crescent.option(
        hikari.User,
        name=locale.LocaleBuilder(
            "user",
            ru="пользователь",
            uk="користувач",
        ),
        description=locale.LocaleBuilder(
            "User",
            ru="Пользователь",
            uk="Користувач",
        ),
    )

    # noinspection PyMethodMayBeStatic
    async def callback(self, context: crescent.Context) -> None:
        await poke.Component(plugin).callback(context)
