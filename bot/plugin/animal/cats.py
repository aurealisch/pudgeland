import crescent

from bot.plugin import animal, plugins
from bot.plugin.locale import locales
from bot.plugin.middleware.animal import cats

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
        await cats.Middleware(plugin).callback(context)
