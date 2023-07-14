import crescent
import hikari
import woofy

from pudgeland.plugin import animal
from pudgeland.locale import locales
from pudgeland.utility import plugins

plugin = plugins.Plugin()


@animal.group.child
@plugin.include
@crescent.command(
    name=locales.LocaleBuilder(
        "dog",
        russian="собака",
        ukrainian="пес",
    ),
    description=locales.LocaleBuilder(
        "Image of a dog",
        russian="Изображение собаки",
        ukrainian="Зображення собаки",
    ),
)
class Dog:
    # noinspection PyMethodMayBeStatic
    async def callback(self, context: crescent.Context) -> None:
        await context.respond(
            embed=(
                hikari.Embed(
                    title="Собака",
                    description="Изображение собаки",
                )
                .set_author(name=context.user.username, icon=context.user.avatar_url)
                .set_image(woofy.Client().images.search()[0].url)
            )
        )
