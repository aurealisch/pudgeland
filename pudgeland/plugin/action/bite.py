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
        "bite",
        russian="укусить",
        ukrainian="вкусити",
    ),
    description=locales.LocaleBuilder(
        "Bite the user",
        russian="Укусить пользователя",
        ukrainian="Вкусити користувача",
    ),
)
class Bite:
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

        image = client.sfw.get(collei.SfwCategory.BITE)

        url = image.url

        title = "Укусить"
        description = f"""\
            <@{context.user.id}> укусил(а) <@{self.user.id}>
        """

        embed = hikari.Embed(title=title, description=description)

        embed.set_author(name=context.user.username, icon=context.user.avatar_url)
        embed.set_image(url)

        await context.respond(embed=embed)
