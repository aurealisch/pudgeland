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
        "poke",
        ru="тыкнуть",
        uk="тицьнути",
    ),
    description=locales.LocaleBuilder(
        "Poke",
        ru="Тыкнуть пользователя",
        uk="Тицьнути користувача",
    ),
)
class Poke:
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
                    title="Тыкнуть",
                    description=f"<@{context.user.id}> тыкнул(а) <@{self.user.id}>",
                )
                .set_author(name=context.user.username, icon=context.user.avatar_url)
                .set_image(collei.Client().sfw.get(collei.SfwCategory.POKE).url)
            )
        )
