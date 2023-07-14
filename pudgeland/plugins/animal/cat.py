import crescent

from pudgeland.plugins import animal
from pudgeland.locales.plugins import locale
from pudgeland.utilities.plugins import plugins
from pudgeland.components.plugins.animal import cat

plugin = plugins.Plugin()


@animal.group.child
@plugin.include
@crescent.command(
    name=locale.LocaleBuilder(
        "cat",
        russian="кот",
        ukrainian="кiт",
    ),
    description=locale.LocaleBuilder(
        "Image of a cat",
        russian="Изображение кота",
        ukrainian="Зображення кота",
    ),
)
class Cat:
    # noinspection PyMethodMayBeStatic
    async def callback(self, context: crescent.Context) -> None:
        await cat.Component(plugin).callback(context)
