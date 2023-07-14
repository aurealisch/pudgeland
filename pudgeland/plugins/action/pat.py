import crescent
import hikari

from pudgeland.plugins import action
from pudgeland.locales.plugins import locale
from pudgeland.utilities.plugins import plugins
from pudgeland.components.plugins.action import pat

plugin = plugins.Plugin()


@action.group.child
@plugin.include
@crescent.command(
    name=locale.LocaleBuilder(
        "pat",
        ru="погладить",
        uk="погладити",
    ),
    description=locale.LocaleBuilder(
        "Pat",
        ru="Погладить пользователя",
        uk="Погладити користувача",
    ),
)
class Pat:
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
        await pat.Component(plugin).callback(context)
