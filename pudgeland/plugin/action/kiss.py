import collei
import crescent
import hikari

from ..module import locales
from ..utility import plugins

plugin = plugins.Plugin()


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
        model = plugin.model
        client = model.client

        image = client.sfw.get(collei.SfwCategory.KISS)

        url = image.url

        title = "Поцеловать"
        description = f"<@{context.user.id}> поцеловал(а) <@{self.user.id}>"

        embed = hikari.Embed(title=title, description=description)

        embed.set_author(name=context.user.username, icon=context.user.avatar_url)
        embed.set_image(url)

        await context.respond(embed=embed)
