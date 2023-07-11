import collei
import crescent
import hikari

from ..module import locales
from ..utility import plugins

plugin = plugins.Plugin()


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
        model = plugin.model
        client = model.client

        image = client.sfw.get(collei.SfwCategory.HUG)

        url = image.url

        title = "Обнять"
        description = f"""\
            <@{context.user.id}> обнял(а) <@{self.user.id}>
        """

        embed = hikari.Embed(title=title, description=description)

        embed.set_author(name=context.user.username, icon=context.user.avatar_url)
        embed.set_image(url)

        await context.respond(embed=embed)
