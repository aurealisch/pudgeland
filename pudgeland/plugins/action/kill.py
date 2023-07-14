import crescent
import hikari

from pudgeland.plugins import action
from pudgeland.locales.plugins import locale
from pudgeland.utilities.plugins import plugins
from pudgeland.components.plugins.action import kill

plugin = plugins.Plugin()


@action.group.child
@plugin.include
@crescent.command(
    name=locale.LocaleBuilder(
        "kill",
        ru="убить",
        uk="вбивати",
    ),
    description=locale.LocaleBuilder(
        "Kill",
        ru="Убить пользователя",
        uk="Вбивати користувача",
    ),
)
class Kill:
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
        await kill.Component(plugin).callback(context)
