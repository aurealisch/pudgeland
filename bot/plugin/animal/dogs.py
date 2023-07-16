import crescent

from bot.plugin import animal, plugins
from bot.plugin.locale import locales
from bot.plugin.middleware.animal import dogs

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
        await dogs.Middleware(plugin).callback(context)
