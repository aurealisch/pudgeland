import collei
import crescent
import hikari

from pudgeland.plugin import action
from pudgeland.locale.plugin import locales
from pudgeland.utility.plugin import plugins

plugin = plugins.Plugin()


@action.group.child
@plugin.include
@crescent.command(
    name=locales.LocaleBuilder(
        "slap",
        ru="шлёпнуть",
        uk="шльопнути",
    ),
    description=locales.LocaleBuilder(
        "Slap",
        ru="Шлёпнуть пользователя",
        uk="Шльопнути користувача",
    ),
)
class Slap:
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
        await context.respond(
            embed=(
                hikari.Embed(
                    title="Шлёпнуть",
                    description=f"<@{context.user.id}> шлёпнул(а) <@{self.user.id}>",
                )
                .set_author(name=context.user.username, icon=context.user.avatar_url)
                .set_image(collei.Client().sfw.get(collei.SfwCategory.SLAP).url)
            )
        )
