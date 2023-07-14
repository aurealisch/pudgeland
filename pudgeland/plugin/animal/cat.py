import crescent
import hikari
import meowy

from pudgeland.plugin import animal
from pudgeland.locale.plugin import locales
from pudgeland.utility.plugin import plugins

plugin = plugins.Plugin()


@animal.group.child
@plugin.include
@crescent.command(
    name=locales.LocaleBuilder(
        "cat",
        russian="кот",
        ukrainian="кiт",
    ),
    description=locales.LocaleBuilder(
        "Image of a cat",
        russian="Изображение кота",
        ukrainian="Зображення кота",
    ),
)
class Cat:
    # noinspection PyMethodMayBeStatic
    async def callback(self, context: crescent.Context) -> None:
        await context.respond(
            embed=(
                hikari.Embed(
                    title="Кот",
                    description="Изображение кота",
                )
                .set_author(name=context.user.username, icon=context.user.avatar_url)
                .set_image(meowy.Client().images.search()[0].url)
            )
        )
