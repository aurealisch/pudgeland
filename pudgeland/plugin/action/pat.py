import crescent
import hikari

from pudgeland.plugin import action
from pudgeland.locale.plugin import locales
from pudgeland.utility.plugin import plugins
from pudgeland.component.plugin.action import pat

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
        await pat.Component(plugin).callback(context)
