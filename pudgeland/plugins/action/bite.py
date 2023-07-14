import crescent
import hikari

from pudgeland.plugins import action
from pudgeland.locales.plugins import locale
from pudgeland.utilities.plugins import plugins
from pudgeland.components.plugins.action import bite

plugin = plugins.Plugin()


@action.group.child
@plugin.include
@crescent.command(
    name=locale.LocaleBuilder(
        "bite",
        russian="укусить",
        ukrainian="вкусити",
    ),
    description=locale.LocaleBuilder(
        "Bite the user",
        russian="Укусить пользователя",
        ukrainian="Вкусити користувача",
    ),
)
class Bite:
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
        await bite.Component(plugin).callback(context)
