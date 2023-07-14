import collei
import crescent
import hikari

from pudgeland.plugin import action
from pudgeland.locale import locales

from ..utility import plugins

plugin = plugins.Plugin()


@action.group.child
@plugin.include
@crescent.command(
    name=locales.LocaleBuilder(
        "hug",
        russian="обнять",
        ukrainian="обійняти",
    ),
    description=locales.LocaleBuilder(
        "Hug the user",
        russian="Обнять пользователя",
        ukrainian="Обійняти користувача",
    ),
)
class Hug:
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
        await context.respond(
            embed=(
                hikari.Embed(
                    title="Обнять",
                    description=f"<@{context.user.id}> обнял(а) <@{self.user.id}>",
                )
                .set_author(name=context.user.username, icon=context.user.avatar_url)
                .set_image(collei.Client().sfw.get(collei.SfwCategory.HUG).url)
            )
        )
