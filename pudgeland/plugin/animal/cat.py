import crescent

from pudgeland.plugin import animal
from pudgeland.locale.plugin import locales
from pudgeland.utility.plugin import plugins
from pudgeland.component.plugin.animal import cat

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
        await cat.Component(plugin).callback(context)
