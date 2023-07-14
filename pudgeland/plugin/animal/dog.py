import crescent

from pudgeland.plugin import animal
from pudgeland.locale.plugin import locales
from pudgeland.utility.plugin import plugins
from pudgeland.component.plugin.animal import dog

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
        await dog.Component(plugin).callback(context)
