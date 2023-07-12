import collei
import crescent
import hikari

from pudgeland.plugin import action

from ..module import locales
from ..utility import plugins

plugin = plugins.Plugin()


@action.group.child
@plugin.include
@crescent.command(
    name=locales.LocaleBuilder(
        "lick",
        russian="лизнуть",
        ukrainian="лизнути",
    ),
    description=locales.LocaleBuilder(
        "Lick the user",
        russian="Лизнуть пользователя",
        ukrainian="Лизнути користувача",
    ),
)
class Lick:
    user = crescent.option(
        hikari.User,
        name=locales.LocaleBuilder(
            "user",
            russian="пользователь",
            ukrainian="користувач",
        ),
        description=locales.LocaleBuilder(
            "User",
            russian="Пользователь",
            ukrainian="Користувач",
        ),
    )

    # noinspection PyMethodMayBeStatic
    async def callback(self, context: crescent.Context) -> None:
        image = collei.Client().sfw.get(collei.SfwCategory.LICK)

        await context.respond(
            embed=(
                hikari.Embed(
                    title="Лизнуть",
                    description=f"<@{context.user.id}> лизнул(а) <@{self.user.id}>",
                )
                .set_author(name=context.user.username, icon=context.user.avatar_url)
                .set_image(image.url)
            )
        )
