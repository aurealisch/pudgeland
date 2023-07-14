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
        "kiss",
        russian="поцеловать",
        ukrainian="поцілувати",
    ),
    description=locales.LocaleBuilder(
        "Kiss the user",
        russian="Поцеловать пользователя",
        ukrainian="Поцілувати користувача",
    ),
)
class Kiss:
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
                    title="Поцеловать",
                    description=f"<@{context.user.id}> поцеловал(а) <@{self.user.id}>",
                )
                .set_author(name=context.user.username, icon=context.user.avatar_url)
                .set_image(collei.Client().sfw.get(collei.SfwCategory.KISS).url)
            )
        )
